import chromadb
from chromadb.utils import embedding_functions

# Create persistent Chroma client
client = chromadb.PersistentClient(path="chroma_db")

# Create or load collection
collection = client.get_or_create_collection(
    name="rag_collection",
    metadata={"hnsw:space": "cosine"}   # Use cosine similarity
)

# ----------------------------------------------------------------------
# STORE VECTORS
# ----------------------------------------------------------------------
import uuid

def store_vectors(chunks, embeddings):
    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    print("Stored", len(chunks), "vectors.")

# ----------------------------------------------------------------------
# SEARCH VECTORS
# ----------------------------------------------------------------------
def search_vectors(query_embedding):
    """
    Retrieves top 5 most relevant chunks for RAG.
    """

    print("=== SEARCH ===")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    retrieved = results.get("documents", [[]])[0]

    print("=== RETRIEVED CHUNKS ===")
    for chunk in retrieved:
        print(chunk[:200], "...")   # Print preview

    return retrieved
