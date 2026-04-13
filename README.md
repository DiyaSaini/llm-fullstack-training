# llm-fullstack-training

## Project Overview

Users submit text, the API processes it — summarize, classify, extract keywords, detect sentiment, answer questions, paraphrase, or translate. Each feature is an independent vertical slice owned by one engineer.

This repository contains the production-structured foundation for an AI Text Processing REST API built with FastAPI. The architecture follows a strict N-Layered pattern to enforce separation of concerns.

You are required to build the concrete implementation for your assigned feature slice. You will not build this as a monolithic script — you will integrate your logic into the existing pipeline.

---

## Repository Structure

```
llm-fullstack-training/
├── app/
│   ├── main.py                        # App factory, router registration
│   ├── config.py                      # Settings, loads .env
│   ├── logging.py                     # Structured logging
│   ├── api/v1/
│   │   ├── deps.py                    # Dependency injection
│   │   ├── routers/                   # YOUR route files
│   │   ├── controllers/               # YOUR controller files
│   │   └── schemas/
│   │       ├── requests/              # YOUR request schemas
│   │       └── responses/             # YOUR response schemas
│   ├── core/
│   │   ├── interfaces/                # READ THESE — they are your spec
│   │   └── pipeline/                  # READ THESE — they define execution order
│   ├── providers/
│   │   └── llm_provider.py            # IMPLEMENT GeminiProvider here
│   └── services/
│       └── <feature>/
│           ├── service.py             # YOUR main implementation
│           └── models.py              # YOUR internal dataclasses
├── scripts/
│   └── run_<feature>.py               # CLI runner to test your feature standalone
├── .env.example                       # Copy to .env and fill in your API key
├── pyproject.toml                     # Project config, linting, type checking
└── requirements.txt                   # Runtime dependencies for pip users
```

---

## Architecture

Data flows strictly top-down through these layers:

```
HTTP Request
    ↓
Router          (app/api/v1/routers/)         — declares the endpoint, nothing else
    ↓
Controller      (app/api/v1/controllers/)     — handles HTTP, calls pipeline, returns response
    ↓
Pipeline        (app/core/pipeline/)          — orchestrates execution order
    ↓
Interface       (app/core/interfaces/)        — abstract contract your service must satisfy
    ↓
Service         (app/services/<feature>/)     — YOUR implementation lives here
    ↓
LLM Provider    (app/providers/)             — calls the Gemini API
    ↓
HTTP Response
```

**Internal data between service methods uses dataclasses. Pydantic is used only at the HTTP boundary.**

---

## What Is Already Built — DO NOT TOUCH

| File / Folder | Purpose |
|---|---|
| `app/main.py` | App factory, registers all routers |
| `app/config.py` | Loads `.env`, exposes `settings` object |
| `app/logging.py` | Structured logging setup |
| `app/api/v1/deps.py` | Dependency injection — wires pipelines to routes |
| `app/core/interfaces/` | Abstract contracts your service must implement |
| `app/core/pipeline/` | Orchestration — calls your service methods in the correct order |
| `app/providers/llm_provider.py` | `BaseLLMProvider` ABC + `GeminiProvider` stub to implement |

---

## What You Must Build

Every associate owns one complete vertical slice:

| File | Your job |
|---|---|
| `app/api/v1/schemas/requests/<feature>.py` | Pydantic request model |
| `app/api/v1/schemas/responses/<feature>.py` | Pydantic response model |
| `app/services/<feature>/models.py` | Internal dataclasses (already stubbed, extend if needed) |
| `app/services/<feature>/service.py` | Implement `validate_input`, `build_prompt`, `parse_response` |
| `app/api/v1/controllers/<feature>_controller.py` | Implement `handle()` — call pipeline, catch exceptions |
| `app/api/v1/routers/<feature>.py` | Register the endpoint, call the controller |

---

## Task Assignments

| Feature    | Branch               | Endpoint                  |
|------------|----------------------|---------------------------|
| Summarize  | `feature/summarize`  | `POST /api/v1/summarize`  |
| Classify   | `feature/classify`   | `POST /api/v1/classify`   |
| Keywords   | `feature/keywords`   | `POST /api/v1/keywords`   |
| Sentiment  | `feature/sentiment`  | `POST /api/v1/sentiment`  |
| Q&A        | `feature/qa`         | `POST /api/v1/qa`         |
| Paraphrase | `feature/paraphrase` | `POST /api/v1/paraphrase` |
| Translate  | `feature/translate`  | `POST /api/v1/translate`  |

---

## Local Setup

**1. Clone the repository:**
```bash
git clone <repository_url>
cd llm-fullstack-training
```

**2. Configure the environment:**

Without uv:
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # If you want dev dependencies too: pip install -r requirements-dev.txt
```

With uv:
```bash
uv sync
```

> Not sure what uv is? [uv docs](https://docs.astral.sh/uv/) — [Installation](https://docs.astral.sh/uv/getting-started/installation/)

**3. Install pre-commit hooks (MANDATORY):**
```bash
pre-commit install
```

> This repository enforces strict code quality. Pre-commit hooks run Ruff (linting/formatting), Mypy (type checking), and Bandit (security scanning) on every commit. If your code fails, the commit is blocked. Fix the errors before pushing.

**4. Add your LLM provider:**

This project does not ship with an LLM provider. You must install one yourself.

Recommended: **Google Gemini (free tier)**

Get your API key: https://aistudio.google.com/app/apikey

```bash
# pip
pip install google-genai

# uv
uv add google-genai
```

You will implement `GeminiProvider` in `app/providers/llm_provider.py`. Choose any model available on your key. Recommended free-tier options:
- `gemini-2.0-flash` — fast, good quality
- `gemini-2.0-flash-lite` — fastest, lowest quota cost

**5. Configure environment variables:**
```bash
cp .env.example .env
```

Open `.env` and set:
```
LLM_API_KEY=your_key_here
```

---

## Implementation Guide

**Step 1 — Read your interface first**

Open `app/core/interfaces/<feature>_interface.py`. This is your spec. It defines exactly what methods you must implement and what inputs/outputs are expected.

**Step 2 — Read your pipeline**

Open `app/core/pipeline/<feature>_pipeline.py`. This shows the exact order your methods will be called:
```
validate_input → build_prompt → provider.generate → parse_response
```

**Step 3 — Implement your service**

Open `app/services/<feature>/service.py`. Every method has a `TODO` comment explaining exactly what to do. Implement them one by one.

**Step 4 — Complete schemas, controller, router**

Wire them together following the existing stubs. The controller handles HTTP errors. The router just registers the endpoint.

**Step 5 — Test with the CLI script**

```bash
python scripts/run_summarize.py --text "Your text here..."
python scripts/run_classify.py --text "Your text here..." --categories "technology,sports"
python scripts/run_keywords.py --text "Your text here..." --max-keywords 5
python scripts/run_sentiment.py --text "Your text here..."
python scripts/run_qa.py --context "Your context..." --question "Your question?"
python scripts/run_paraphrase.py --text "Your text here..." --tones "formal,casual"
python scripts/run_translate.py --text "Bonjour!" --target-language "English"
```

**Step 6 — Run the server and test via Swagger**

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

---

## LLM Prompt Engineering Tips

Your `build_prompt` must instruct the LLM to return only valid JSON with no markdown fences. Always end your prompt with:

```
Respond ONLY with a valid JSON object. Do not include any explanation,
markdown formatting, or code fences. Just the raw JSON.
```

Your `parse_response` should defensively strip fences in case the model ignores the instruction:

```python
raw = raw_response.strip()
if raw.startswith("```"):
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
raw = raw.strip()
result = json.loads(raw)
```

---

## Development Workflow & Rules

1. **Branching** — Always branch from `dev`:
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/<your-feature>
   ```
   Direct pushes to `main` and `dev` are blocked.

2. **Commits** — Commit frequently with clear messages:
   ```bash
   git add .
   git commit -m "feat(summarize): implement validate_input and build_prompt"
   ```

3. **Pull Requests** — Open a PR against `dev` when your feature is complete. Not before.

4. **CI enforcement** — Every PR triggers the CI pipeline (Ruff, Mypy, Bandit).
   - If CI fails, your PR will be ignored
   - Do not request review until CI is green
   - Debugging CI failures is your responsibility

5. **Merge requirements** — CI must be green and at least one peer must approve before merge.

---

## Definition of Done

Your feature is complete when all of the following are true:

- [ ] Pre-commit hooks pass locally on every commit
- [ ] CI pipeline is green on your PR
- [ ] `python scripts/run_<feature>.py` produces correct output with a real API key
- [ ] The endpoint responds correctly at http://localhost:8000/docs
- [ ] You can explain every line of code you wrote
- [ ] A peer has reviewed and approved your PR
