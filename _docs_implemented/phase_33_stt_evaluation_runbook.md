# Phase 33.0 — Vietnamese STT Baseline Evaluation Runbook

Date: 2026-08-13  
Status: Ready for controlled baseline collection  
Privacy: do not attach production audio, user transcripts, book content, prompts, keywords, tool arguments, or credentials to this document or server logs.

---

## Goal

Collect a reproducible baseline before enabling Phase 33.1 or 33.2. This runbook does not change voice behavior. It uses the current production STT configuration and records only aggregate outcomes outside server logs.

The OpenAI Realtime transcription guide recommends testing representative microphones, accents, noise, code-switching, domain vocabulary, numbers, and long sessions, while tracking empty, truncated, and delayed final transcripts separately from general transcription accuracy. [OpenAI Realtime transcription guide](https://developers.openai.com/api/docs/guides/realtime-transcription)

## Required server evidence

Restart one agent session and confirm these safe records appear:

```text
VOICE_DIAG transcription_session_requested
VOICE_DIAG realtime_session_updated
VOICE_DIAG transcription_final
```

When `VOICE_AGENT_ASR_FINAL_RESPONSE_GATE_ENABLED=true`, also confirm:

```text
VOICE_DIAG asr_final_response_gate_final_received
VOICE_DIAG asr_final_response_gate_reply_requested
```

Only record scalar values such as model, language mode/count, keyword count, prompt character count, final `item_id`, transcript character count, and timing. Do not enable raw transcript logging for this evaluation.

## Test matrix

Use a protected local worksheet or test database to resolve placeholders to the current Study Context. Keep the result sheet private.

| ID range | Category | Required examples | Expected measurement |
|---|---|---|---|
| V01–V08 | Ordinary Vietnamese | direct factual and explanatory questions | Final transcript correctness; answer starts. |
| V09–V14 | Book metadata | `<BOOK_TITLE_A>`, `<AUTHOR_A>`, document count/list | Proper-noun recall; correct metadata/context route. |
| V15–V20 | Section navigation | `chương <N>`, `<SECTION_TITLE_A>`, nested section reference | Number accuracy; correct section/book target. |
| V21–V26 | Code-switching | GPT, RAG, OpenAI, Gemini, C#, English book title | Term recall; retrieval target accuracy. |
| V27–V30 | Acoustic variation | near mic, normal mic, moderate ambient noise, slower speech | Empty/truncated final rate; final-ASR latency. |
| V31–V34 | Conversation state | two follow-ups and one long session | Final ordering; no duplicate response; target preservation. |
| V35–V38 | Unclear input | clipped/ambiguous speech and intentional pause | Clarification behavior; no forced incorrect grounding. |

For every book-title case, test the title spoken naturally, not by reading character-by-character. For number cases, include both a standalone number and a number embedded in a question.

## Per-run result sheet

Record this outside application logs:

```text
run_id:
commit:
environment:
realtime model / transcription model:
flags: ASR gate / context budget / dynamic prompt:
microphone and noise profile:

case_id:
expected final meaning:
final transcript correct: yes | no | partial
proper noun correct: yes | no | not-applicable
number correct: yes | no | not-applicable
grounding target correct: yes | no | not-applicable
final-ASR latency ms:
answer-start latency ms:
empty/truncated final: yes | no
duplicate response / interruption / provider error: yes | no
notes:
```

## Baseline summary

Do not compare individual anecdotes. Aggregate at least the complete V01–V38 run:

| Metric | Formula |
|---|---|
| Proper-noun recall | correctly recognized title/author/section/technical terms divided by applicable cases |
| Number accuracy | correct expected numbers divided by applicable cases |
| Grounding-target accuracy | correct book/section/context route divided by applicable cases |
| Empty/truncated rate | empty or truncated finals divided by all voice cases |
| Final-ASR latency | median and p95 from final event timing |
| Answer-start latency | median and p95 from final event to first assistant audio |

The baseline is sufficient to approve Phase 33.1 only when the session request/acknowledgement and final-transcript diagnostics are present for the complete run. It is not evidence to change provider configuration yet.
