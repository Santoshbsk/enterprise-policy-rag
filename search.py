from google import genai
from google.genai import types
import chromadb

from config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_PATH,
    COLLECTION_NAME
)


# Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ChromaDB client
chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)


def search(query, top_k=3):

    # Convert user's question into embedding
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768
        )
    )

    query_embedding = result.embeddings[0].values


    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )


    return results


# Test
query = "How many annual leave days do employees get?"

results = search(query)


for i, document in enumerate(results["documents"][0]):

    print("\n-----------------------------")

    print(f"Result {i + 1}")

    print("-----------------------------")

    print("Document:")

    print(document)

    print("\nMetadata:")

    print(results["metadatas"][0][i])

    print("\nDistance:")

    print(results["distances"][0][i])