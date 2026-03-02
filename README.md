# Local-Agentic-Resume-Enhancer

A local-first agentic web app that rewrites resume bullet points into stronger, role-targeted versions using a locally running LLM. Built to demonstrate core agentic AI patterns including self-correction loops, critic-rewriter pipelines, and multi-stage LLM orchestration — all without a paid API.

## Agentic Architecture

The backend implements a two-stage agentic pipeline per bullet:

**Stage 1 — Rewriter Loop (self-correction)**
The LLM generates three variant rewrites. If the response fails JSON parsing, the agent feeds the broken output back to the LLM with a correction prompt and retries up to 3 times. This teaches the model to observe its own failure and act to fix it.

**Stage 2 — Critic Loop (quality gate)**
If valid variants are produced, a second LLM call evaluates them against per-variant rules (does `impact_first` actually lead with an outcome? does `scope_first` avoid invented scope?) and global hallucination rules (no invented metrics, tools, or team sizes). If rejected, the critic's feedback is injected into a new rewrite prompt and the rewriter tries again, up to 2 times.

```
validate_bullet()              ← deterministic pre-check
        │
        ▼
Rewriter loop (max 3)
  generate() → parse JSON → ✅ break
                           → ❌ correction prompt → retry
        │
        ▼
Critic loop (max 2)
  critique_variants() → ✅ approved → break
                      → ❌ rewrite with feedback → retry
        │
        ▼
RewriteResponse → frontend
```

## Features

- Paste one or many resume bullets and an optional job description
- Generates 3 variants per bullet:
  - `impact_first` — leads with measurable result or outcome
  - `scope_first` — leads with scale, team size, or project scope
  - `tech_first` — leads with technologies, tools, or methodologies
- Self-correcting JSON output — retries with corrective context on parse failure
- Critic-rewriter feedback loop — LLM evaluates its own output and rewrites on rejection
- Deterministic input validation:
  - strong action verb check
  - no first-person language
  - character length limit (150 chars)
  - quantified impact check
- Flags missing info and generates targeted follow-up questions
- Hallucination prevention — rewriter and critic both enforce no invented metrics, tools, or scope

## Next Steps

**Follow-up question replies**
Add a text box per bullet that lets users answer the generated follow-up questions (ex. providing the actual team size, metrics, or technologies used). The LLM then regenerates all three variants using the new context, closing the human-in-the-loop feedback cycle.

**Level 3 — Tool Use**
Instead of always running the same fixed prompt, an agent first analyzes the bullet and decides which tools to invoke — such as `classify_bullet_type` or `identify_missing_info` — before rewriting. The LLM determines its own execution path rather than following a hardcoded pipeline.

**Level 4 — Multi-Agent Orchestration**
Split responsibilities across three specialized agents coordinated by an orchestrator: a Critic Agent that diagnoses weaknesses, a Rewriter Agent that generates variants based on that diagnosis, and an Evaluator Agent that scores and ranks the final outputs.

## Tech Stack

- **Frontend:** React + TypeScript (Vite)
- **Backend:** Python (FastAPI)
- **Local LLM runtime:** Ollama — llama3.2:3b
