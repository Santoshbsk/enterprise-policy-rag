from google import genai
from google.genai import types

from config import GEMINI_API_KEY, EMBEDDING_MODEL


client = genai.Client(api_key=GEMINI_API_KEY)


def create_embeddings(texts, batch_size=100):

    all_embeddings = []

    for start in range(0, len(texts), batch_size):

        batch = texts[start:start + batch_size]

        print(
            f"Embedding chunks {start + 1} "
            f"to {start + len(batch)} "
            f"of {len(texts)}"
        )

        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=768
            )
        )

        batch_embeddings = [
            embedding.values
            for embedding in result.embeddings
        ]

        all_embeddings.extend(batch_embeddings)

    return all_embeddings