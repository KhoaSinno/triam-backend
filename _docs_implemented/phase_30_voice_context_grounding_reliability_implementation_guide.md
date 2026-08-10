# Phase 30 Implementation Guide — Voice Context Grounding Reliability

Date: 2026-08-10  
Status: Phase 30.0 implemented and runtime-reviewed; Phase 30.0.1 is the next P0; Phases 30.1–30.5 remain proposed
Scope: voice-only RAG budget, final-transcript safety gate, concise spoken responses, structured follow-up state, and section routing verification

---

## 1. Decision and boundaries

Keep the current architecture. Do not change model, Flutter/DataChannel contract, or text-chat orchestration in this phase.

```text
Realtime model
  -> search_book_knowledge tool
  -> TriamAssistant.resolve_book_query
  -> SharedAgentPolicy
  -> GroundingRouter (metadata / section / RAG / web policy)
  -> grounded model response
```

Code review confirms the shared policy is already the right boundary:

- `TriamAssistant._resolve_shared_policy()` sends `input_mode=VOICE` to `SharedAgentPolicy`.
- `SharedAgentPolicy._resolve_rag()` is the common RAG path for voice and text.
- `GroundingRouter._resolve_section()` already resolves section references and produces deterministic section context.
- `format_rag_context()` currently uses the one global `VOICE_AGENT_RAG_MAX_CHARS` budget.
- `AgentTurnTracer.has_final_transcript()` already exists, but the first book-search tool does not yet wait for it.

The phase improves the handoff into grounding. It must not fork routing logic between voice and text.

### Safety rules

1. Every behavior change has its own feature flag, defaulting to `false`.
2. With a flag off, the code follows today's voice path.
3. Never concatenate raw previous queries into every RAG query.
4. Never log transcript text, tool arguments, chunk content, web content, or generated answer content.
5. No database migration is allowed.
6. Existing generic `search_book_knowledge` remains available as fallback.

---

## 2. Findings that motivate Phase 30

| Finding | Current code | Meaning |
|---|---|---|
| Voice has a global RAG cap | `format_rag_context()` reads `VOICE_AGENT_RAG_MAX_CHARS` | Text-friendly context can be too broad for spoken answers. |
| 8 reranked chunks exist before formatting | `search_voice_book_context()` returns the ranked payload | Keep recall at 8 candidates but reduce only model-visible voice context. |
| Final ASR can arrive late | trace has `has_final_transcript()` and late-transcript correlation | A bounded wait can reduce timing risk; it must fail open. |
| Voice state is not grounding state | `VoiceTurnState` holds transcript/clarification only | Follow-up references are not represented as structured source IDs. |
| Section path already exists | `GroundingRouter._resolve_section()` | A new tool is conditional, not P0. |

Important correction: do not add a generic final-transcript wait inside confirmed `execute_web_search()`. That tool runs after an earlier permission turn and is protected by the existing watchdog. The ASR gate belongs only before the first book-grounding decision in `search_book_knowledge()`.

---

## 3. Delivery plan

| Subphase | Change | Risk | Exit criteria |
|---|---|---:|---|
| 30.0 | Add safe trace fields only | None | Baseline collected with all flags off |
| 30.0.1 | Bound Realtime output-token reservation | Low | Limit errors fall without reducing RAG context |
| 30.1 | Voice-only RAG budget | Low | Text output unchanged; voice budget enforced |
| 30.2 | Concise voice response profile | Low | Normal answers become shorter; detailed requests remain coherent |
| 30.3 | Bounded ASR-final gate | Medium | No silent/duplicate turn; timeout proceeds |
| 30.4 | Structured grounding state | Medium | State cannot leak across book/topic/TTL |
| 30.5 | Typed section tool | Conditional | Implement only if routing traces justify it |

Implement one subphase per PR/commit. Do not combine all phase flags in one change.

### Runtime review — 2026-08-10

The first Phase 30.0 production trace established the following:

- OpenAI Realtime emitted `rate_limit_exceeded` with error type `tokens` four times during the voice test.
- Before two failures, voice RAG rendered 6,907–8,015 content characters from 7–8 candidates. A rendered tool result remains in the live Realtime conversation, so several such turns compound session token load.
- A later web-permission turn also hit the same limit. Therefore RAG context is a major contributor, but not the sole direct trigger after the session budget is already depleted.
- The installed LiveKit OpenAI Realtime plugin defaults `max_response_output_tokens` to `inf`. OpenAI Realtime reserves output tokens when a response is created, so an explicit finite cap is a lower-risk first mitigation than dropping RAG chunks.
- Final ASR arrived after book-tool start in several normal turns (roughly 69–1,384 ms in the sampled traces). This supports Phase 30.3 later, but it is not the cause of the rate-limit incident.

One Phase 30.0 metric correction is required in the next deployment: only the first final transcript may update timing for a book tool. This prevents a later user utterance during a rate-limited/stuck turn from corrupting the original timing metric.

---

## 3.1 Phase 30.0.1 — Realtime Token-Reservation Cap (next P0)

This subphase does not reduce retrieved chunks or RAG characters. It limits the maximum output reservation for one Realtime response.

Add a feature-controlled setting:

```python
VOICE_AGENT_REALTIME_OUTPUT_TOKEN_CAP_ENABLED: bool = False
VOICE_AGENT_REALTIME_MAX_OUTPUT_TOKENS: int = 512
```

The installed `livekit.plugins.openai.realtime.RealtimeModel` supports this through `update_options`, not its constructor:

```python
model = RealtimeModel(...existing settings...)
if settings.VOICE_AGENT_REALTIME_OUTPUT_TOKEN_CAP_ENABLED:
    model.update_options(
        max_response_output_tokens=settings.VOICE_AGENT_REALTIME_MAX_OUTPUT_TOKENS,
    )
session = AgentSession(llm=model, ...)
```

Initial canary is 512 tokens. It is deliberately large enough for an explicitly requested detailed Vietnamese explanation, while avoiding the plugin's unlimited (`inf`) response reservation. Do not start at 128 or 256 because a hard output cutoff could stop a useful detailed answer prematurely.

Required tests:

1. Flag off does not call `update_options` and preserves current behavior.
2. Flag on calls `update_options(max_response_output_tokens=512)` before session start.
3. Invalid values outside OpenAI's accepted finite range fail config validation.
4. Realtime startup fallback behavior is unchanged.

Runtime test: after the provider token window resets, run the same 8–10 RAG-turn test. Compare `rate_limit_exceeded` count, response completion, and answer length against the 30.0 baseline.

Rollback:

```ini
VOICE_AGENT_REALTIME_OUTPUT_TOKEN_CAP_ENABLED=false
```

If rate limits continue after this cap, the OpenAI project/model token tier must be raised for the expected demo concurrency. Backend changes can reduce demand and provide a graceful error, but cannot create quota.

---

## 4. Configuration

Add to `app/core/config.py` and `.env.example`. Defaults preserve deployed behavior:

```python
# Phase 30 — Voice Context Grounding Reliability
VOICE_AGENT_VOICE_RAG_BUDGET_ENABLED: bool = False
VOICE_AGENT_VOICE_RAG_MAX_CHARS: int = 8000
VOICE_AGENT_VOICE_RAG_MAX_CHUNKS: int = 3

VOICE_AGENT_VOICE_CONCISE_REPLY_ENABLED: bool = False
VOICE_AGENT_VOICE_REPLY_TARGET_SENTENCES: int = 2

VOICE_AGENT_ASR_FINAL_GATE_ENABLED: bool = False
VOICE_AGENT_ASR_FINAL_GATE_WAIT_MS: int = 350

VOICE_AGENT_GROUNDING_CONTEXT_STATE_ENABLED: bool = False
VOICE_AGENT_GROUNDING_CONTEXT_STATE_TTL_SECONDS: int = 180

VOICE_AGENT_SECTION_TOOL_ENABLED: bool = False
```

Validation:

```text
VOICE_AGENT_VOICE_RAG_MAX_CHARS >= 1000
1 <= VOICE_AGENT_VOICE_RAG_MAX_CHUNKS <= 8
1 <= VOICE_AGENT_VOICE_REPLY_TARGET_SENTENCES <= 3
0 <= VOICE_AGENT_ASR_FINAL_GATE_WAIT_MS <= 750
30 <= VOICE_AGENT_GROUNDING_CONTEXT_STATE_TTL_SECONDS <= 900
```

Do not lower the existing global `VOICE_AGENT_RAG_MAX_CHARS` in this phase. It remains the text/default budget, so the newly-good agentic text chat is not accidentally weakened.

Recommended first canary after focused tests:

```ini
VOICE_AGENT_VOICE_RAG_BUDGET_ENABLED=true
VOICE_AGENT_VOICE_RAG_MAX_CHARS=8000
VOICE_AGENT_VOICE_RAG_MAX_CHUNKS=3
VOICE_AGENT_VOICE_CONCISE_REPLY_ENABLED=true
VOICE_AGENT_VOICE_REPLY_TARGET_SENTENCES=2

VOICE_AGENT_ASR_FINAL_GATE_ENABLED=false
VOICE_AGENT_GROUNDING_CONTEXT_STATE_ENABLED=false
VOICE_AGENT_SECTION_TOOL_ENABLED=false
```

---

## 5. Phase 30.0 — privacy-safe baseline

Files:

```text
app/services/agent_observability/contracts.py
app/services/agent_observability/turn_trace.py
tests/services/agent_observability/test_turn_trace.py
```

Phase 30.0 adds numeric/count/enum fields only:

```python
rag_candidate_count: int = 0
rag_context_selected_count: int = 0
rag_context_char_count: int = 0
rag_context_budget_mode: str | None = None  # default in Phase 30.0

asr_final_status_at_book_tool: str | None = None
asr_final_before_book_tool_ms: int | None = None
book_tool_before_asr_final_ms: int | None = None
```

The Phase 30.0 ASR status is observation, not a gate:

```text
final_seen | final_missing
```

Never add raw text to `AGENT_TRACE`.

`final_seen` means the final transcript had already been traced when `search_book_knowledge` began; `asr_final_before_book_tool_ms` is the gap. `final_missing` means it had not; if a final transcript later correlates to that trace, `book_tool_before_asr_final_ms` records the gap. Both fields being `null` means no comparable final event was correlated, not an agent failure.

The future gate outcome/status and grounding-context-state status are intentionally not logged in Phase 30.0, because neither behavior exists yet. They are added only with Phases 30.3 and 30.4.

Collect at least 20 known-book voice turns, covering metadata, explicit chapter, concept, ambiguous request, follow-up, web permission approval, and interruption. Save trace ID plus expected route only. Record baseline p50/p95 for retrieval, tool total, result-to-speech, total turn, answer chars, and retrieval result count.

---

## 6. Phase 30.1 — voice-only RAG budget

### Behavior

```text
Cohere/retriever: 8 ranked candidates
  -> text: existing global budget
  -> voice: first 2–3 ranked chunks, at most 8,000 content characters
```

Do not reduce retrieval candidates to 2–3. Candidate count preserves recall; rendered context controls model focus and audio verbosity.

### Files

```text
app/services/voice_agent/rag_context.py
app/services/agent_policy/shared_policy.py
app/services/agent_voice_gpt_realtime.py
tests/services/voice_agent/test_rag_context.py
tests/services/agent_policy/test_shared_policy.py
```

Create one policy object:

```python
@dataclass(frozen=True)
class RagContextBudget:
    max_chars: int
    max_chunks: int | None
    mode: str  # default | voice


def get_rag_context_budget(input_mode: AgentInputMode) -> RagContextBudget:
    if input_mode == AgentInputMode.VOICE and settings.VOICE_AGENT_VOICE_RAG_BUDGET_ENABLED:
        return RagContextBudget(
            max_chars=settings.VOICE_AGENT_VOICE_RAG_MAX_CHARS,
            max_chunks=settings.VOICE_AGENT_VOICE_RAG_MAX_CHUNKS,
            mode="voice",
        )
    return RagContextBudget(
        max_chars=settings.VOICE_AGENT_RAG_MAX_CHARS,
        max_chunks=None,
        mode="default",
    )
```

Make the formatter explicit and backward compatible:

```python
def format_rag_context(
    result: VoiceRagResult,
    *,
    budget: RagContextBudget | None = None,
) -> str:
    budget = budget or get_rag_context_budget(AgentInputMode.TEXT)
    selected = result.chunks[:budget.max_chunks] if budget.max_chunks else result.chunks
    # Reuse current remaining-character trim logic against selected.
```

Pass `get_rag_context_budget(request.input_mode)` from `SharedAgentPolicy._resolve_rag()`. Also pass the same mode-aware budget from the legacy `TriamAssistant._resolve_rag_context()` fallback. Do not use a hidden global conditional in only one path.

Initial selection is rank-and-budget only. Do not add score thresholds or resurrect evidence validation in this subphase.

Required tests:

1. Existing text fixture output remains unchanged.
2. Voice flag off remains byte-for-byte equivalent to current formatter output.
3. Voice flag on selects no more than configured chunks.
4. Voice content does not exceed its character budget.
5. Oversized first chunk is safely trimmed.
6. Shared and legacy RAG paths receive the same voice budget.
7. Trace reports candidate count, selected count, actual content chars, and mode.

Rollback:

```ini
VOICE_AGENT_VOICE_RAG_BUDGET_ENABLED=false
```

---

## 7. Phase 30.2 — concise spoken response

File: `app/services/agent_voice_gpt_realtime.py`.

This is an instruction profile, never a post-generation string cut. Cutting model output can produce broken Vietnamese speech.

```python
def build_voice_response_style_instruction() -> str:
    if not settings.VOICE_AGENT_VOICE_CONCISE_REPLY_ENABLED:
        return ""
    target = settings.VOICE_AGENT_VOICE_REPLY_TARGET_SENTENCES
    return (
        f"For a normal spoken answer, use at most {target} short Vietnamese sentences. "
        "Give the useful answer first, then ask whether the user wants more detail. "
        "Use a longer answer only when the user explicitly requests explanation, summary, comparison, or a list. "
        "Do not read Markdown headings, tables, source labels, or internal tool markers aloud."
    )
```

Append this only to realtime `TriamAssistant` instructions. Do not alter `lk.chat`, `_chat_with_agentic_loop()`, or text-chat prompts.

Manual checks:

- Author/title question normally takes one or two sentences.
- “Explain in detail” remains allowed to be longer.
- Chapter summary gives overview then offers continuation.
- User can interrupt a longer response without duplicate watchdog speech.

Monitor existing `assistant_char_count` and `turn_total`; do not make tests assert exact model wording.

Rollback:

```ini
VOICE_AGENT_VOICE_CONCISE_REPLY_ENABLED=false
```

---

## 8. Phase 30.3 — final-transcript gate

### Objective

A final transcript may be recorded shortly after the voice tool begins. The gate gives the turn a small time window to stabilize. It does **not** replace the model tool query with raw ASR text.

### Files

```text
app/services/agent_voice_gpt_realtime.py
app/services/agent_observability/contracts.py
app/services/agent_observability/turn_trace.py
tests/services/voice_agent/test_agent_voice_asr_final_gate.py
tests/services/agent_observability/test_turn_trace.py
```

Add a pure/testable async helper with injected sleep:

```python
async def wait_for_voice_final_transcript(
    tracer: AgentTurnTracer,
    *,
    enabled: bool,
    wait_ms: int,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> AsrFinalGateResult:
    if not enabled:
        return AsrFinalGateResult("disabled", 0)
    if not tracer.has_active_turn(AgentInputMode.VOICE):
        return AsrFinalGateResult("no_active_voice_turn", 0)
    if tracer.has_final_transcript(AgentInputMode.VOICE):
        return AsrFinalGateResult("already_final", 0)

    # Poll until configured deadline.
    # If final arrives: wait_satisfied.
    # Deadline: timeout_fail_open. Never block or reject the tool.
```

Call it once at the entry of the realtime `search_book_knowledge()` tool before `resolve_book_query()`. Do not put it in generic `resolve_book_query()`, which also serves non-voice/fallback paths. Do not call it in permission-confirmed `execute_web_search()`.

Rollout:

1. Ship helper/trace with flag off.
2. Run observe-only analysis to see whether final commonly arrives inside 350 ms.
3. Enable at 250–350 ms with fail-open timeout.
4. Compare first-speech latency to Phase 30.0 baseline.

Required tests:

1. Disabled and final-already-present do not sleep.
2. Final arriving during the window proceeds with `wait_satisfied`.
3. No final proceeds with `timeout_fail_open`.
4. No active voice turn does not wait.
5. Text chat never calls gate.
6. Confirmed web-search execution never calls gate.
7. Timeout never creates clarification, error, second tool call, or duplicate reply.

Rollback:

```ini
VOICE_AGENT_ASR_FINAL_GATE_ENABLED=false
```

---

## 9. Phase 30.4 — structured grounding context state

Do not solve follow-up context by increasing `VOICE_AGENT_HISTORY_LIMIT` or appending old text to new RAG queries. That creates topic leakage and makes retrieval untestable.

Create:

```text
app/services/voice_agent/grounding_context_state.py
tests/services/voice_agent/test_grounding_context_state.py
```

State contains IDs only:

```python
@dataclass(frozen=True)
class VoiceGroundingContextSnapshot:
    document_ids: tuple[str, ...]
    source: AgentAnswerSource
    resolved_book_ids: tuple[str, ...]
    resolved_section_ids: tuple[str, ...]
    retrieval_chunk_ids: tuple[str, ...]
    created_monotonic: float


class VoiceGroundingContextState:
    def remember_success(self, result: AgentPolicyResult) -> None: ...
    def active(self, *, document_ids: list[str], ttl_seconds: float) -> VoiceGroundingContextSnapshot | None: ...
    def clear(self) -> None: ...
```

Rules:

- Remember only successful `BOOK_METADATA`, `BOOK_SECTION`, or `BOOK_RAG` results with IDs.
- Clear on document change, expiration, clarification, error, web result, or fresh scope.
- Never store answer text, user query, transcript, chunk content, or web content.
- Instantiate once per realtime session; never process-global.

State does not automatically narrow any search. Once it is stable, expose intent explicitly through the generic tool schema:

```python
@function_tool
async def search_book_knowledge(
    self,
    query: Annotated[str, "A complete, resolved book question"],
    scope: Annotated[
        Literal["book", "active_section"],
        "Use active_section only when continuing the most recently grounded section; otherwise use book.",
    ] = "book",
) -> str:
    ...
```

`scope=active_section` may use the state only when it is fresh and contains section IDs. Missing/stale state falls back to normal book RAG and records the status. It must never infer section scope from a keyword or silently apply stale state.

Before adding retrieval filtering, inspect `rag_service.search_book_knowledge` for an efficient optional `section_ids` filter. If the storage layer cannot filter, do not load all section content into a prompt as a workaround.

Tests:

1. Successful section/RAG/metadata state stores IDs only.
2. Error, web, and clarification clear state.
3. TTL and document mismatch invalidate state.
4. `scope=active_section` without valid state falls back to normal book search.
5. `scope=book` never uses old section state.
6. Text chat cannot mutate/read voice session state.

Rollback:

```ini
VOICE_AGENT_GROUNDING_CONTEXT_STATE_ENABLED=false
```

---

## 10. Phase 30.5 — typed section tool, only after evidence

The generic tool already reaches the section resolver through `GroundingRouter`. A separate tool is justified only if traces from at least 20 clear section questions show material failure: for example, explicit chapter requests frequently route to `BOOK_RAG` with zero/weak retrieval after final ASR and query guard are healthy.

If the gate passes, add:

```python
@function_tool
async def get_book_section_context(
    self,
    section_reference: Annotated[str, "Chapter number/path or section title resolved from the request."],
    request: Annotated[str, "Summary, explanation, or detail requested for this section."],
) -> str:
    ...
```

Requirements:

- Reuse `parse_section_reference`, `resolve_section`, and section-context construction through a public policy method.
- Do not call `GroundingRouter._resolve_section` directly or duplicate its parser.
- Ambiguous section returns existing clarification marker, not whole-book RAG.
- Generic semantic questions remain on `search_book_knowledge`.
- Feature flag off means Realtime does not see the tool.

Tests: numeric reference, title reference, ambiguous reference, generic concept, feature-off tool visibility.

---

## 11. Mandatory review checklist

For every PR:

```text
[ ] Restricted to AgentInputMode.VOICE where intended?
[ ] Old behavior exactly preserved with flag off?
[ ] Timeout/exception/stale-state fallback cannot produce silence?
[ ] No duplicate tool call or speech?
[ ] No raw content added to normal logs or AGENT_TRACE?
[ ] SharedAgentPolicy remains the common routing layer?
[ ] Text-chat tests prove no behavior regression?
[ ] New tests are deterministic and do not require LiveKit/OpenAI network timing?
```

Commands after each subphase:

```powershell
uv run ruff check app/core/config.py app/services/agent_voice_gpt_realtime.py app/services/voice_agent app/services/agent_policy app/services/agent_observability tests/services/voice_agent tests/services/agent_policy tests/services/agent_observability

uv run pytest tests/services/voice_agent/test_rag_context.py tests/services/voice_agent/test_turn_state.py tests/services/voice_agent/test_agent_voice_query_guard.py tests/services/agent_policy/test_shared_policy.py tests/services/agent_observability/test_turn_trace.py -q
```

Before canary:

```powershell
uv run pytest tests/services/voice_agent tests/services/agent_policy tests/services/agent_grounding tests/services/agent_observability -q
uv run pytest tests -q --maxfail=1 --durations=20
```

Manual test records only trace ID, expected route, speech started, watchdog fired/not fired, and duplicate speech yes/no.

---

## 12. Release gates and independent rollback

Functional gates:

- No silence after successful user-facing RAG/web tool result.
- No duplicate answer in five consecutive runs of each golden voice scenario.
- Text mode preserves current orchestration and global RAG budget.
- Clear section request reaches `BOOK_SECTION` whenever resolver can identify it.
- RAG miss produces clarification/established policy, never fabricated book fact.
- No raw content is present in logs.

Performance gates:

- Voice RAG budget reduces rendered context characters when enabled.
- p95 tool-result-to-speech does not regress from Phase 30.0 baseline.
- ASR gate adds no more than its configured wait and fails open.
- Concise mode reduces median answer chars for simple questions without raising clarification rate.

| Symptom | Disable only this flag |
|---|---|
| Missing useful detail | `VOICE_AGENT_VOICE_RAG_BUDGET_ENABLED=false` |
| Answer too terse | `VOICE_AGENT_VOICE_CONCISE_REPLY_ENABLED=false` |
| Added latency/timing instability | `VOICE_AGENT_ASR_FINAL_GATE_ENABLED=false` |
| Wrong follow-up topic | `VOICE_AGENT_GROUNDING_CONTEXT_STATE_ENABLED=false` |
| Wrong section-tool selection | `VOICE_AGENT_SECTION_TOOL_ENABLED=false` |

No subphase requires DB rollback, model replacement, cache wipe, or Flutter deployment.

---

## 13. Explicit non-goals

This phase does not replace `gpt-realtime-2.1-mini`, raise reasoning effort, re-enable old evidence validation, reduce Cohere candidate count from 8, modify watchdog behavior, or introduce keyword-based routing.

Only evaluate model/reasoning changes after deterministic grounding and turn-boundary metrics show they are the limiting factor.
