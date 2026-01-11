import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def embed_text(chunks):
    if not API_KEY:
        raise Exception("OPENROUTER_API_KEY missing from .env")

    url = "https://openrouter.ai/api/v1/embeddings"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "My RAG App",
        "Content-Type": "application/json"
    }

    embeddings = []

    for text in chunks:
        payload = {
            "model": "openai/text-embedding-3-small",  # ← 384 DIM MODEL
            "input": text
        }

        response = requests.post(url, json=payload, headers=headers)
        res = response.json()

        if "error" in res:
            raise Exception(f"Embedding error: {res}")

        vectors = res["data"][0]["embedding"]
        embeddings.append(vectors)

    return embeddings
