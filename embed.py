"""
embed.py: embed chunks.json into ChromaDB and provide a retrieval function.

Usage:
    python embed.py           # build the vector store
    python embed.py test      # run sample queries and print results
"""

import json
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "unofficial_guide"
CHROMA_DIR = "chroma_db"
CHUNKS_FILE = Path("chunks.json")
TOP_K = 5

_model = None
_collection = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
        )
    return _collection


def build_store() -> None:
    if not CHUNKS_FILE.exists():
        raise SystemExit("chunks.json not found. Run `python ingest.py` first.")
    records = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

    model = get_model()
    texts = [r["text"] for r in records]
    print(f"Embedding {len(texts)} chunks with {EMBED_MODEL}...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        ids=[r["id"] for r in records],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{
            "source": r["source"],
            "professor": r["professor"],
            "course": r["course"],
        } for r in records],
    )
    print(f"Stored {collection.count()} chunks in ChromaDB ({CHROMA_DIR}/).")


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """Return the top-k most similar chunks with source, professor, course, and distance."""
    model = get_model()
    collection = get_collection()
    q_emb = model.encode([query]).tolist()
    res = collection.query(query_embeddings=q_emb, n_results=k)
    hits = []
    for doc, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        hits.append({
            "text": doc,
            "source": meta["source"],
            "professor": meta["professor"],
            "course": meta["course"],
            "distance": round(float(dist), 3),
        })
    return hits


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        questions = [
            "What should students watch out for in Professor Karrah's class?",
            "Which professor is the most recommended at UTD CS?",
            "Why is Arnold good for CS1200 but bad for other courses?",
        ]
        for q in questions:
            print(f"\n=== {q}")
            for h in retrieve(q):
                preview = h["text"][:160].replace("\n", " ")
                print(f"  [{h['distance']}] ({h['professor']}, {h['course']}) {preview}...")
    else:
        build_store()
