from crewai.tools import tool

from dotenv import load_dotenv

from rag_code import COLLECTION_NAME, EmbedData, QdrantVDB, Retriever

load_dotenv()


@tool("Machine Learning FAQ Retrieval Tool")
def ml_faq_retrieval_tool(query: str) -> str:
    """Retrieve the most relevant documents from the machine learning FAQ collection.
    Use this tool when the user asks about ML fundamentals, model training, or evaluation.
    """
    retriever = Retriever(QdrantVDB(COLLECTION_NAME), EmbedData())
    return retriever.search(query)
