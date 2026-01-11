import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_answer(context: str, question: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""
You MUST answer only using the document below.

Document:
{context}

Question:
{question}

If the answer is not in the document, reply:
"The answer is not present in the document."
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost:5173/",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if "choices" not in data:
            return f"OpenRouter API Error:\n{data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"LLM Error: {str(e)}"
