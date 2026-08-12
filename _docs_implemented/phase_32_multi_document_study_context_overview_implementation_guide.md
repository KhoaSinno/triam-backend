# Phase 32 Implementation Guide — Multi-Document Study Context Overview (P0)

Date: 2026-08-12  
Status: Proposed; P0 only, not implemented  
Scope: deterministic questions about the current Study Context's document collection, shared by voice and text chat

---

## 1. Decision

Implement **Study Context Overview** before attempting multi-document RAG diversification.

This P0 answers factual questions about the collection selected in the current thread, for example:

- how many documents are in the current context;
- which documents are available;
- a concise overview of the documents currently available for study.

These are structured metadata questions. They must be answered from the loaded `GroundingScope`, never inferred from RAG chunks and never guessed by an LLM.

The change belongs inside the existing common boundary:

```text
voice search_book_knowledge / text search_book_knowledge_text
  -> SharedAgentPolicy
  -> GroundingRouter
  -> Context Overview route (new)
  -> deterministic result for voice or text
```

Voice and text must receive the same facts, while retaining their own presentation behavior (spoken concise response versus text rendering). No separate voice-only keyword logic is allowed.

---

## 2. Evidence and root cause

### 2.1 The full document scope does reach the agent

`get_token_for_thread()` loads every `StudyContextDocumentLink` for the thread's context and serializes them as `document_ids` in LiveKit job metadata. `load_grounding_scope(document_ids)` then loads all permitted books and their sections. A missing document ID is therefore not the primary cause of the incorrect answer.

### 2.2 Current routing only models one-book metadata

`GroundingIntent` currently covers metadata of a single book only:

```text
title, author, document type, section count, root-section count, status
```

There is no intent or route for collection-level facts such as document count/list.

For a metadata intent without an explicit book title, `resolve_metadata_book()` does this in a multi-book scope:

```text
scope.allowed_book_ids[0]
  -> primary_book_fallback
  -> metadata answer for only the first book
```

That branch explains answers that mention one "primary" document when the user actually asks about all documents in the current context. It is deterministic but semantically wrong for the request.

### 2.3 RAG cannot make aggregate metadata reliable

The hybrid search/RRF/Cohere pipeline is global across all selected documents. It may return chunks from only one document after reranking. It also returns content chunks, not an authoritative document count. Sending more chunks or raising `VOICE_AGENT_RAG_MAX_CHARS` cannot make a collection count correct and increases Realtime TPM pressure.

---

## 3. Boundaries

### In scope

1. Count and list the documents in the **current** `GroundingScope`.
2. Return selected document metadata only: title, optional author, optional document type, processing status, and count of top-level sections where available.
3. Use the same `GroundingRouter` and `SharedAgentPolicy` path for voice and text.
4. Add safe aggregate diagnostics and regression tests.

### Explicitly out of scope

1. RAG chunk selection, Cohere configuration, embedding/index schema, or evidence validation.
2. Automatic selection of a primary document for content questions.
3. Rolling Realtime sessions, context retention, watchdog behavior, or output caps.
4. New database tables, migrations, or changes to the Flutter/LiveKit metadata contract.
5. Context-level summaries derived from full book contents. `context_overview` means a metadata overview only, not a generated synthesis of every document.

---

## 4. Product contract

### 4.1 Deterministic response rules

| User intent | Required result | Example shape |
|---|---|---|
| Count documents | Exact count from `len(scope.books)` | “Ngữ cảnh học tập hiện có 3 tài liệu.” |
| List documents | All titles in scope order; author only when stored | “Gồm: Redis Cookbook; Clean Code; …” |
| Context overview | Count plus bounded per-document metadata | “Có 3 tài liệu. Redis Cookbook (PDF, …); …” |
| No document in scope | Direct truthful answer | “Tôi chưa tìm thấy tài liệu nào trong ngữ cảnh học tập hiện tại.” |

The scope order must remain the order of `document_ids` received from the thread metadata, which `get_grounding_scope()` already preserves. Do not sort titles alphabetically and do not select a primary book for these intents.

### 4.2 Response-size policy

Counts must always be complete. Lists and overviews must have a small explicit display policy:

```text
1–6 documents: show every title.
7+ documents: state exact count, show the first 6 titles in scope order,
             then say how many additional documents exist.
```

This is a UI/readability boundary, not a retrieval decision. The structured result must retain the exact full count even when the rendered text is shortened. The implementation must use a numeric renderer parameter, not a language-specific title-matching rule.

For voice, the deterministic text is passed through the current tool result and the Realtime model is instructed to read its factual answer naturally. It must not invent or omit documents. For text, return the deterministic answer directly; do not spend an LLM turn to paraphrase metadata.

### 4.3 Ambiguous wording

If the semantic classifier identifies a collection-level intent, answer the collection even when the user does not say “Study Context” verbatim. If the request simultaneously contains a uniquely identified book title and a per-book metadata request, preserve the existing one-book route.

If the classifier confidence does not reach its existing threshold, retain the existing semantic RAG fallback. Do not add `if query contains ...` or a Vietnamese/English keyword guard to force the context route.

---

## 5. Target design

### 5.1 Add explicit semantic intents and route

Extend `GroundingIntent`:

```python
CONTEXT_DOCUMENT_COUNT = "context.document_count"
CONTEXT_DOCUMENT_LIST = "context.document_list"
CONTEXT_OVERVIEW = "context.overview"
```

Extend `GroundingRoute`:

```python
CONTEXT_OVERVIEW = "context_overview"
```

Add multilingual paraphrase prototypes to the existing semantic intent classifier. These are model examples, not substring-routing rules. Include paraphrases for count, list, and overview in Vietnamese (with/without accents) and English. Keep all existing intent classifier thresholds and fallback behavior.

Examples of evaluation utterances, not hardcoded matching terms:

```text
"Trong ngữ cảnh hiện tại có mấy tài liệu?"
"Hãy cho tôi biết danh sách tài liệu đang học"
"Tổng quan các sách tôi đã chọn"
"How many documents are in this study context?"
```

### 5.2 Introduce a typed context-overview value

Create `app/services/agent_grounding/context_overview.py` rather than embedding collection formatting in the router.

```python
@dataclass(frozen=True)
class ContextOverview:
    document_count: int
    documents: tuple[GroundingBook, ...]


def build_context_overview(scope: GroundingScope) -> ContextOverview:
    return ContextOverview(
        document_count=len(scope.books),
        documents=scope.books,
    )
```

Add deterministic renderers in `response_renderer.py`:

```python
def render_context_document_count(overview: ContextOverview) -> str: ...
def render_context_document_list(overview: ContextOverview, *, max_visible_documents: int) -> str: ...
def render_context_overview(overview: ContextOverview, *, max_visible_documents: int) -> str: ...
```

The renderer owns wording and truncation. It must not query the database, call an LLM, access RAG chunks, or mutate session state.

### 5.3 Route before single-book metadata resolution

In `GroundingRouter.resolve()` add the context-level branch before `_resolve_metadata()`:

```python
elif intent in CONTEXT_OVERVIEW_INTENTS:
    result = self._resolve_context_overview(intent)
else:
    result = self._resolve_metadata(normalized, intent)
```

`_resolve_context_overview()` must:

1. Build its answer exclusively from `self.scope.books`.
2. Use `GroundingRoute.CONTEXT_OVERVIEW`.
3. Include **all** scope book IDs in `GroundingDecision.resolved_book_ids`.
4. Return a direct deterministic answer, including the zero-document case.
5. Never call `resolve_metadata_book()`, which would activate `primary_book_fallback`.

### 5.4 Carry the result through shared policy

Update `format_grounding_tool_result()` to emit a typed marker:

```text
STUDY_CONTEXT_FOUND:
<deterministic metadata answer>
```

Update `SharedAgentPolicy._from_grounding_result()` so `CONTEXT_OVERVIEW` returns:

```python
AgentPolicyResult(
    action=AgentPolicyAction.DIRECT_ANSWER,
    answer_source=AgentAnswerSource.CONTEXT_METADATA,
    reason_code="context_document_count" | "context_document_list" | "context_overview",
    user_message=grounding_result.deterministic_answer,
    tool_marker=format_grounding_tool_result(grounding_result),
    resolved_book_ids=all_scope_book_ids,
)
```

Add `AgentAnswerSource.CONTEXT_METADATA` rather than mislabeling a collection fact as one-book metadata. The text renderer already returns `user_message` directly for `DIRECT_ANSWER`; the voice renderer returns the tool marker. This preserves the shared policy architecture.

### 5.5 Update tool instructions, not hardcoded behavior

Clarify the descriptions/prompt instructions for the existing book-knowledge tool:

```text
Use this tool for questions about the current study context, including the documents available in it.
When the tool returns STUDY_CONTEXT_FOUND, relay its factual result and do not call RAG or web search.
```

Do not add another independently implemented voice tool for this P0. The current tool already reaches Shared Agent Policy and avoids another tool-choice surface for Realtime.

For text agentic mode, update `TEXT_AGENTIC_SYSTEM_INSTRUCTIONS` with the same tool-use rule. This prevents `gpt-4o-mini` from guessing a document count from conversational history while retaining its normal agentic flow for content questions.

---

## 6. Feature flag and configuration

Add one rollout flag, default off:

```python
AGENT_CONTEXT_OVERVIEW_ENABLED: bool = False
AGENT_CONTEXT_OVERVIEW_MAX_VISIBLE_DOCUMENTS: int = 6
```

Validation:

```text
1 <= AGENT_CONTEXT_OVERVIEW_MAX_VISIBLE_DOCUMENTS <= 12
```

Flag-off behavior must preserve current routing. Do not register collection intents in the active classifier path while disabled; otherwise an apparently disabled feature could silently change routing. The implementation may keep static prototype data in source, but `classify_intent()` must exclude context-overview intents from candidates unless the flag is enabled.

When the flag is on:

```text
context question -> semantic intent -> deterministic scope route
one-book metadata question -> existing metadata resolver
content/comparison question -> existing RAG route
```

Add the settings to `.env.example` with `false`. No production environment change is part of implementation.

---

## 7. Observability and privacy

The existing trace already records route, reason, answer source, and `resolved_book_ids`. Add scalar-only fields if needed:

```python
context_document_count: int | None = None
context_documents_rendered_count: int | None = None
```

Emit a safe event such as:

```text
AGENT_TRACE context_overview_resolved |
input_mode=voice|text |
intent=context.document_list |
document_count=3 |
rendered_document_count=3
```

Do not trace document titles, authors, user queries, tool arguments, LLM output, RAG chunk content, or the rendered overview. `resolved_book_ids` remain operational identifiers under the current trace policy.

Startup/config logs may include the boolean flag and numeric max-visible value only.

---

## 8. Required tests

### 8.1 Unit tests: typed overview and renderer

New test module: `tests/services/agent_grounding/test_context_overview.py`.

1. Empty scope produces count zero and a truthful no-document answer.
2. Three-book scope has exact count and retains scope order.
3. Optional metadata is omitted cleanly when absent; no literal `None` appears.
4. Seven-book scope reports seven but renders only six titles and an exact remainder.
5. Renderer is deterministic and never exposes IDs in user-facing text.

### 8.2 Router tests

Extend `tests/services/agent_grounding/test_grounding_router.py` with a multi-book fixture.

1. With flag on, each context intent routes to `CONTEXT_OVERVIEW` and does not invoke section loading or RAG.
2. `resolved_book_ids` contains every permitted book, in scope order.
3. A named single-book author/title question still routes to `BOOK_METADATA` and resolves only that book.
4. A content question still routes to `BOOK_RAG`.
5. With flag off, context-intent candidates are excluded and current routing behavior is preserved.

Mock `classify_intent()` at the router boundary to make the route tests deterministic; separately test classifier prototypes/flag filtering in `test_intent_router.py`.

### 8.3 Shared policy and rendering tests

Extend `tests/services/agent_policy/test_shared_policy.py`.

1. Text receives `DIRECT_ANSWER` with the same deterministic answer.
2. Voice receives one `STUDY_CONTEXT_FOUND` tool marker with the same facts.
3. Neither path invokes `search_book_context` or web permission.
4. Trace output contains counts and IDs only, never a title.

### 8.4 Agentic text integration tests

At the existing `search_book_knowledge_text` boundary, mock the tool call/result and verify:

1. The agentic loop can return a collection answer after one book-context tool call.
2. It does not make an additional web-search call.
3. A regular content query still follows the current RAG tool flow.

### 8.5 LiveKit metadata contract regression

Extend `tests/services/test_live_service.py`:

1. A thread linked to three documents creates a token metadata payload with exactly those three `document_ids`.
2. Their order is preserved into the loaded `GroundingScope` fixture.

---

## 9. Canary plan and acceptance criteria

### Canary

1. Deploy code with `AGENT_CONTEXT_OVERVIEW_ENABLED=false`.
2. Verify startup logs; no existing voice/text behavior changes.
3. Enable for one controlled multi-document test context containing 3–5 known documents.
4. Test voice and text separately, using a new Realtime room for voice to avoid unrelated TPM history.

### Test script

1. “Ngữ cảnh hiện tại có bao nhiêu tài liệu?”
2. “Liệt kê các tài liệu đang có.”
3. “Cho tôi tổng quan ngắn về các tài liệu đã chọn.”
4. “Tác giả của `<exact one title>` là ai?”
5. “Giải thích `<concept>` trong `<exact one title>`.”
6. “So sánh `<concept>` giữa các tài liệu này.” — record as baseline only; it remains P1, not a required P0 success.

### Pass criteria

1. Count equals the number of linked documents in database and matches the UI context count.
2. List includes every document when count is within the visible limit; otherwise count and omitted remainder are exact.
3. No answer falls back to the first/primary document for a recognized collection question.
4. Voice and text return the same factual collection result.
5. No RAG, Cohere, web, or provider quota call occurs for P0 metadata requests.
6. Existing single-book metadata and content questions pass unchanged.

### Rollback

```ini
AGENT_CONTEXT_OVERVIEW_ENABLED=false
```

Rollback only disables the new collection route. It does not affect document storage, existing RAG, text agentic mode, voice watchdog, or Realtime configuration.

---

## 10. Deferred P1 — Multi-document content synthesis

Do not implement this in Phase 32 P0.

For later work, content queries that explicitly ask for comparison, contrast, or synthesis across documents need a separate retrieval strategy:

1. keep global hybrid recall;
2. apply document diversity only for a classifier-detected multi-document content intent;
3. guarantee no more than a configured number of chunks per document before filling remaining budget by score;
4. add `Book: <title>` to every model-visible source chunk;
5. trace selected-document count and per-document chunk counts without logging text;
6. test single-book queries to ensure diversity logic does not dilute a focused answer.

P1 must not be disguised as a larger `VOICE_AGENT_RAG_MAX_CHARS` or `AGENT_RERANKER_TOP_N` value. That would increase token usage without guaranteeing source coverage.

---

## 11. Implementation order

1. Add contracts: intents, route, answer source, overview value type.
2. Build deterministic renderer and its unit tests.
3. Add feature-gated classifier candidates and router branch/tests.
4. Wire the route through `response_renderer`, `SharedAgentPolicy`, voice tool marker, and text direct rendering.
5. Add safe trace fields and regression tests.
6. Update `.env.example` and configuration validation.
7. Run isolated test suites, then canary with flag off followed by one controlled multi-document context.

Keep this phase to one focused PR/commit. Do not combine it with Realtime quota work, Phase 30 voice RAG budgeting, or P1 retrieval diversity.
