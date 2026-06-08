"""
ingest.py load RMP professor review files, parse each review as a
self-contained chunk with professor name and course code prepended,
and write chunks.json.

Usage:
    python ingest.py            # build chunks.json
    python ingest.py inspect    # build, then print 5 sample chunks + stats
"""

import json
import re
import sys
from pathlib import Path

DOCS_DIR = Path("documents")
OUTPUT_FILE = Path("chunks.json")
MAX_CHUNK_CHARS = 800
OVERLAP_CHARS = 80
MIN_CHUNK_CHARS = 50

# Lines that are pure RMP interface noise and should be dropped.
NOISE_LINES = {
    "logo", "professors", "caret down", "professor name", "your school",
    "log in", "sign up", "help", "rate", "compare", "arrow icon",
    "rating distribution", "awesome 5", "great 4", "good 3", "ok 2", "awful 1",
    "similar professors", "all courses", "quality", "difficulty",
    "helpful", "thumbs up", "thumbs down", "load more ratings",
    "site guidelines", "terms & conditions", "privacy policy",
    "copyright compliance policy", "ca notice at collection",
    "do not sell my personal information", "participation matters",
    "amazing lectures", "hilarious", "tough grader", "get ready to read",
    "graded by few things", "accessible outside class", "lecture heavy",
    "test heavy", "lots of homework", "clear grading criteria",
    "gives good feedback", "caring", "respected", "inspirational",
    "so many papers", "group projects", "online savvy", "extra credit",
    "beware of pop quizzes", "skip class? you won't pass.",
}

# Matches RMP metadata lines that appear before the review text.
METADATA_RE = re.compile(
    r"^(for credit|attendance|would take again|grade|textbook|online class"
    r"|reviewed:)\s*[:\-]",
    re.IGNORECASE,
)

# Matches a course code like CS1337, CE2336, CS6308, etc.
COURSE_RE = re.compile(r"^(?:Computer Icon)?((?:CS|CE|EE)\d{3,4})\s*$", re.IGNORECASE)

# Matches a date line like "Apr 9th, 2026" or "Jun 2nd, 2026".
DATE_RE = re.compile(
    r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\w*,\s+\d{4}$",
    re.IGNORECASE,
)

# Matches pure number lines (scores like "4.0", "1.0", counts like "0", "3").
NUMBER_RE = re.compile(r"^\d+(\.\d+)?$")

# Matches the overall stats block lines.
STATS_RE = re.compile(
    r"^(\d+\.?\d*\s*/\s*5|overall quality|based on \d+|level of difficulty"
    r"|\d+%|would take again|\d+\s*student ratings|i\'m professor)",
    re.IGNORECASE,
)


def extract_professor_name(lines: list[str]) -> str:
    """Return the professor name from the file header."""
    for i, line in enumerate(lines[:30]):
        if line.strip().lower() == "computer science":
            if i > 0:
                return lines[i - 1].strip()
    return "Unknown Professor"


def is_noise(line: str) -> bool:
    clean = line.strip().lower()
    if not clean:
        return True
    if clean in NOISE_LINES:
        return True
    if NUMBER_RE.match(clean):
        return True
    if DATE_RE.match(clean):
        return True
    if METADATA_RE.match(clean):
        return True
    if STATS_RE.match(clean):
        return True
    # Footer copyright line
    if clean.startswith("© "):
        return True
    return False


def split_into_review_blocks(lines: list[str]) -> list[list[str]]:
    """Split raw lines into per-review blocks, each starting at a Quality marker."""
    blocks, current = [], []
    for line in lines:
        if line.strip().lower() == "quality":
            if current:
                blocks.append(current)
            current = []
        else:
            current.append(line)
    if current:
        blocks.append(current)
    return blocks


def extract_course(block_lines: list[str]) -> str:
    """Return the course code from the first few lines of a block."""
    for line in block_lines[:10]:
        m = COURSE_RE.match(line.strip())
        if m:
            return m.group(1).upper()
    return "Unknown Course"


def extract_review_text(block_lines: list[str]) -> str:
    """Return only the substantive review text from a block, stripping noise."""
    text_lines = []
    for line in block_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if COURSE_RE.match(stripped):
            continue
        if is_noise(stripped):
            continue
        text_lines.append(stripped)
    return " ".join(text_lines).strip()


def split_long_review(text: str) -> list[str]:
    """If a single review exceeds MAX_CHUNK_CHARS, split it with overlap."""
    if len(text) <= MAX_CHUNK_CHARS:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + MAX_CHUNK_CHARS
        chunks.append(text[start:end])
        start = end - OVERLAP_CHARS
    return chunks


def build_chunks() -> list[dict]:
    if not DOCS_DIR.exists():
        raise SystemExit("documents/ folder not found.")
    files = sorted(p for p in DOCS_DIR.iterdir() if p.suffix.lower() == ".txt")
    if not files:
        raise SystemExit("No .txt files found in documents/.")

    records = []
    for path in files:
        raw_lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        professor = extract_professor_name(raw_lines)
        blocks = split_into_review_blocks(raw_lines)
        file_chunks = 0

        for block in blocks:
            course = extract_course(block)
            # Skip the header block since it has no course code
            if course == "Unknown Course":
                continue
            review_text = extract_review_text(block)
            if len(review_text) < MIN_CHUNK_CHARS:
                continue
            label = f"Professor {professor}, {course}:"
            full_text = f"{label} {review_text}"
            for part in split_long_review(full_text):
                if len(part) < MIN_CHUNK_CHARS:
                    continue
                records.append({
                    "id": f"{path.stem}-{len(records)}",
                    "text": part,
                    "source": path.name,
                    "professor": professor,
                    "course": course,
                })
                file_chunks += 1

        print(f"  {path.name}: {file_chunks} chunks")

    return records


def inspect(records: list[dict]) -> None:
    total = len(records)
    print(f"\nTotal chunks: {total}")
    if total < 50:
        print("Warning: fewer than 50 chunks. Chunks may be too large.")
    elif total > 2000:
        print("Warning: more than 2000 chunks. Chunks may be too small.")
    else:
        print("Chunk count looks good.")

    step = max(1, total // 5)
    print("\n--- 5 sample chunks ---")
    for r in records[::step][:5]:
        print(f"\n[{r['source']} | {r['course']} | {len(r['text'])} chars]")
        print(r["text"])
        print()


if __name__ == "__main__":
    print("Loading and chunking documents...")
    records = build_chunks()
    OUTPUT_FILE.write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nWrote {len(records)} chunks to {OUTPUT_FILE}")
    if len(sys.argv) > 1 and sys.argv[1] == "inspect":
        inspect(records)
