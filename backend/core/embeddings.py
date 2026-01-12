from sentence_transformers import SentenceTransformer

# MiniLM = 384 dimensions
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text_list):
    """
    Input: list[str]
    Output: list[list[float]] (384-dim vectors)
    """
    embeddings = model.encode(text_list, convert_to_numpy=True)
    return embeddings.tolist()
