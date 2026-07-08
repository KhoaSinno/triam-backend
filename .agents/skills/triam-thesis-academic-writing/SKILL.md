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

- **Source Code as Ground Truth**: The actual backend codebase is the single source of truth. Since implementation code may have evolved after the thesis draft or specifications were written, the agent MUST search and read the active python code (models, services, workers, repositories, etc.) in the workspace before writing or updating any technical chapter. Ensure that the database structures, algorithms, parameters, function names, and workflows described in the thesis align exactly with the current source code.

## Default Workflow

1. Read the target file and nearby outline files such as `_docs_capstone/c4_c7_core.md`.
2. Identify the chapter role: theory, overview, design, implementation, evaluation, or conclusion.
3. **Cross-reference Source Code**: Before writing any implementation-related content, identify the relevant Python files/directories in `app/` and inspect them to confirm the current implementation details.
4. Decide the appropriate depth before rewriting.
5. For citation work, prefer reputable sources and verify current official docs when technology details may have changed.
6. Rewrite in Vietnamese academic prose with concise transitions.
7. Audit for overclaiming: do not state that the system implements a method unless code or project docs support it.

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

Use formal, concise, and easy-to-understand Vietnamese in an academic research tone:

- **Simplicity and Clarity**: 
  - Write concisely and to the point. Avoid exclamations and conversational/emotional filler.
  - Avoid overly complex translation-style words like "hoạch định" (use "lập kế hoạch" instead).
  - Use the word "hệ thống" instead of repeating "hệ thống TRIAM".
- **Handling English & Abbreviations**:
  - Keep common English keywords/abbreviations as is (e.g., "Hybrid search", "RAG", "LLM", "Cross-Encoder", "WebRTC", "TTS", "STT"). Do not try to translate them or explain them in parentheses unless they are introduced for the first time.
  - For new abbreviations, add them directly to the list in `noidung/kihieu.tex` rather than writing inline parenthetical notes.
- **Avoid Redundant Explanations**: 
  - Limit parenthetical translations or annotations such as `(race conditions)`, `(commit)`. Avoid redundant, repetitive words.
- **Structure**:
  - Use paragraphs of 3-6 sentences. Avoid one-sentence paragraphs.
  - Prefer synthesis over bullet lists. Use bullets only when they improve readability of dense items.
  - Avoid promotional adjectives (e.g., "mạnh mẽ", "hiện đại", "tối ưu tuyệt đối", "thông minh vượt trội").
  - Avoid repeating "giúp" and "có thể" in every sentence.

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

When editing or drafting `.tex` files:

- **Compiler & Styling Assumptions**: 
  - Standard font size is 13pt (`\changefontsizes{13pt}` via `scrextend`).
  - Standard font is Times New Roman or TeX Gyre Termes.
  - Document supports both pdfTeX (using `\usepackage[utf8]{vietnam}`) and XeTeX/LuaTeX (using `\setmainfont` to load `times.ttf` from `tmp/fonts/`).
  - Line spacing is 1.2 (`\setstretch{1.2}`), paragraph skip is 6pt (`\setlength\parskip{6pt}`), and margins are `top=2cm, bottom=2cm, left=3cm, right=2cm`.
- **Chapter & Title Formats**:
  - The thesis has exactly 10 chapters.
  - Use uppercase centered titles for chapters (`\chapter{...}`).
  - Use uppercase bold for sections (`\section{...}`).
  - Use bold normal case for subsections (`\subsection{...}`).
  - Use bold italic for subsubsections (`\subsubsection{...}`).
- **Table and Figure Captions**:
  - Always use the strict position specifier `[H]` for both figures and tables (`\begin{figure}[H]` and `\begin{table}[H]`).
  - Always declare `\centering` right after `\begin{figure}[H]` or `\begin{table}[H]`.
  - **Tables**: Place the caption at the TOP of the table (inside `\begin{table}[H]` and before the `tabular` environment). Table caption style is `normalsize, bf, raggedright`. Label should be `\label{tab:tablename}`.
  - **Figures**: Place the caption and label at the BOTTOM of the figure (inside `\begin{figure}[H]` and after the graphic). Figure caption style is `normalsize, bf, centering`. Label should be `\label{fig:figurename}`. Specify graphic widths as a fraction of text width, e.g., `[width=0.95\textwidth]`.
- **English & Math Formatting inside LaTeX**:
  - Format conceptual English terms using `\textit{English term}` (e.g., `\textit{spaced repetition}`, `\textit{flashcard}`, `\textit{idempotency key}`).
  - Format code entities, model identifiers, folder paths, parameters, or configurations using `\texttt{name}` (e.g., `\texttt{gpt-4o-mini}`, `\texttt{Heading Styles}`, `\texttt{app/main.py}`).
  - Format all variables and formulas in math mode (e.g., `$q$`, `$d$`, `$Doc$`, `$Size$`, or `\[ ... \]`).
- **Algorithms (Pseudo-code)**:
  - Must use the `algorithm2e` package within the `\begin{algorithm}[H]` environment.
  - Declare parameters with `\KwData{...}` and `\KwResult{...}` at the top.
  - Enclose the algorithm logic in `\Begin{...}`.
  - Terminate all pseudo-code instructions with `\;`.
  - Use `\tcp{...}` for inline/block comments.
  - Include font scaling macros inside/before the algorithm: `\SetAlFnt{\scriptsize}`, `\SetAlCapFnt{\small}`, `\SetAlCapNameFnt{\small}`.
- **Cross-Referencing & Labels**:
  - Chapters: `\label{chap:chaptername}`, referred to as `Chương \ref{chap:chaptername}`.
  - Sections: `\label{sec:sectionname}`, referred to as `Mục \ref{sec:sectionname}`.
  - Figures: `\label{fig:figurename}`, referred to as `Hình \ref{fig:figurename}`.
  - Tables: `\label{tab:tablename}`, referred to as `Bảng \ref{tab:tablename}`.
  - Algorithms: `\label{alg:algname}`, referred to as `Giải thuật \ref{alg:algname}` or `Thuật toán \ref{alg:algname}`.
- **Citations & Bibliography**:
  - Citations use the `vancouver` style (`\bibliographystyle{vancouver}`).
  - Use `\cite{key}` for citation. Refer to keys defined in `noidung/tailieuthamkhao.bib`.
  - Escape special LaTeX characters (like `_`, `%`, `&`, `#`) in prose.

## Useful References

- Read `references/style-guide.md` when rewriting prose, restructuring a chapter, or making the writing more academic.
- Read `references/citation-guide.md` when adding sources, checking citation quality, creating BibTeX suggestions, or deciding whether a claim needs a citation.
