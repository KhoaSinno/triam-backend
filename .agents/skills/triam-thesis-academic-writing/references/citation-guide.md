# TRIAM Thesis Citation Guide

## Source Hierarchy

Use the strongest available source for each claim:

1. Original peer-reviewed paper or widely cited preprint for theory.
2. Survey paper for broad state-of-the-art summaries.
3. Official standard/specification for protocols.
4. Official vendor/project documentation for implementation technologies.
5. High-quality technical articles only when primary sources are unavailable.

Do not rely on Wikipedia, marketing pages, random tutorials, or generated summaries for thesis claims.

## Citation Density

For Chapter 3, use citations sparingly but deliberately:

- 1-2 citations for a foundational concept.
- 1 citation for an official tool/framework description.
- 2-3 citations for areas with active research or known risk, such as RAG and hallucination.

Do not cite every sentence. Cite the paragraph or claim cluster.

## Recommended Source Map

### Generative AI, LLM, Transformer

- Vaswani et al., "Attention Is All You Need", 2017. Use for Transformer and attention.
- Zhao et al., "A Survey of Large Language Models", 2023. Use for LLM overview.
- Ji et al., "Survey of Hallucination in Natural Language Generation", 2023. Use for hallucination risk.

Suggested keys:

```bibtex
vaswani2017attention
zhao2023llmSurvey
ji2023hallucinationSurvey
```

### RAG and Retrieval

- Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", 2020. Use for original RAG framing.
- Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey", 2023/2024. Use for modern RAG variants and limitations.
- Chen et al., "Benchmarking Large Language Models in Retrieval-Augmented Generation", 2023. Use if discussing retrieval quality and faithfulness.

Suggested keys:

```bibtex
lewis2020rag
gao2023ragSurvey
chen2023rgb
```

### Embedding, Vector Search, Hybrid Search

- OpenAI Embeddings official documentation. Use for embedding model behavior and dimensions when discussing OpenAI models.
- PostgreSQL Full Text Search documentation. Use for lexical search.
- PostgreSQL pg_trgm documentation. Use for trigram similarity.
- pgvector official README/docs. Use for vector storage and indexing in PostgreSQL.

Suggested keys:

```bibtex
openaiEmbeddingsDocs
postgresFullTextSearchDocs
postgresPgTrgmDocs
pgvectorDocs
```

### Document Processing

- W3C EPUB 3.3 specification. Use for EPUB navigation/TOC.
- Microsoft Open XML / ECMA-376 references. Use for DOCX structure and heading styles if needed.
- PDF specification or library official docs. Use for PDF outline/bookmark concepts if discussed.

Suggested keys:

```bibtex
w3cEpub33
ecma376OpenXml
pdfSpec
```

### Realtime Voice, STT, TTS

- W3C WebRTC specification. Use for WebRTC fundamentals.
- LiveKit official documentation. Use for LiveKit rooms, SFU, agents, and realtime media concepts.
- OpenAI Realtime API official documentation. Use for realtime voice assistant capabilities.
- Google Cloud Text-to-Speech Chirp 3 HD documentation. Use for TTS provider background if discussing provider choice.

Suggested keys:

```bibtex
w3cWebrtc
livekitDocs
openaiRealtimeDocs
googleCloudTtsDocs
```

### Data, Security, and Background Jobs

- PostgreSQL official documentation. Use for relational database, ACID, indexing, full text.
- Supabase official docs. Use for Auth, Storage, and Row Level Security.
- Celery official docs. Use for distributed task queue/background processing.
- Redis official docs. Use for broker/cache role if needed.
- Firebase Cloud Messaging official docs. Use for push notification concepts.

Suggested keys:

```bibtex
postgresDocs
supabaseRlsDocs
supabaseAuthDocs
celeryDocs
redisDocs
firebaseMessagingDocs
```

### Spaced Repetition and Learning Science

- Ebbinghaus, "Memory: A Contribution to Experimental Psychology", 1885/1913 translation. Use for forgetting curve background.
- Cepeda et al., "Distributed practice in verbal recall tasks: A review and quantitative synthesis", 2006. Use for spacing effect evidence.
- SuperMemo SM-2 official algorithm page. Use only as a reference algorithm, not as implemented TRIAM behavior unless code changes.

Suggested keys:

```bibtex
ebbinghaus1885memory
cepeda2006distributedPractice
supermemoSm2
```

## TRIAM Claim Guardrails

Use this wording when implementation differs from full theory:

- "TRIAM vận dụng nguyên lý lặp lại ngắt quãng thông qua các mốc ôn tập cố định sau khi người học hoàn thành bài học."
- "SM-2 được trình bày như một thuật toán tham khảo phổ biến trong nhóm phương pháp spaced repetition, không phải mô tả trực tiếp thuật toán đang triển khai."
- "RAG trong chương cơ sở lý thuyết được trình bày ở mức nguyên lý; các biến thể như hybrid retrieval, reranking và evidence validation được phân tích sâu ở chương triển khai."

Avoid:

- "TRIAM sử dụng thuật toán SM-2" unless code actually implements quality score and ease factor.
- "RAG đảm bảo câu trả lời luôn đúng."
- "Web search luôn cung cấp thông tin chính xác."

## BibTeX Guidance

When adding citations:

1. Check whether the thesis already has a `.bib` file or `thebibliography`.
2. If none exists, recommend a single bibliography approach instead of mixing styles.
3. Prefer stable keys in lower camel case or author-year style.
4. Include URL and access date for official docs.
5. For papers, include title, author, year, venue if known, DOI/arXiv if verified.

Never fabricate missing fields. If a field is unknown, omit it or mark it for verification outside the final thesis text.
