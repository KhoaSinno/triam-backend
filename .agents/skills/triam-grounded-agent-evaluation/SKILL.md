---
name: triam-grounded-agent-evaluation
description: Project-specific rules for evaluating, debugging, refactoring, or optimizing Triam book-grounded chat, LiveKit realtime voice, STT behavior, RAG retrieval, section routing, web-search permission, prompts, and model choices. Use whenever work touches agent accuracy, hallucination, wrong-book/wrong-section answers, voice-versus-text differences, retrieval quality, agent traces, evaluation datasets, or agent model upgrades.
---

# Triam Grounded Agent Evaluation

Use this skill to prevent speculative fixes and preserve grounded behavior across typed chat and realtime voice.

## Required Reading

Read only the documents relevant to the current task:

- Overall direction: `_docs_implemented/phase_10_grounded_book_agent_voice_accuracy_roadmap.md`
- Baseline and trace: `_docs_implemented/phase_10_0_agent_evaluation_baseline_trace_implementation_guide.md`
- Realtime architecture: `_docs_implemented/phase_7_realtime_voice_agent_stabilization_implementation_guide.md`
- Document structure: `_docs_implemented/phase_5_document_structure_tree_learning_unit_planner_implementation_guide.md`

## Mandatory Workflow

1. Reproduce or inspect the failure before editing.
2. Capture the final transcript, selected source, retrieval IDs/scores, tool flow, and committed answer when available.
3. Classify the primary failure layer:
   - input/STT;
   - ambiguity;
   - intent or section routing;
   - index coverage;
   - retrieval relevance;
   - context validation;
   - answer grounding;
   - web permission;
   - persistence;
   - FE reconciliation;
   - infrastructure latency.
4. Establish or update a regression case before changing behavior.
5. Apply the smallest change at the layer that owns the failure.
6. Run the same case through typed chat and voice when the change affects shared behavior.
7. Report accuracy, source selection, latency, cost, and remaining trade-offs.

## Grounding Rules

- Treat `BookSection` source content as the canonical book knowledge target; do not assume Full or Pareto learning units are canonical.
- Route deterministic metadata questions to database metadata, not vector search.
- Resolve explicit chapter/section questions before semantic retrieval.
- Treat non-empty retrieval output as insufficient evidence by itself; validate relevance and source.
- Do not answer book questions from model memory when grounded context is required.
- Ask a short clarification when voice input is ambiguous or missing critical information.
- Preserve web-search permission policy. Never search automatically because book retrieval is weak.
- Do not upgrade or blame the model before proving retrieval and context are correct.

## Voice Rules

- Realtime final transcripts may arrive after the response. Do not diagnose delay as missed audio without event evidence.
- Do not use transcript text or arrival time as the only turn correlation key.
- Use committed conversation events and stable SDK item IDs when available.
- Use final transcripts for persistence and evaluation; do not persist interim transcripts.
- Compare semantic intent preservation, not exact transcript wording alone.

## Evaluation Rules

- Keep unit tests deterministic and offline.
- Keep real LiveKit/provider/server tests in manual integration scripts, outside default pytest execution.
- Maintain golden cases for metadata, section lookup, semantic retrieval, unavailable content, ambiguous voice, and web permission.
- Prefer deterministic graders: expected source, expected section, required facts, forbidden facts, and permission behavior.
- Use model-based grading only as an additional signal.
- Record a baseline before prompt, retrieval, STT, or model changes.
- Add a regression case for every verified production bug.

## Trace And Logging Rules

- Log trace IDs, stages, source, tool names, IDs, counts, rounded scores, latency, and error codes.
- Do not log access tokens, headers, raw audio, embeddings, full transcripts, full answers, full chunks, or full web results.
- Keep text preview disabled by default and local-only.
- A tracing failure must never break the user-facing agent flow.

## Change Boundaries

- Preserve `lk.chat`, `lk.transcript`, and `lk.control` contracts unless a separately approved FE migration exists.
- Avoid mixing evaluation instrumentation with behavior changes in the same phase or diff.
- Do not hard-code fixes for one book, author, chapter, language phrase, or test fixture.
- Use feature flags and rollback paths for retrieval or model changes.

## Verification

At minimum, run focused checks for changed files:

```powershell
uv run pytest tests/services/voice_agent tests/services/agent_observability -q
uv run ruff check app/services/voice_agent app/services/agent_observability app/services/rag_service.py app/services/agent_voice_gpt_realtime.py
```

For real chat/voice behavior, run the approved manual integration runner with a test account and report DB message delta without exposing the access token.
