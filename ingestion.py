import os
import chromadb

from config import CHROMA_PATH, COLLECTION_NAME
from chunking import chunk_text
from embeddings import create_embeddings


DOCUMENTS_FOLDER = "./docs"


# -----------------------------
# Metadata for each document
# -----------------------------

DOCUMENT_METADATA = {
    "leave_policy.txt": {
        "department": "HR",
        "policy_type": "leave",
        "policy_id": "HR-LEAVE-001",
        "year": 2026
    },

    "travel_policy.txt": {
        "department": "Finance",
        "policy_type": "travel",
        "policy_id": "FIN-TRAVEL-001",
        "year": 2026
    },

    "wfh_policy.txt": {
        "department": "HR",
        "policy_type": "wfh",
        "policy_id": "HR-WFH-001",
        "year": 2026
    },

    "benefits_policy.txt": {
        "department": "HR",
        "policy_type": "benefits",
        "policy_id": "HR-BENEFITS-001",
        "year": 2026
    }
}


# -----------------------------
# Connect to ChromaDB
# -----------------------------

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)

if collection.count() > 0:
    print("ChromaDB already contains data.")
    print(f"Existing chunks: {collection.count()}")
    print("Skipping ingestion.")
    exit()


# -----------------------------
# Read documents
# -----------------------------

all_chunks = []
all_metadata = []
all_ids = []


for filename in os.listdir(DOCUMENTS_FOLDER):

    if not filename.endswith(".txt"):
        continue

    file_path = os.path.join(
        DOCUMENTS_FOLDER,
        filename
    )

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="replace"
    ) as file:

        text = file.read()


    # Create chunks
    chunks = chunk_text(
        text,
        chunk_size=500,
        overlap=50
    )


    # Get document metadata
    base_metadata = DOCUMENT_METADATA.get(
        filename,
        {}
    )


    # Store chunks + metadata
    for index, chunk in enumerate(chunks):

        metadata = {
            "source": filename,
            **base_metadata,
            "chunk_id": index
        }

        chunk_id = f"{filename}_{index}"


        all_chunks.append(chunk)
        all_metadata.append(metadata)
        all_ids.append(chunk_id)


# -----------------------------
# Create embeddings
# -----------------------------

print(f"Total chunks created: {len(all_chunks)}")

embeddings = create_embeddings(all_chunks)


# -----------------------------
# Insert into ChromaDB
# -----------------------------

collection.upsert(
    ids=all_ids,
    documents=all_chunks,
    metadatas=all_metadata,
    embeddings=embeddings
)


print("Successfully inserted chunks into ChromaDB.")

print(
    f"Total documents in collection: {collection.count()}"
)