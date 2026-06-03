"""Simple web UI for the Agentic RAG API. Start server.py first."""

import os

import gradio as gr
import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_API_URL = os.getenv("SERVER_URL", "http://127.0.0.1:8001")
UI_PORT = int(os.getenv("UI_PORT", "7860"))


def ask(query: str, api_url: str) -> str:
    if not query.strip():
        return "Please enter a question."

    base = api_url.strip().rstrip("/")
    try:
        response = requests.post(
            f"{base}/predict",
            json={"query": query.strip()},
            timeout=600,
        )
        response.raise_for_status()
        return response.json()["output"]
    except requests.exceptions.ConnectionError:
        return (
            f"**Cannot connect to** `{base}`\n\n"
            "Start the API in another terminal:\n\n"
            "```bash\npython server.py\n```"
        )
    except requests.exceptions.HTTPError as error:
        return f"**API error:** {error}"
    except requests.exceptions.Timeout:
        return "**Request timed out** (over 10 minutes). Try a shorter question or check Ollama."
    except requests.exceptions.RequestException as error:
        return f"**Error:** {error}"


def main():
    with gr.Blocks(title="Agentic RAG") as demo:
        gr.Markdown(
            "# Agentic RAG\n"
            "Private Qwen + CrewAI (Researcher → Writer). "
            "**Run `python server.py` first**, then ask a question."
        )
        api_url = gr.Textbox(label="API URL", value=DEFAULT_API_URL)
        query = gr.Textbox(
            label="Question",
            placeholder="What is cross-validation and why is it important?",
            lines=2,
        )
        ask_btn = gr.Button("Ask", variant="primary")
        answer = gr.Markdown(label="Answer")

        gr.Examples(
            examples=[
                ["What is cross-validation and why is it important?"],
                ["How do I avoid overfitting?"],
                ["When should I use deep learning?"],
            ],
            inputs=query,
        )

        inputs = [query, api_url]
        ask_btn.click(fn=ask, inputs=inputs, outputs=answer)
        query.submit(fn=ask, inputs=inputs, outputs=answer)

    demo.launch(server_name="127.0.0.1", server_port=UI_PORT)


if __name__ == "__main__":
    main()
