"""
evaluate.py: run all 5 evaluation questions through ask() and write results to evaluate.txt.

Usage:
    python evaluate.py
"""

from pathlib import Path
from query import ask

QUESTIONS = [
    "What should students watch out for in Professor Karrah's class?",
    "Which CS professor is the most recommended, and which is the most warned against?",
    "Why do students recommend Arnold for CS1200 but warn against him for other courses like CS1337?",
    "What went wrong with Professor Jason Smith's final exam?",
    "What percentage of students said they would take Professor Arnold again?",
]

lines = []
for i, q in enumerate(QUESTIONS, 1):
    result = ask(q)
    lines.append(f"\n{'='*70}")
    lines.append(f"Q{i}: {q}")
    lines.append(f"\nRetrieved chunks:")
    for h in result["hits"]:
        preview = h["text"][:120].replace("\n", " ")
        lines.append(f"  [{h['distance']}] ({h['professor']}, {h['course']}) {preview}...")
    lines.append(f"\nAnswer:\n{result['answer']}")
    lines.append(f"\nSources: {', '.join(result['sources']) or '(none)'}")
    print(f"Q{i} done.")

output = "\n".join(lines)
Path("evaluate.txt").write_text(output, encoding="utf-8")
print("\nResults written to evaluate.txt")
