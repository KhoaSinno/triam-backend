# Phase 33 Implementation Guide — Vietnamese Voice Transcription Reliability

Date: 2026-08-13  
Status: Phases 33.0 and 33.1 are implemented; Phases 33.2–33.4 remain proposed
Scope: make Vietnamese final transcripts, especially book titles, author names, chapter names, numbers, and English technical terms, more reliable before they reach voice grounding and RAG.

---

## 1. Decision

Keep the existing speech-to-speech voice architecture and the existing shared grounding path. Improve the **input transcription contract** in small, independently reversible stages.

```text
microphone
  -> LiveKit input audio / BVC noise cancellation
  -> OpenAI Realtime input noise reduction
  -> gpt-live-transcribe
  -> final transcript
  -> Realtime conversation item (audio remains available to the Realtime model)
  -> SharedAgentPolicy -> GroundingRouter -> tool/RAG
  -> grounded spoken response
```

The final transcript is not a replacement for the Realtime model's audio understanding. It is nevertheless a critical input for:

1. `search_book_knowledge` tool arguments;
2. `SharedAgentPolicy` and `GroundingRouter` intent resolution;
3. semantic/RAG retrieval;
4. query-guard and web-permission state;
5. user-visible saved transcript.

Therefore, an ASR error in a proper noun can make an otherwise capable voice model retrieve the wrong document. The fix belongs **before** retrieval, not in a hard-coded Vietnamese keyword correction layer after it.

### Why this design

- It preserves one `SharedAgentPolicy` / `GroundingRouter` path for voice and text.
- It does not inject a second user text message into the Realtime session.
- It does not turn off `VOICE_AGENT_ASR_FINAL_RESPONSE_GATE_ENABLED`; that gate fixes response ordering, not word recognition.
- It does not depend on an LLM guessing a misspelled book title after the retrieval query has already become wrong.
- Every behavioral change is isolated behind a default-off flag and has a direct rollback.

### What this phase cannot promise

No speech-to-text provider can guarantee perfect recognition for every microphone, accent, background condition, overlapping speech, or unknown name. This phase can establish that the configuration is sent correctly, remove a proven vocabulary-selection bug, and measure whether the error rate improves on representative Vietnamese audio. A rollout is accepted only if the measured data improves without degrading latency or correct existing turns.

---

## 2. Evidence and root causes

### 2.1 Current implementation

The current application configures:

```ini
OPENAI_REALTIME_TRANSCRIPTION_MODEL=gpt-live-transcribe
OPENAI_REALTIME_TRANSCRIPTION_LANGUAGE=vi
OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED=true
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_CHARS=900
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_TERMS=45
OPENAI_REALTIME_TRANSCRIPTION_PROMPT_MAX_SECTION_TERMS=20
OPENAI_REALTIME_INPUT_AUDIO_NOISE_REDUCTION=near_field
```

At startup, `agent_voice_gpt_realtime.py` builds one `AudioTranscription` object and passes `model`, singular `language`, and one free-text `prompt` to `RealtimeModel`. The dynamic prompt builder collects generic domain terms first and book/author/section terms later.

### 2.2 Proven implementation defect: relevant terms do not reach the prompt

`build_realtime_transcription_prompt()` can collect 45 terms, but `_build_prompt()` renders only `terms[:12]` as a synthetic Vietnamese greeting. The first terms are fixed generic words (`Tri Âm`, `chương`, `sách`, ...). Titles, authors, and sections are appended after them.

Result: the startup log may say `terms=45`, while many of the terms with the highest business value were never sent to OpenAI.

This is a real defect independent of model quality.

### 2.3 Provider-schema / SDK compatibility gap

The installed dependencies are currently pinned to:

```text
livekit-agents==1.5.17
livekit-plugins-openai==1.5.17
openai>=2.36,<3  (resolved locally as 2.41.0)
```

The installed `AudioTranscription` type exposes `model`, singular `language`, `prompt`, and `delay`; it does not expose `languages` or `keywords`.

Current OpenAI documentation for `gpt-live-transcribe` specifies:

- `languages` for expected input languages;
- `keywords` for literal names, acronyms, and product terms;
- `prompt` for the recording setting;
- `delay` as an explicit latency/accuracy control;
- do not send both `language` and `languages` for this model.

This means the current client abstraction cannot express the documented `gpt-live-transcribe` vocabulary contract. The current `language="vi"` is not proof that an equivalent model-specific language hint is accepted and applied by the remote service.

### 2.4 Missing observability

Current diagnostics log transcript character count and prompt character/term counts, but cannot prove these facts per session:

1. the remote session acknowledged the expected transcription model;
2. it received the expected language form;
3. it received a non-empty keyword list after an upgrade;
4. a final transcript was empty, partial, late, or materially different from the committed user item;
5. a title/author/section term was recognized accurately in controlled tests.

No raw transcript, prompt, keyword, tool argument, audio, or chunk content should be logged to solve this.

### 2.5 Official basis

OpenAI recommends `gpt-live-transcribe` for live transcript deltas/final transcripts. Its Realtime transcription guide specifies `prompt` for setting, `keywords` for literal terms, `languages` for expected languages, and uses `delay` to trade latency for accuracy. It further advises testing real microphones, accents, noise, code-switching, domain vocabulary, and long sessions rather than synthetic clean audio. [OpenAI Realtime transcription guide](https://developers.openai.com/api/docs/guides/realtime-transcription)

---

## 3. Boundaries and non-goals

### In scope

1. Session transcription configuration, vocabulary prioritisation, scalar-only diagnostics, tests, and controlled rollout.
2. Vietnamese plus English code-switching expected in this product.
3. Book titles, authors, chapter/section labels, common application terms, acronyms, and numbers in the evaluation set.
4. Dependency upgrade only when a compatibility test proves it is needed to represent the provider schema.

### Out of scope

1. Replacing OpenAI Realtime, changing `gpt-realtime-2.1-mini`, TTS voice selection, or the Flutter/LiveKit transport.
2. A post-ASR hard-coded dictionary that rewrites arbitrary user speech.
3. A second transcription request per normal voice turn.
4. Changing RAG chunk size, Cohere candidate count, evidence validation, database schema, or text-chat orchestration.
5. Re-enabling automatic Realtime responses before ASR final.
6. Automatically updating STT vocabulary every turn. In P0, scope vocabulary is built once at session start; a later state-driven update is conditional on Phase 30.4 evidence.

---

## 4. Target contract

### 4.1 P0 transcription configuration after dependency compatibility is available

```python
RealtimeTranscriptionConfig(
    model="gpt-live-transcribe",
    languages=("vi", "en"),
    prompt="Vietnamese voice conversation in the TRIAM audiobook study app. "
           "Users may mention book titles, author names, chapter names, "
           "numbers, and English technical terms.",
    keywords=(
        # highest-value current Study Context terms, ordered and bounded
        "exact book title",
        "author name",
        "chapter title",
    ),
    delay="medium",
)
```

`keywords` are only acoustic hints, never a forced rewrite. The resulting transcript is still user speech; an unrelated word must not be changed just because it resembles a title.

### 4.2 Vocabulary ranking policy

The builder must produce a structured result, not one synthetic dialogue string:

| Priority | Source | Default cap | Why |
|---|---|---:|---|
| 1 | Exact book titles in `GroundingScope.books` | 8 | Most valuable document disambiguator. |
| 2 | Authors and document aliases/types | 8 | Supports natural title/author queries. |
| 3 | Current scope section/chapter titles and path components | 12 | Supports chapter navigation and references. |
| 4 | Product/domain terms and acronyms | 12 | Supports mixed Vietnamese/English app terms. |
| 5 | Explicit safe extra terms from job metadata | 4 | Reserved for future product requirements. |

Terms are normalized, deduplicated case-insensitively, length-limited, and bounded by configuration. They retain scope order. The builder must never load RAG chunks or arbitrary document body text merely to make STT hints.

### 4.3 Stable prompt policy

The prompt is short and descriptive. It contains no fake dialogue, no long comma-separated vocabulary list, no raw context, and no instruction to force terms. The vocabulary belongs in `keywords` when the supported SDK permits it.

Before the SDK upgrade, the compatibility fallback may append a small **prioritized** term sample to the prompt only when the flag is on. It must be capped separately and clearly treated as a temporary compatibility path.

### 4.4 Delay policy

Start canary at `delay="medium"`, not `high` or `xhigh`.

- `medium` is the documented balance of latency and accuracy.
- The ASR-final gate already waits for final transcription, so P0 should measure final latency rather than optimize partial-caption speed.
- Increase to `high` only after data shows a material proper-noun gain that is worth the added end-of-turn latency.
- Do not use `minimal` or `low` for a retrieval-critical final transcript without an evaluation showing equal accuracy.

---

## 5. Delivery plan

Implement one subphase per PR/commit. Do not combine dependency upgrading, prompt behavior, audio preprocessing, and routing changes.

| Subphase | Change | Runtime risk | Default | Exit criterion |
|---|---|---:|---|---|
| 33.0 | Add scalar-only STT observability and a repeatable Vietnamese evaluation corpus | None | On for diagnostics only | Baseline has complete session/config/final timing data. |
| 33.1 | Fix vocabulary prioritisation and remove mock-dialogue prompt | Low | Flag off | High-value scoped terms are demonstrably included; no reply/routing behavior changes. |
| 33.2 | Upgrade compatible SDK/plugin and use `languages`, `keywords`, and `delay` | Medium | Flag off | Wire schema accepted and all focused compatibility tests pass. |
| 33.3 | Controlled canary for 33.1 + 33.2 | Medium | Off | Measured improvement versus baseline with no material latency/regression. |
| 33.4 | Optional one-variable noise-reduction A/B | Medium | Off | Select BVC + provider NR, BVC only, or provider NR only from recordings/evals. |

## 6. Phase 33.0 — observability and evaluation baseline

### Objective

Measure quality before changing it. The first change must not alter the provider request, the transcript, tool selection, RAG, session budget, or response gate.

### New scalar diagnostics

Extend `app/services/voice_agent/realtime_diagnostics.py` with a safe transcription session snapshot. It must parse acknowledgement metadata without retaining content:

```python
@dataclass(frozen=True)
class RealtimeTranscriptionSessionSnapshot:
    event_id: str | None
    model: str | None
    language_mode: Literal["language", "languages", "none", "unknown"]
    language_count: int | None
    keyword_count: int | None
    delay: str | None
    prompt_chars: int | None
```

Log a `VOICE_DIAG transcription_session_ack` record only with these scalar fields plus `thread_id`. Never log language values, keywords, prompt, transcript, audio, or provider raw event.

For each final transcript event, retain/add only:

```text
VOICE_DIAG transcription_final
  final=true | chars | language_present | provider_confidence_present
  final_to_response_request_ms | thread_id
```

If LiveKit exposes confidence, aggregate it only as a coarse safe band (`unknown`, `low`, `medium`, `high`) after confirming semantics; do not make a low-confidence transcript automatically block a user answer in P0.

### Evaluation corpus

Create a versioned, non-production test fixture with 30–50 short recordings or controlled live test scripts. It must include:

1. ordinary Vietnamese questions;
2. existing book titles and author names;
3. chapter/section labels and numbers;
4. Vietnamese with English technical terms (`GPT`, `RAG`, `C#`, `OpenAI`);
5. near/far microphone conditions and moderate background noise;
6. at least two natural Vietnamese speaking styles;
7. a few intentionally unclear utterances, whose expected product behavior is a clarification request, not forced correction.

Do not commit user audio, production transcripts, credentials, document body text, or private book titles without explicit authorization. If audio fixtures cannot be committed, commit the evaluation manifest and run recordings in a protected test location.

### Required measurements

For every corpus item, record outside production logs:

| Metric | Definition |
|---|---|
| Final transcript exact match | Exact normalized phrase match where appropriate. |
| Proper-noun recall | Expected title/author/chapter/term retained correctly. |
| Number accuracy | Expected chapter/document number is correct. |
| Retrieval target accuracy | Correct scoped book/section or correct context route selected. |
| Final-ASR latency | End-of-speech/commit to final transcript. |
| Answer start latency | Final transcript to first assistant audio. |
| Empty/truncated final rate | Separate from ordinary WER. |

The corpus is not merely a unit test. It is the acceptance oracle for all later canaries.

### Tests

- Unit test scalar event parser with `language`, `languages`, missing fields, and malformed provider events.
- Unit test ensures logs/snapshots never include raw prompt, term text, or transcript text.
- Unit test transcript timing correlation; partial transcript must not be counted as final.
- No existing voice behavior test is updated merely to accommodate diagnostics.

### Rollback

Remove or disable diagnostics only if operationally necessary. There is no behavioral rollback because 33.0 makes no behavioral change.

---

## 7. Phase 33.1 — fix vocabulary construction safely

### Objective

Fix the known `terms[:12]` defect without requiring a provider/SDK upgrade.

### Code shape

Refactor [transcription_prompt.py](../app/services/voice_agent/transcription_prompt.py) from a single string-only result to a content-safe structured build result:

```python
@dataclass(frozen=True)
class TranscriptionPromptBuildResult:
    prompt: str
    keyword_candidates: tuple[str, ...]
    prompt_term_count: int
    keyword_candidate_count: int
    prompt_chars: int
    dynamic_enabled: bool
```

Implementation requirements:

1. Replace `_base_domain_terms() -> tuple[str, ...]` + append ordering with category-aware collection.
2. Build prioritized candidates using the table in section 4.2.
3. Remove `_build_prompt()`'s mock greeting entirely.
4. Build one neutral setting description.
5. For the legacy fallback only, append the first N **prioritized** candidates after the setting description; N is a separate configuration limit, default `0` while rollout is off.
6. Never use a term as a hard correction rule after transcription.
7. Preserve existing normalization/length limits and enforce the provider prompt length cap before constructing `AudioTranscription`.

Example fallback prompt, if explicitly enabled:

```text
Vietnamese voice conversation in the TRIAM audiobook study app. Users may mix
Vietnamese and English technical terms. Expected names may include: <bounded
priority terms>.
```

The exact title list must not be logged.

### Flags and configuration

```ini
# Phase 33.1 — off by default; legacy SDK-compatible vocabulary prompt canary.
VOICE_AGENT_TRANSCRIPTION_CONTEXT_HINTS_ENABLED=false
VOICE_AGENT_TRANSCRIPTION_LEGACY_PROMPT_TERM_LIMIT=8
VOICE_AGENT_TRANSCRIPTION_PROMPT_MAX_CHARS=900
```

Existing `OPENAI_REALTIME_DYNAMIC_TRANSCRIPTION_PROMPT_ENABLED` remains the parent switch. Phase 33.1 must require both flags; turning either off reproduces the current base-prompt behavior.

### Why not immediately send all 45 terms in the prompt

Long lists are weaker cues than explicit keyword fields, consume the prompt length budget, and can bias recognition toward irrelevant documents in a multi-document context. The P0 goal is high-value scoped disambiguation, not vocabulary stuffing.

### Tests

- A multi-book scope test proves book titles appear before generic domain terms in candidates.
- A section-heavy scope test proves caps and scope order are respected.
- A test proves synthetic greeting text is absent.
- A test proves a disabled flag returns the exact old base prompt and no candidates.
- A test proves only counts/chars, never candidate text, enter diagnostics.

### Rollback

Set `VOICE_AGENT_TRANSCRIPTION_CONTEXT_HINTS_ENABLED=false` and restart the agent. No session/history/database migration is involved.

### Implementation record (2026-08-13)

Implemented as an SDK-legacy fallback only:

1. The existing collector and synthetic-dialogue prompt remain unchanged when `VOICE_AGENT_TRANSCRIPTION_CONTEXT_HINTS_ENABLED=false`.
2. With both the existing dynamic-prompt parent switch and the new flag enabled, the builder ranks title, author/document type, section/path, domain terms, then explicit extras.
3. The fallback sends only `VOICE_AGENT_TRANSCRIPTION_LEGACY_PROMPT_TERM_LIMIT` prioritized terms in a neutral `Expected names may include` sentence; the full candidate list is held only in memory for a later V2 keyword adapter and is never logged.
4. No transcript rewrite, shared policy, grounding, RAG, Realtime session schema, VAD, watchdog, or model behavior changed.

---

## 8. Phase 33.2 — make the SDK/provider contract explicit

### Objective

Upgrade the minimal compatible dependency set so the application can represent OpenAI's current `gpt-live-transcribe` fields: `languages`, `keywords`, and `delay`.

### Preflight: do not guess a version

Before changing `pyproject.toml`, create a disposable compatibility environment and verify all of the following against the candidate versions:

1. The OpenAI type exposes `gpt-live-transcribe` and `languages`, `keywords`, `prompt`, and `delay` together.
2. `livekit-plugins-openai` preserves those fields when building `session.update`; inspect serialized request in a local mocked transport.
3. The OpenAI provider accepts the session update for the actual project and returns a session acknowledgement.
4. LiveKit receives both partial and final events and preserves the user conversation item.
5. Semantic VAD with `create_response=False` remains intact when `VOICE_AGENT_ASR_FINAL_RESPONSE_GATE_ENABLED=true`.
6. Function tools, watchdog, remote session budget, interruption, text chat, and current focused tests remain compatible.

Do not widen version constraints to unbounded `>=` versions. Pin the verified `openai`, `livekit-agents`, and `livekit-plugins-openai` versions together in `pyproject.toml`/lockfile. Record the selected versions and the compatibility evidence in the implementation PR.

### New adapter boundary

Do not scatter provider-version conditionals through `agent_voice_gpt_realtime.py`. Add a small adapter, for example:

```text
app/services/voice_agent/realtime_transcription_config.py
```

Its responsibility is limited to:

```python
def build_realtime_transcription_options(
    *,
    settings: Settings,
    prompt_result: TranscriptionPromptBuildResult,
) -> RealtimeTranscriptionOptions:
    """Build the provider-compatible transcription payload.

    Validates bounded fields, selects the configured API schema, and exposes
    only safe summary metadata for diagnostics.
    """
```

`agent_voice_gpt_realtime.py` should call this adapter once during session construction. It must not know whether the provider object uses Pydantic, a dict, or a LiveKit wrapper.

### Configuration after verified upgrade

```ini
# Phase 33.2 — off by default until a successful controlled canary.
VOICE_AGENT_TRANSCRIPTION_SCHEMA_V2_ENABLED=false
OPENAI_REALTIME_TRANSCRIPTION_MODEL=gpt-live-transcribe
OPENAI_REALTIME_TRANSCRIPTION_LANGUAGES=vi,en
OPENAI_REALTIME_TRANSCRIPTION_DELAY=medium
VOICE_AGENT_TRANSCRIPTION_KEYWORD_LIMIT=24
```

Rules:

1. V2 sends `languages`; it must not send singular `language` too.
2. V2 sends the bounded candidate list as `keywords`.
3. Prompt stays neutral/short; it must not duplicate all keywords.
4. `delay` is configurable but validated against the provider-supported enum.
5. If a startup preflight shows the selected dependency cannot represent the enabled V2 schema, fail startup with a clear configuration error rather than silently falling back to a malformed request.

### Why upgrade instead of raw manual provider events

Manually sending undocumented events around LiveKit would create a second owner for session state and risks breaking VAD, remote context, tools, or event ordering. A compatible SDK/plugin pair preserves the single LiveKit session owner and gives typed validation.

### Tests

- Adapter unit tests snapshot serialized payloads for legacy and V2 schemas.
- V2 test asserts `languages=("vi", "en")`, no singular `language`, and bounded deduplicated keywords.
- Rejected unsupported configuration test has a clear error and no provider connection attempt.
- LiveKit/OpenAI integration smoke test validates acknowledgement and one audio final transcript.
- Existing voice regression suite: response gate, watchdog, session budget, transcript store, query guard, grounding router, and text agent tests.

### Rollback

1. Set `VOICE_AGENT_TRANSCRIPTION_SCHEMA_V2_ENABLED=false`.
2. Deploy the prior lockfile/version set only if the dependency change itself causes a regression.
3. Leave `VOICE_AGENT_ASR_FINAL_RESPONSE_GATE_ENABLED=true`; it is independent.

---

## 9. Phase 33.3 — controlled rollout and acceptance gate

### Canary order

1. **Baseline:** 33.0 only, all behavior flags off.
2. **Prompt canary:** enable 33.1 for one controlled test context; run the exact same corpus.
3. **Schema canary:** enable 33.2 only after dependency compatibility is green; run the same corpus.
4. **Combined canary:** enable 33.1 + 33.2 for the same context and repeat representative long sessions.
5. Expand gradually only after reviewing scalar logs and corpus results.

Do not run two versions in the same Realtime session. Flags are read at session startup; restart/reconnect for each arm.

### Acceptance criteria

The implementation is considered an improvement only when all are true:

1. Proper-noun recall improves against baseline on the corpus, with no decrease in ordinary Vietnamese question accuracy.
2. Number accuracy and retrieval-target accuracy do not regress.
3. Empty/truncated final-transcript rate does not increase.
4. Median final-ASR and answer-start latency stay within the product budget agreed before the test. Suggested initial guard: no more than 250 ms median and 500 ms p95 regression versus baseline.
5. No increase in `asr_final_response_gate_reply_error`, duplicate assistant commits, watchdog fires, Realtime errors, or rate-limit failures.
6. Session acknowledgement logs show the expected model/schema/delay and the expected non-zero keyword count for V2.
7. Voice and text still use the same `SharedAgentPolicy` / `GroundingRouter` semantics.

If an individual title improves while common Vietnamese questions worsen, the canary fails. Do not cherry-pick only favorable examples.

### Diagnostic review template

```text
run_id / commit / dependency versions / flags
corpus size / microphone profile / noise profile
proper-noun recall: baseline -> candidate
number accuracy: baseline -> candidate
retrieval target accuracy: baseline -> candidate
final-ASR p50/p95: baseline -> candidate
answer-start p50/p95: baseline -> candidate
empty/truncated finals: baseline -> candidate
provider/session errors: baseline -> candidate
decision: promote | hold | rollback
```

---

## 10. Phase 33.4 — optional audio-preprocessing experiment

### Problem

The current pipeline applies LiveKit BVC noise cancellation and OpenAI `near_field` input noise reduction. Neither is proven wrong, but two independent filters can sometimes remove noise beneficially or can soften short consonants/proper nouns depending on microphone conditions.

### Experiment

Run the same corpus through three mutually exclusive configurations:

| Arm | LiveKit BVC | OpenAI input NR |
|---|---:|---:|
| A: current | on | `near_field` |
| B | on | off |
| C | off | `near_field` |

Do not choose an arm based on subjective one-off listening. Compare the Phase 33 metrics and call quality. This must be a separate flag from vocabulary/schema flags:

```ini
VOICE_AGENT_INPUT_AUDIO_PREPROCESSING_PROFILE=current
```

Supported values should be validated exactly: `current`, `livekit_only`, `openai_only`. The default remains `current`.

### Rollback

Set the profile to `current` and restart. Never enable a fourth arm that applies additional filters without new evaluation evidence.

---

## 11. Cross-phase safety checklist

Before merge of each subphase, verify:

1. No hard-coded title/word match is added to route user intents.
2. No raw transcript, keyword, prompt, audio, RAG chunk, tool argument, or answer text is added to INFO logs.
3. Flags default to `false`; disabled behavior is covered by tests.
4. No DB migration, chat history rewrite, or Flutter protocol change is introduced.
5. The Realtime model retains audio input; no duplicate text user message is created.
6. The ASR-final gate stays semantically unchanged.
7. A provider upgrade is pinned and tested as a unit, not blended with routing/prompt rewrites.
8. Every new field sent to OpenAI is either acknowledged by a real canary or causes a visible startup/configuration failure.
9. Voice tool/RAG consumes a final transcript; partial deltas cannot trigger retrieval or response generation.
10. `AGENT_CONTEXT_OVERVIEW_ENABLED` behavior remains deterministic and unaffected.

---

## 12. File-level implementation map

| File | Phase | Intended change |
|---|---|---|
| `app/core/config.py` | 33.1–33.4 | Typed flags and bounded configuration values. |
| `.env.example` | 33.1–33.4 | Explain flags, defaults, schema compatibility, and rollback. |
| `app/services/voice_agent/transcription_prompt.py` | 33.1 | Prioritized structured vocabulary; no mock dialogue. |
| `app/services/voice_agent/realtime_transcription_config.py` | 33.2 | New provider schema adapter and safe summary. |
| `app/services/voice_agent/realtime_diagnostics.py` | 33.0/33.2 | Scalar-only acknowledgement and final timing parsing. |
| `app/services/agent_voice_gpt_realtime.py` | 33.0–33.2 | Wire builder/adapter once; emit safe diagnostics. |
| `tests/services/voice_agent/test_transcription_prompt.py` | 33.1 | Ordering, cap, disabled fallback, and privacy tests. |
| `tests/services/voice_agent/test_realtime_transcription_config.py` | 33.2 | Schema serialization/validation tests. |
| `tests/services/voice_agent/test_realtime_diagnostics.py` | 33.0/33.2 | Safe parser tests. |
| `pyproject.toml`, lockfile | 33.2 only | Pin only a verified compatible dependency set. |

---

## 13. Approval sequence

This document deliberately does not authorize implementation. Approve each item separately:

1. `Approve implement Phase 33.0 STT observability and evaluation baseline only.`
2. Review baseline data.
3. `Approve implement Phase 33.1 prioritized transcription prompt, feature flag default false.`
4. Test 33.1 canary and review logs/evaluation.
5. `Approve compatibility investigation for Phase 33.2; do not update production dependencies yet.`
6. Review selected versions and compatibility evidence.
7. `Approve implement Phase 33.2 transcription schema V2, feature flag default false.`
8. Run controlled canary; promote only when section 9 acceptance criteria pass.

The first recommended approval is Phase 33.0. It adds evidence without changing transcription, response generation, RAG, or user-visible voice behavior.
