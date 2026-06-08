"""
query.py: retrieve relevant chunks and generate a grounded answer via Groq.

Usage:
    python query.py "question"
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq

from embed import retrieve, TOP_K

load_dotenv()

LLM_MODEL = "llama-3.3-70b-versatile"
REFUSAL = "I don't have enough information on that."

SYSTEM_PROMPT = (
    "You are a helpful assistant answering questions about student reviews of "
    "Computer Science professors at the University of Texas at Dallas. "
    "Answer the question using ONLY the information in the provided context below. "
    "Do not use any outside knowledge or make up any details. "
    "Do not include source numbers or citation labels like (Source 1) in your answer. "
    "Sources are listed separately after your response. "
    "If the context does not contain enough information to answer, reply exactly: "
    f'"{REFUSAL}"'
)


def _client() -> Groq:
    key = os.environ.get("GROQ_API_KEY")
    if not key or key == "your_key_here":
        raise SystemExit("Set GROQ_API_KEY in your .env file.")
    return Groq(api_key=key)


def build_context(hits: list[dict]) -> str:
    blocks = []
    for i, h in enumerate(hits, 1):
        blocks.append(f"[Source {i}: {h['source']}]\n{h['text']}")
    return "\n\n".join(blocks)


def ask(question: str, k: int = TOP_K) -> dict:
    hits = retrieve(question, k=k)
    context = build_context(hits)
    user_msg = f"Context:\n{context}\n\nQuestion: {question}"

    response = _client().chat.completions.create(
        model=LLM_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    )
    answer = response.choices[0].message.content.strip()

    # Attach sources
    sources = []
    if REFUSAL not in answer:
        seen = set()
        for h in hits:
            if h["source"] not in seen:
                seen.add(h["source"])
                sources.append(h["source"])

    return {"answer": answer, "sources": sources, "hits": hits}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python query.py "your question"')
    result = ask(" ".join(sys.argv[1:]))
    print("\nANSWER:\n" + result["answer"])
    if result["sources"]:
        print("\nSOURCES:")
        for s in result["sources"]:
            print(f"  {s}")
