from google import genai
from google.genai import types
import chromadb

from config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_PATH,
    COLLECTION_NAME
)


# -----------------------------------
# Gemini client
# -----------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# -----------------------------------
# ChromaDB
# -----------------------------------

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_collection(
    name=COLLECTION_NAME
)


# -----------------------------------
# Create query embedding
# -----------------------------------

def create_query_embedding(query):

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values


# -----------------------------------
# Retrieve relevant chunks
# -----------------------------------

def retrieve_documents(query, top_k=3):

    query_embedding = create_query_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


# -----------------------------------
# Build context
# -----------------------------------

def build_context(results):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for i, document in enumerate(documents):

        metadata = metadatas[i]

        context_parts.append(
            f"""
SOURCE: {metadata.get("source")}
POLICY TYPE: {metadata.get("policy_type")}
POLICY ID: {metadata.get("policy_id")}

CONTENT:
{document}
"""
        )

    return "\n".join(context_parts)


# -----------------------------------
# Generate grounded answer
# -----------------------------------

def generate_answer(query, context):

    prompt = f"""
You are an HR policy assistant.

Answer the user's question using ONLY the policy information
provided in the CONTEXT below.

Do not use outside knowledge.

If the answer cannot be found in the context, say:

"I don't have enough information in the company policies to answer that."

Do not invent or assume information.

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    chat = client.chats.create(
    model="gemini-3.6-flash"
    )

    response = chat.send_message(
        message=prompt
    )
    # response = client.models.generate_content(
    #     model="gemini-3.8-flash",
    #     contents=prompt
    # )

    return response.text


# -----------------------------------
# Complete RAG pipeline
# -----------------------------------

def ask_question(query, top_k=3):

    results = retrieve_documents(
        query,
        top_k=top_k
    )

    context = build_context(results)

    answer = generate_answer(
        query,
        context
    )

    return answer, results