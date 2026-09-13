from google import genai
from google.genai import types
import chromadb
from grounding import check_grounding
from reranker import rerank_documents

from config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_PATH,
    COLLECTION_NAME,
    LLM_MODEL
)
from scope import check_scope


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

def retrieve_documents(query, retrieval_k=10, final_k=3):

    query_embedding = create_query_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=retrieval_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    reranked = rerank_documents(
        query=query,
        documents=documents,
        top_k=final_k
    )

    reranked_documents = []
    reranked_metadatas = []
    rerank_scores = []

    for document, score, original_index in reranked:

        reranked_documents.append(document)
        reranked_metadatas.append(
            metadatas[original_index]
        )
        rerank_scores.append(float(score))

    return {
        "documents": [reranked_documents],
        "metadatas": [reranked_metadatas],
        "scores": rerank_scores
    }
# -----------------------------------
# Build context
# -----------------------------------

def build_context(results):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for document, metadata in zip(documents, metadatas):

        source = metadata.get("source", "Unknown Source")
        policy_id = metadata.get("policy_id", "Unknown Policy")

        context_parts.append(
            f"[Source: {source} | Policy ID: {policy_id}]\n"
            f"{document}"
        )

    return "\n".join(context_parts)


# -----------------------------------
# Generate grounded answer
# -----------------------------------

def generate_answer(query, context):

    prompt = f"""
You are an HR policy assistant.

Answer the user's question using ONLY the information
provided in the CONTEXT below.

Rules:

1. Answer the question directly.
2. Keep the answer concise and focused.
3. Provide the exact value, limit, percentage, number, or rule when available.
4. Do not include additional policy details unless necessary.
5. Do not use outside knowledge.
6. Do not invent or assume information.
7. After answering, provide the source policy.
8. Use the source information provided in the context.
9. If the answer cannot be found in the context, say:
   "I don't have enough information in the company policies to answer that."
10. Do not create or modify policy IDs.

Format the response as:

Answer: <direct answer>

Source: <policy name> (<policy ID>)

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""
    chat = client.chats.create(
        model=LLM_MODEL
    )

    response = chat.send_message(
        prompt
    )

    return response.text.strip()
# -----------------------------------
# Complete RAG pipeline
# -----------------------------------

def ask_question(query, retrieval_k=10, final_k=3):

    if not check_scope(query):

        answer = (
            "I can't answer that because the required "
            "employee-specific information is not available "
            "in the company policy knowledge base."
        )

        return answer, {
            "documents": [[]],
            "metadatas": [[]],
            "scores": []
        }

    results = retrieve_documents(
        query=query,
        retrieval_k=retrieval_k,
        final_k=final_k
    )

    print("Reranker scores:", results["scores"])

    context = build_context(results)
    if not check_grounding(query, context):

        answer = (
            "I don't have enough information in the company "
            "policies to answer that."
        )

        return answer, results
    
    answer = generate_answer(query, context)

    return answer, results