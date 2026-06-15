---
name: triam-thesis-academic-writing
description: Use when drafting, rewriting, auditing, or improving Vietnamese academic prose and citations for the TRIAM capstone thesis, especially files under _docs_capstone such as triam_co_so_ly_thuyet.tex, c4_c7_core.md, outlines, literature/background sections, theory chapters, implementation chapters, or LaTeX/BibTeX thesis text. Helps keep Chapter 3 concise and theoretical, later chapters implementation-focused, citations reliable, and claims aligned with source code and reputable references.
---

# TRIAM Thesis Academic Writing

## Operating Principles

Write as a Vietnamese capstone thesis assistant, not as a product marketer or tutorial writer.

Keep the thesis architecture in mind:

- Chapter 3, "Co so ly thuyet", is a short theory foundation. It should be broad, readable, and source-backed, about 20% of the thesis weight.
- Chapters 5-8 are the implementation-heavy chapters. Reserve code flow, database fields, constants, class names, and detailed algorithms for those chapters unless the user explicitly asks otherwise.
- Chapter 4 covers analysis/design. UML and architecture modeling usually fit there better than in the theory chapter.

When editing a section, preserve the user's thesis direction unless it conflicts with code or evidence. Improve clarity, academic tone, citation quality, and claim precision.

## Default Workflow

1. Read the target file and nearby outline files such as `_docs_capstone/c4_c7_core.md`.
2. Identify the chapter role: theory, overview, design, implementation, evaluation, or conclusion.
3. Decide the appropriate depth before rewriting.
4. For citation work, prefer reputable sources and verify current official docs when technology details may have changed.
5. Rewrite in Vietnamese academic prose with concise transitions.
6. Audit for overclaiming: do not state that TRIAM implements a method unless code or project docs support it.

## Theory Chapter Pattern

For Chapter 3 theory sections, use this compact structure:

1. Khai niem: define the concept in plain academic Vietnamese.
2. Nguyen ly chinh: explain the mechanism only as much as needed for later chapters.
3. Han che: state practical limitations or risks.
4. Lien he voi TRIAM: add one short paragraph explaining why this concept is relevant.

Avoid deep implementation in Chapter 3:

- Do not include table schemas, class names, endpoint names, exact config constants, worker internals, or long formulas unless they are core theory.
- Do not turn Chapter 3 into a duplicate of Chapters 5-8.
- Do not over-explain all tools equally. Give more space to LLM, RAG, embedding/search, voice realtime, document processing, and spaced repetition; keep framework/tool sections shorter.

## Prose Style

Use formal but natural Vietnamese:

- Prefer "hệ thống", "người học", "tài liệu học tập", "trợ lý học tập", "ngữ cảnh", "truy xuất", "lập chỉ mục", "ôn tập".
- Introduce English terms once with parentheses, then use the Vietnamese term consistently.
- Use paragraphs of 3-6 sentences. Avoid many one-sentence paragraphs.
- Prefer synthesis over listing. Use bullets only when they genuinely improve readability.
- Avoid promotional adjectives such as "mạnh mẽ", "hiện đại", "tối ưu tuyệt đối", "thông minh vượt trội".
- Avoid repeating "giúp" and "có thể" in every sentence.
- Use "trong phạm vi hệ thống TRIAM" when grounding a general concept in the project.

For detailed style examples and replacement patterns, read `references/style-guide.md`.

## Citation Discipline

Use citations to support claims, not to decorate every sentence.

For theory and research claims:

- Prefer original papers, survey papers, standards, and official documentation.
- Use blog posts only when no primary or official source exists, and say why.
- Do not invent DOI, page numbers, publication years, or BibTeX fields.
- If a citation key is not already available, propose a stable key such as `vaswani2017attention` and include enough source metadata for the user to add to `.bib`.

For implementation technologies:

- Use official docs for FastAPI, Flutter, Next.js, PostgreSQL, pgvector, Supabase, Celery, Firebase, WebRTC, LiveKit, OpenAI, Google Cloud TTS, and Tavily.
- Use papers/surveys for LLM, RAG, hallucination, information retrieval, and spaced repetition.

For the recommended source map and citation strategy, read `references/citation-guide.md`.

## TRIAM-Specific Claim Boundaries

Be strict about these distinctions:

- TRIAM uses RAG and hybrid retrieval in implementation chapters; Chapter 3 should explain the concepts only.
- TRIAM's current spaced review implementation uses fixed intervals after learning-unit completion, not full SM-2 adaptive scheduling. SM-2 may be presented as related theory or future enhancement, not as the implemented algorithm.
- TRIAM separates source document structure from learning units. In theory sections, describe this as a general design motivation; reserve `BookSection`, `LearningUnit`, and table details for implementation chapters unless requested.
- TRIAM's voice assistant combines realtime communication, model reasoning, transcript synchronization, and controlled web search. In theory sections, keep this to WebRTC/LiveKit/STT/TTS/realtime assistant foundations.

## LaTeX Guidelines

When editing `.tex`:

- Preserve the existing compiler assumptions: Vietnamese via `fontspec` and `polyglossia` unless the user asks to change the LaTeX stack.
- Use `\section`, `\subsection`, and `\subsubsection` consistently.
- Use `\cite{key}` or `\parencite{key}` only after checking the document's citation style. If no bibliography system exists, propose one before scattering citations.
- Escape special LaTeX characters in prose when needed: `_`, `%`, `&`, `#`.
- Keep formulas only when they clarify core theory, not as decoration.

## Useful References

- Read `references/style-guide.md` when rewriting prose, restructuring a chapter, or making the writing more academic.
- Read `references/citation-guide.md` when adding sources, checking citation quality, creating BibTeX suggestions, or deciding whether a claim needs a citation.
