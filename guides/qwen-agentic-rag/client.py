import argparse
import time

import requests

SERVER_URL = "http://127.0.0.1:8001"


def main():
    parser = argparse.ArgumentParser(description="Send a query to the Agentic RAG API.")
    parser.add_argument("--query", type=str, required=True, help="Question to ask the crew.")
    parser.add_argument(
        "--url",
        type=str,
        default=SERVER_URL,
        help="LitServe base URL (default: http://127.0.0.1:8000)",
    )
    args = parser.parse_args()

    payload = {"query": args.query}

    try:
        response = requests.post(f"{args.url}/predict", json=payload, timeout=600)
        response.raise_for_status()
        answer = response.json()["output"]

        for token in answer.split():
            print(token, end=" ", flush=True)
            time.sleep(0.03)
        print()
    except requests.exceptions.RequestException as error:
        print(f"Error sending request: {error}")


if __name__ == "__main__":
    main()
