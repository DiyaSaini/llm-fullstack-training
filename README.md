# llm-fullstack-training

## Project Overview
Users submit text, the API does things to it — summarize, classify, extract keywords, detect sentiment, answer questions about it. Simple, very modular, each route is independent.

This repository contains the foundation for a production-structured AI Text Processing REST API built with FastAPI and LLM. The architecture follows a strict N-Layered pattern to enforce separation of concerns.

You are required to build the concrete implementations for your assigned feature slice. You will not build this as a monolithic script; you will integrate your logic into the existing pipeline.

## Architecture & Boundaries
The system is divided into layers. Data flows top-down.

HTTP Request -> Router -> Controller -> Pipeline -> Interface -> Service -> LLM Provider -> HTTP Response

**What is already built (DO NOT TOUCH):**
* `app/main.py` & `app/config.py` (Application factory and environment loading)
* `app/api/v1/deps.py` (Dependency injection)
* `app/core/interfaces/` (The abstract base contracts your service MUST fulfill)
* `app/core/pipeline/` (The orchestration layer)
* `app/providers/` (The Gemini API connection layer)

**What you must build:**
* **Schemas:** Pydantic models for your specific request and response payloads.
* **Service:** The concrete class containing your business logic and LLM prompt engineering, inheriting from your assigned core interface.
* **Controller:** The function that handles the HTTP request, injects the payload into the pipeline, and returns the response schema.
* **Router:** The FastAPI endpoint registration.
* **Tests:** Pytest unit tests for your service using the provided mock LLM provider.

## Task Assignments
You are responsible for one vertical slice. Find your assignment below.

| Feature    | Branch               | Endpoint                  |
|------------|----------------------|---------------------------|
| Summarize  | `feature/summarize`  | `POST /api/v1/summarize`  |
| Classify   | `feature/classify`   | `POST /api/v1/classify`   |
| Keywords   | `feature/keywords`   | `POST /api/v1/keywords`   |
| Sentiment  | `feature/sentiment`  | `POST /api/v1/sentiment`  |
| Q&A        | `feature/qa`         | `POST /api/v1/qa`         |
| Paraphrase | `feature/paraphrase` | `POST /api/v1/paraphrase` |
| Translate  | `feature/translate`  | `POST /api/v1/translate`  |

## Local Setup
Execute these exact commands to configure your local development environment.

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd llm-fullstack-training
    ```

2. **Configure the environment (assuming standard virtual environment):**

   If not using uv

    ```bash
    python -m venv .venv
    source .venv/bin/activate # Windows : .venv\Scripts\activate
    pip install -r requirements.txt
    ```

    With uv

    ```bash
    uv sync
    ```
    If you don't know what uv is and want to know more, visit here [uv](https://docs.astral.sh/uv/).

    To install uv [Installation | uv](https://docs.astral.sh/uv/getting-started/installation/).

4. **Install Pre-Comit Hooks (MANDATORY):**
    ```bash
    pre-commit install
    ```

    Note: This repository enforces strict code quality. The pre-commit hooks will automatically run Ruff (linting/ formatting), Mypy (type checking), and Bandit (security scanning) every time you attempt to commit. If your code fails these checks, the commit will be blocked locally. You must fix the errors before pushing.

4. **Environment Variables:**
    ```bash
    cp .env.example .env
    ```
    Open the .env file and insert your LLM Model Key here.

## Development Workflow & Rules
  1. **Branching**: Checkout your specific feature branch (e.g. git checkout -b feature/summarize). Direct pushes to main are mechanically blocked.
  2. **Implementation Sequence**:
     * Read your assigned interface in app/core/interfaces/ to understand the inputs and outputs required.
     * Write your Pydantic schemas.
     * Write you Service implementation.
     * Wire the Controller and Router.
     * Write your tests.
  3. **Pull Requests**: Open a PR against the dev branch when your feature is complete.
  4. **CI/CD Enforcement**: Every PR triggers a Github Actions pipeline running the test suite, linters, and type checkers.
     * If the CI pipeline fails, your PR will be ignored.
     * Do not request a code review until the CI pipeline is green. It is your responsibility to debug and resolve your own build errors.
  5. **Merge Requirements**: Code is only merged after passing CI and receiving explicit peer review approval.

## Execution
  To run the server locally for testing:
  ```bash
  uvicorn app.main:app --reload
  ```
  Access the Swagger UI at [localhost:8000/docs](http://127.0.0.1:8000/docs) to test your endpoints.
