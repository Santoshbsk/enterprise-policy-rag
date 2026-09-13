from google import genai

from config import GEMINI_API_KEY, LLM_MODEL


client = genai.Client(api_key=GEMINI_API_KEY)


def check_grounding(query, context):

    prompt = f"""
You are a grounding checker for an enterprise HR policy assistant.

Determine whether the CONTEXT contains enough information
to answer the USER QUESTION.

Return ONLY one of:

SUPPORTED
NOT_SUPPORTED

Rules:

- Return SUPPORTED if the context directly contains the
  information required to answer the question.
- Return NOT_SUPPORTED if the answer cannot be determined
  from the context.
- Do not use outside knowledge.
- Do not make assumptions.

CONTEXT:
{context}

USER QUESTION:
{query}

CLASSIFICATION:
"""
    chat = client.chats.create(
        model=LLM_MODEL
    )
    
    response = chat.send_message(
        prompt
    )

    result = response.text.strip().upper()

    return result == "SUPPORTED"