# Resume Bullet Optimizer (Local First)

A local-first web app that rewrites resume bullet points into stronger, role-targeted versions using a locally running LLM. The frontend is built in TypeScript and the backend is a Python FastAPI service that enforces strict JSON output, validates results, and returns follow-up questions when key details like metrics are missing.

## Features
- Paste one or many resume bullets and an optional job description
- Generates 3 variants per bullet:
  - impact-first
  - scope-first
  - tech-first
- Strict JSON schema for reliable outputs
- Built-in linting and validation:
  - character length limits
  - strong action verbs
  - no first-person language
  - quantified impact checks
- Flags missing info (metrics, scale, scope) and suggests targeted follow-up questions
- Local-first inference (no paid API required)

## Tech Stack
- Frontend: TypeScript (Next.js or React)
- Backend: Python (FastAPI)
- Local LLM runtime: Ollama or LM Studio (HTTP API)
