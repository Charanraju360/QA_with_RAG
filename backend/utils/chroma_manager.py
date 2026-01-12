import chromadb
import uuid

# Persistent Chroma client
client = chromadb.PersistentClient(path="chroma_db")

# Create initial collection
collection = client.get_or_create_collection(
    name="rag_collection",
    metadata={"hnsw:space": "cosine"}
)


def reset_chroma():
    """
    Deletes the entire ChromaDB collection so old vectors are removed.
    Recreates a fresh empty collection.
    """
    global collection

    try:
        client.delete_collection("rag_collection")
        print("Old Chroma collection deleted.")
    except Exception as e:
        print("No existing collection or deletion failed:", e)

    # Recreate new empty collection
    collection = client.get_or_create_collection(
        name="rag_collection",
        metadata={"hnsw:space": "cosine"}
    )

    print("New empty Chroma collection created.")


def store_vectors(chunks, embeddings):
    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    print(f"Stored {len(chunks)} vectors.")
    return True


def search_vectors(query_embedding):
    """
    Retrieves top 5 most relevant chunks.
    """
    print("=== SEARCHING VECTORS ===")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    retrieved = results.get("documents", [[]])[0]

    print("=== RETRIEVED CHUNKS ===")
    for chunk in retrieved:
        print(chunk[:200], "...")

    return retrieved
