# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Student reviews of **Computer Science professors at the University of Texas at Dallas**, collected from RateMyProfessors. The system answers plain-language questions about teaching style, workload, exam format, and which courses a professor is good/bad for.

This knowledge is hard to find officially because the course catalog describes *what* a course covers, not *how* a professor teaches it. The lived experience exists only in student-to-student reviews, scattered across hundreds of individual ratings per professor.

---

## Documents

10 professor pages from [RateMyProfessors](https://www.ratemyprofessors.com), UT Dallas Computer Science department. Each file contains the full set of student reviews across **all courses** that professor teaches.

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Gordon Arnold | RMP reviews, all CS courses | [`rmp_gordon_arnold.txt`](documents/rmp_gordon_arnold.txt) \| [RMP URL](https://www.ratemyprofessors.com/professor/1976371) |
| 2 | Shyam Karrah | RMP reviews, all CS courses | [`rmp_shyam_karrah.txt`](documents/rmp_shyam_karrah.txt) \| [RMP URL](https://www.ratemyprofessors.com/professor/1554657) |
| 3 | Jason Smith | RMP reviews, all CS courses | [`rmp_jason_smith.txt`](documents/rmp_jason_smith.txt) \| [RMP URL](https://www.ratemyprofessors.com/professor/1833058) |
| 4 | Srimathi Srinivasan | RMP reviews, all CS courses | [`rmp_srimathi_srinivasan.txt`](documents/rmp_srimathi_srinivasan.txt) \| [RMP URL](https://www.ratemyprofessors.com/professor/2424646) |
| 5 | Priya Narayanasami | RMP reviews, all CS courses | [`rmp_priya_narayanasami.txt`](documents/rmp_priya_narayanasami.txt) \| [RMP URL](https://www.ratemyprofessors.com/professor/2337456) |
| 6 | Neeraj Gupta | RMP reviews, all CS courses | [`rmp_neeraj_gupta.txt`](documents/rmp_neeraj_gupta.txt) \| [RMP URL](https://www.ratemyprofessors.com/professor/1916155) |
| 7 | Miguel Razo | RMP reviews, all CS courses | [`rmp_miguel_razo.txt`](documents/rmp_miguel_razo.txt) \| [RMP URL](https://www.ratemyprofessors.com/professor/1607810) |
| 8 | Brian Ricks | RMP reviews, all CS courses | [`rmp_brian_ricks.txt`](documents/rmp_brian_ricks.txt) \| [RMP URL](https://www.ratemyprofessors.com/professor/2822326) |
| 9 | Laurie Thompson | RMP reviews, all CS courses | [`rmp_laurie_thompson.txt`](documents/rmp_laurie_thompson.txt) \| [RMP URL](https://www.ratemyprofessors.com/professor/191259) |
| 10 | Scott Dollinger | RMP reviews, all CS courses | [`rmp_scott_dollinger.txt`](documents/rmp_scott_dollinger.txt) \| [RMP URL](https://www.ratemyprofessors.com/professor/2523207) |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
