"""
Run the qa feature from the command line.

ASSOCIATE 5 — this script should work once your service is implemented.
You can run it to manually test your feature end-to-end.

Setup:
    cp .env.example .env
    # Add your GEMINI_API_KEY to .env

Usage:
    python scripts/run_qa.py --context "Python was created by Guido van Rossum." --question "Who created Python?"
"""

import argparse
import sys
from pathlib import Path

from app.api.v1.schemas.requests.qa import QARequest
from app.config import settings
from app.core.pipeline.qa_pipeline import QAPipeline
from app.logging import get_logger, setup_logging
from app.providers.llm_provider import GeminiProvider, LLMProviderError
from app.services.qa.service import QAService

# Allow running from the repo root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()


setup_logging()
logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the qa pipeline from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--context",
        type=str,
        required=True,
        help="Context passage to answer from",
    )
    parser.add_argument(
        "--question", type=str, required=True, help="Question to answer"
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    provider = GeminiProvider(model="gemini-2.0-flash", api_key=settings.llm_api_key)
    pipeline = QAPipeline(service=QAService(provider=provider))

    request = QARequest(context=args.context, question=args.question)

    print("\nRunning qa pipeline...")
    try:
        result = pipeline.execute(request)
    except ValueError as e:
        print(f"\nValidation error: {e}", file=sys.stderr)
        sys.exit(1)
    except LLMProviderError as e:
        print(f"\nLLM provider error: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nDone!")
    print(f"\nAnswerable: {result.is_answerable}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Answer:     {result.answer}")
    print()


if __name__ == "__main__":
    main()
