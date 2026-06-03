"""Create the Qdrant collection and ingest the sample ML FAQ knowledge base."""

from dotenv import load_dotenv

from rag_code import FAQ_TEXT, EmbedData, QdrantVDB

load_dotenv()


def main():
    contexts = [chunk.replace("\n", " ") for chunk in FAQ_TEXT.split("\n\n")]

    embeddata = EmbedData()
    embeddata.embed(contexts)

    vector_db = QdrantVDB()
    vector_db.create_collection()
    vector_db.ingest_data(embeddata)

    print(f"Ingested {len(contexts)} FAQ chunks into Qdrant collection '{vector_db.collection_name}'.")


if __name__ == "__main__":
    main() 
