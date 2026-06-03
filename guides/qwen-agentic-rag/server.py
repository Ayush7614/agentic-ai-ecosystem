import os

import litserve as ls
from crewai import Agent, Crew, LLM, Task
from crewai_tools import FirecrawlSearchTool
from dotenv import load_dotenv

from tools import ml_faq_retrieval_tool

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "ollama/qwen3.6:27b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


class AgenticRAGAPI(ls.LitAPI):
    def setup(self, device):
        llm = LLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
        )

        researcher_tools = [ml_faq_retrieval_tool]
        firecrawl_key = os.getenv("FIRECRAWL_API_KEY", "").strip()
        if firecrawl_key:
            researcher_tools.append(FirecrawlSearchTool())

        web_search_hint = (
            "Use Firecrawl web search for recent or general topics not covered in the knowledge base."
            if firecrawl_key
            else "Use only the ML FAQ retrieval tool."
        )
        fallback_hint = (
            "Fall back to Firecrawl for everything else."
            if firecrawl_key
            else "Answer from the ML FAQ knowledge base only."
        )

        researcher_agent = Agent(
            role="Researcher",
            goal="Research the user's query using the vector database and web search tools",
            backstory=(
                "You are a research assistant. Prefer the ML FAQ retrieval tool for "
                f"machine-learning questions. {web_search_hint}"
            ),
            verbose=True,
            tools=researcher_tools,
            llm=llm,
        )

        writer_agent = Agent(
            role="Writer",
            goal="Write a clear, accurate answer using the researcher's findings",
            backstory=(
                "You synthesize research into concise, well-structured answers. "
                "Cite whether information came from the knowledge base or the web."
            ),
            verbose=True,
            llm=llm,
        )

        researcher_task = Task(
            description=(
                "Research the user's query and collect the most relevant context: {query}. "
                f"Use the ML FAQ tool first for ML topics. {fallback_hint}"
            ),
            expected_output="A bullet list of key findings with sources (vector DB or web).",
            agent=researcher_agent,
        )

        writer_task = Task(
            description=(
                "Using the research findings, write a final answer for: {query}. "
                "Keep it concise, factual, and easy to read."
            ),
            expected_output="A polished answer to the user's query.",
            agent=writer_agent,
            context=[researcher_task],
        )

        self.crew = Crew(
            agents=[researcher_agent, writer_agent],
            tasks=[researcher_task, writer_task],
            verbose=True,
        )

    def decode_request(self, request):
        query = request.get("query", "").strip()
        if not query:
            raise ValueError("Missing required field: query")
        return query

    def predict(self, query):
        result = self.crew.kickoff(inputs={"query": query})
        return result.raw if hasattr(result, "raw") else str(result)

    def encode_response(self, output):
        return {"output": output}


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8001"))
    api = AgenticRAGAPI()
    server = ls.LitServer(api, timeout=False)
    server.run(port=port)
