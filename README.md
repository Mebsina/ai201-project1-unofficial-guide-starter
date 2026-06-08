# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Student reviews of **Computer Science professors at the University of Texas at Dallas**, collected from [RateMyProfessors](https://www.ratemyprofessors.com). The system answers plain-language questions about teaching style, workload, exam format, and which courses a professor is good or bad for.

This knowledge is hard to find officially because the course catalog describes *what* a course covers, not *how* a professor teaches it. The lived experience exists only in student-to-student reviews, scattered across hundreds of individual ratings per professor.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
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

**Chunk size:** One review per chunk, typically 300 to 600 characters. A review longer than 800 characters is split with a small overlap; shorter reviews are kept whole.

**Overlap:** About 80 characters, applied only when a single long review must be split. There is no overlap between separate reviews since each review is already a self-contained unit.

**Why these choices fit your documents:** RMP data is review-heavy, not long-form prose. Each review is a short, self-contained opinion about one course with one professor. A fixed character splitter would either merge two unrelated students' opinions into one chunk or cut a single opinion in half, both of which weaken retrieval. The strategy is review-aware: each chunk is one review with the professor name and course code prepended, for example `Professor Arnold, CS1337: "..."`. This keeps every chunk independently retrievable and preserves attribution so the system can tell which course and professor a given opinion refers to.

**Final chunk count:** 311 chunks across 10 professor files.

### Sample chunks

**Chunk 1** (source: `rmp_brian_ricks.txt`)
> Professor Brian Ricks, CS1436: prof ricks is so nice! he made classes interesting, and grades really fairly. his exams are super easy compared to the other professors. he responds to emails quickly and is super nice and answers questions!

**Chunk 2** (source: `rmp_gordon_arnold.txt`)
> Professor Gordon Arnold, CS1337: Let me summarize his reviews. He is a good professor for CS 1200, and his 5-star ratings come mainly from students in that course. However, he is the worst professor for any other class that involves computer science topics.

**Chunk 3** (source: `rmp_laurie_thompson.txt`)
> Professor Laurie Thompson, CS1436: Please take this class either with a different professor or at a community college. The subject is not hard to grasp but prof made it extremely tough for no reason. Her lectures consisted of talking about the industry and reading off slides. For every minute you're late, you get points deducted.

**Chunk 4** (source: `rmp_shyam_karrah.txt`)
> Professor Shyam Karrah, CS1436: Prof. Karrah always made lectures interesting and engaging. Class participation is encouraged. Lab assignments are easy and only take an hour or so a week. Beware of pop quizzes late in the semester.

**Chunk 5** (source: `rmp_jason_smith.txt`)
> Professor Jason Smith, CS2337: Great class and was very easy to follow. There is a lot of work and projects, but they are very easy. He knows what he is talking about and answers questions. However, for the final, he gave some of us the wrong version of the exam and had to retake it.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`. It runs locally with no API key or rate limits, is small and fast, and handles short text like reviews well. It also enables semantic search: queries and reviews are compared by meaning, not exact words, so "is his grading harsh" can match a review that says "tough grader" even with no shared terms.

**Production tradeoff reflection:**

If I deployed this for real users and cost were not a constraint, I would weigh three factors when choosing a different embedding model:

- **Accuracy on domain-specific text:** a larger or domain-tuned model from a hosted API would capture slang and course-code semantics better than MiniLM.
- **Context length:** MiniLM truncates around 256 tokens, fine for single reviews but limiting if I later index long guides.
- **Latency and hosting:** local MiniLM has zero per-query cost but uses my own CPU or GPU, while a hosted API adds network latency and per-call cost but scales better.

---

## Retrieval Test Results

**Query 1:** What should students watch out for in Professor Karrah's class?

```
  [0.288] (Shyam Karrah, CS1436) Professor Shyam Karrah, CS1436: Prof. Karrah always made lectures interesting and engaging. Class participation is encou...
  [0.38] (Shyam Karrah, CS1436) Professor Shyam Karrah, CS1436: Dr. Karrah is passionate about teaching and he is also caring about his students. But th...
  [0.423] (Shyam Karrah, CS1436) Professor Shyam Karrah, CS1436: Prof. Karrah is an amazing professor and I strongly recommend him for this course. Profe...
  [0.429] (Shyam Karrah, CS1436) Professor Shyam Karrah, CS1436: Professor Karrah was an amazing lecturer and was good at explaining the concept and like...
  [0.45] (Shyam Karrah, CS1337) Professor Shyam Karrah, CS1337: Terrible professor. Can't teach and grades horribly. Need to figure out his teaching sty...
```

Why these chunks are relevant: All 5 results are from the Karrah file and directly address student experiences in his class. The top result explicitly mentions the pop quiz warning that matches the query. All distance scores are well below 0.5, indicating strong semantic matches.

**Query 2:** Which professor is the most recommended at UTD CS?

```
  [0.246] (Brian Ricks, CS1436) Professor Brian Ricks, CS1436: By far the best professor I have taken at UTD. Lectures are very interesting, he is very ...
  [0.254] (Brian Ricks, CS2336) Professor Brian Ricks, CS2336: The best professor I've had at UTD (and probably ever will). He truly cares about your suc...
  [0.314] (Brian Ricks, CS2336) Professor Brian Ricks, CS2336: The best professor at UTD. Ready to get invested in his stories and hobbies during the cla...
  [0.327] (Jason Smith, CS2336) Professor Jason Smith, CS2336: I took him for 1337 and he is extremely consistent in the way he teaches. You learn a lot,...
  [0.334] (Jason Smith, CS2337) Professor Jason Smith, CS2337: really great professor in my opinion, hes very flexible and easy to work with and i really...
```

Why these chunks are relevant: The top 3 results are all Ricks chunks containing superlative praise ("best professor at UTD"), which semantically matches the query. The distances are the lowest of any query at 0.246 to 0.314, reflecting very strong alignment.

**Query 3:** Why is Arnold good for CS1200 but bad for other courses?

```
  [0.318] (Gordon Arnold, CS1337) Professor Gordon Arnold, CS1337: Let me summarize his reviews. He is a good professor for CS 1200, and his 5-star ratin...
  [0.414] (Gordon Arnold, CS1200) Professor Gordon Arnold, CS1200: This is the best professor for the CS1200 course. He only gives out three assignments w...
  [0.423] (Gordon Arnold, CS1336) Professor Gordon Arnold, CS1336: Ok so this professor is not as bad as people make him out to be. He tries his bes...
  [0.449] (Gordon Arnold, CS1200) Professor Gordon Arnold, CS1200: i don't believe he will be teaching cs 1200 again, but if he is i would go for him. hi...
  [0.452] (Gordon Arnold, CS1200) Professor Gordon Arnold, CS1200: He is a good professor when he is on topic which is usually only about 60% of the time...
```

Why these chunks are relevant: The top result at 0.318 is a review that explicitly summarizes the CS1200 vs other courses contrast in a single chunk, making it the best possible retrieval result for this query. The remaining chunks reinforce both sides of the comparison.

---

## Grounded Generation

**System prompt grounding instruction:** The model receives the following system prompt on every query: "You are a helpful assistant answering questions about student reviews of Computer Science professors at the University of Texas at Dallas. Answer the question using ONLY the information in the provided context below. Do not use any outside knowledge or make up any details. Do not include source numbers or citation labels in your answer. If the context does not contain enough information to answer, reply exactly: 'I don't have enough information on that.'"

**How source attribution is surfaced in the response:** Source filenames are attached programmatically in `query.py` after the LLM responds, by reading the `source` field from the retrieved chunk metadata. This means citations are always accurate and present regardless of what the model writes. The model is explicitly told not to include citation labels in its answer body so that all attribution is handled by the pipeline, not the LLM.

### Example responses

**Example 1** (in-scope, cited)

Question: *What should students watch out for in Professor Karrah's class?*

Answer: In Professor Karrah's CS1436 class, students should watch out for pop quizzes late in the semester. Lectures may sometimes go overtime. Exams can be very detailed, requiring students to know every single thing. Students who take notes and practice outside of class tend to do well.

Sources: `rmp_shyam_karrah.txt`

**Example 2** (in-scope, cited)

Question: *Why do students recommend Arnold for CS1200 but warn against him for other courses like CS1337?*

Answer: Students recommend Professor Gordon Arnold for CS1200 because he is considered a good professor for that course, giving out only three assignments that are not difficult and being entertaining in class. However, they warn against him for other courses like CS1337 because he is reportedly not as effective in teaching other computer science topics, with some students considering him the worst professor for those classes.

Sources: `rmp_gordon_arnold.txt`, `rmp_miguel_razo.txt`

**Example 3** (out-of-scope refusal)

Question: *What is the best restaurant near campus?*

Answer: I don't have enough information on that.

Sources: (none)

---

## Query Interface

The interface is a Gradio web app launched with `python app.py` and accessible at `http://localhost:7860`.

**Input:** A single text box labeled "Your question" with a placeholder example. The user can submit by clicking the Ask button or pressing Enter.

**Output:** "Answer" showing the generated response and "Sources" listing the filenames the answer was drawn from.

**Sample interaction transcript**

Input: *What should students watch out for in Professor Karrah's class?*

Answer: In Professor Karrah's CS1436 class, students should watch out for pop quizzes late in the semester. Lectures may sometimes go overtime. Exams can be very detailed, requiring students to know every single thing. Students who take notes and practice outside of class tend to do well.

Sources: rmp_shyam_karrah.txt

---

## Evaluation Report

| # | Question | Expected answer | System response | Retrieval quality | Response accuracy |
|---|----------|-----------------|-----------------|-------------------|-------------------|
| 1 | What should students watch out for in Professor Karrah's class? | Pop quizzes, especially late in the semester. | Pop quizzes late in the semester, overtime lectures, and very detailed exams. Students who take notes and practice outside of class tend to do well. | Relevant | Accurate |
| 2 | Which CS professor is the most recommended, and which is the most warned against? | Most recommended: Brian Ricks. Most warned against: Laurie Thompson. | Most recommended are Karrah and Ricks. Most warned against is Arnold, described as only good for CS1200. | Partially relevant | Partially accurate |
| 3 | Why do students recommend Arnold for CS1200 but warn against him for other courses like CS1337? | CS1200 is easy with 3 assignments and no exams; other courses are textbook-heavy with hard exams. | Arnold is good for CS1200 because he gives only 3 easy assignments and is entertaining. He is warned against for other courses because he is ineffective at teaching other CS topics. | Relevant | Accurate |
| 4 | What went wrong with Professor Jason Smith's final exam? | He gave out the wrong version of the final, so affected students retook the correct one. | Professor Smith gave some students the wrong version of the exam, corrected the mistake quickly, and gave many options to retake it. | Relevant | Accurate |
| 5 | What percentage of students said they would take Professor Arnold again? | 49% | I don't have enough information on that. | Off-target | Inaccurate |

---

## Failure Case Analysis

**Question that failed:** What percentage of students said they would take Professor Arnold again?

**What the system returned:** "I don't have enough information on that." The top retrieved chunk had a distance of 0.426, and all 5 retrieved chunks were general Arnold reviews with no mention of the percentage.

**Root cause (tied to a specific pipeline stage):** The failure originates in the ingestion stage. The 49% figure appears on the RMP page as a bare label-value pair ("49% Would take again") with no surrounding sentence. During cleaning in `ingest.py`, this line is matched by `STATS_RE` as a stats-block line and stripped before chunking. Because the number never made it into any chunk, the vector store has no representation of it, and retrieval correctly returns nothing useful. The LLM then issues the refusal response as instructed.

**What you would change to fix it:** Preserve the page-level stats block as a dedicated structured chunk rather than stripping it. For example, combining the professor name, overall rating, difficulty, and "would take again" percentage into a single metadata chunk like `Professor Gordon Arnold overall stats: 3.1/5 quality, 3.2 difficulty, 49% would take again, 139 ratings` would give the embedding model a meaningful, queryable representation of those numbers.

---

## Spec Reflection

**One way the spec helped you during implementation:**
Writing the chunking strategy in planning.md before coding forced me to think through why review-aware chunking was the right approach before touching any code. When I got to Milestone 3, I already knew the chunk size, overlap, and the reasoning behind them, so I could give Claude specific inputs rather than vague instructions. Without the spec, I would have just used a generic fixed-size splitter and likely ended up with bad retrieval.

**One way your implementation diverged from the spec, and why:**
My spec described review-aware chunking but did not account for the RMP page header being parsed as a review block. During Milestone 3 I discovered the first chunk of every file was the ratings summary and similar professors list, which had no course code and no review text. I added a guard to skip any block that could not be assigned a course code, which was not in my original plan. The spec was correct in principle but incomplete for the specific structure of copied RMP pages.

---

## AI Usage

<!-- Fill these in your own words. Describe what you actually gave Claude as input and what you changed. -->

**Instance 1**

- *What I gave the AI:* The Chunking Strategy section from planning.md plus the raw rmp_gordon_arnold.txt file, and asked it to implement ingest.py with RMP boilerplate cleaning and review-aware chunking.
- *What it produced:* A working ingest.py that parsed review blocks, stripped noise lines, and prepended professor name and course code to each chunk.
- *What I changed or overrode:* After the first run, chunk 0 in every file was a junk header block containing the ratings summary and similar professors list. I directed a fix to skip any block that could not be assigned a course code. That guard was not in the original output.

**Instance 2**

- *What I gave the AI:* The grounding requirement from planning.md and asked it to implement query.py with a strict system prompt that answers only from retrieved context and refuses otherwise.
- *What it produced:* An initial SYSTEM_PROMPT with the grounding instruction and the refusal string.
- *What I changed or overrode:* After testing, the LLM was writing citation labels like Source 1, Source 3 inline in the answer body. I directed adding a new instruction telling the model not to include source numbers or citation labels in its answer, since sources are handled separately by the pipeline. The original output did not have that instruction.

---

## Demo Video

[YouTube](https://youtu.be/GGMKEXcAyXM)
