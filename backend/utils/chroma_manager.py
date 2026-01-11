import chromadb

client = chromadb.Client()

# ChromaDB old versions do NOT support embedding_dim → remove it
collection = client.get_or_create_collection(
    name="rag_chunks",
    metadata={"hnsw:space": "cosine"}
)

def store_vectors(chunks, embeddings):
    print("=== STORING 384-DIM EMBEDDINGS ===")

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks
    )

def search_vectors(query_embedding):
    print("=== SEARCH USING 384-DIM EMBEDDING ===")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    return results["documents"][0]
