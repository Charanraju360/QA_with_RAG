import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_answer(question, context):
    if not API_KEY:
        raise Exception("Missing OPENROUTER_API_KEY in .env")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "RAG App",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful RAG assistant. Only answer using the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if "error" in data:
            print("LLM ERROR:", data)
            return "LLM request failed."

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("LLM REQUEST FAILED:", e)
        return "Error generating answer."
