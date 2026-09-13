from google import genai
from config import GEMINI_API_KEY, LLM_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def check_scope(query):

    prompt = f"""
You are a scope classifier for an enterprise HR policy assistant.

The assistant can answer questions about:
- Company HR policies
- Leave policies
- Work from home policies
- Travel policies
- Employee benefits
- Insurance benefits
- Company rules and procedures

The assistant CANNOT answer questions requiring:
- An employee's personal records
- An employee's historical transactions
- Individual leave balances or leave taken
- Payroll or salary records
- Attendance records
- Information from HR systems that is not present in the policy documents

Classify the user's question as either:

IN_SCOPE
or
OUT_OF_SCOPE

Return ONLY one of these two values.

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

    return result == "IN_SCOPE"