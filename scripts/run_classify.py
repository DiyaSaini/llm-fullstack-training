"""
Run the classify feature from the command line.

ASSOCIATE 2 — this script should work once your service is implemented.
You can run it to manually test your feature end-to-end.

Setup:
    cp .env.example .env
    # Add your GEMINI_API_KEY to .env

Usage:
    python scripts/run_classify.py --text "The new iPhone has a great camera." --categories "technology,sports,politics"
"""

import argparse
import sys
from pathlib import Path

from app.api.v1.schemas.requests.classify import ClassifyRequest
from app.config import settings
from app.core.pipeline.classify_pipeline import ClassifyPipeline
from app.logging import get_logger, setup_logging
from app.providers.llm_provider import GeminiProvider, LLMProviderError
from app.services.classify.service import ClassifyService

# Allow running from the repo root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()

setup_logging()
logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the classify pipeline from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--text", type=str, required=True, help="Text to classify")
    parser.add_argument(
        "--categories",
        type=str,
        default=None,
        dest="categories",
        help="Optional comma-separated list of categories",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # ── Initialise provider and pipeline ──────────────────────────────────────
    provider = GeminiProvider(model="gemini-2.0-flash", api_key=settings.llm_api_key)
    pipeline = ClassifyPipeline(service=ClassifyService(provider=provider))

    # ── Build request ─────────────────────────────────────────────────────────
    categories = (
        [c.strip() for c in args.categories.split(",")] if args.categories else None
    )
    request = ClassifyRequest(text=args.text, categories=categories)

    # ── Execute ───────────────────────────────────────────────────────────────
    print("\n⏳ Running classify pipeline...")
    try:
        result = pipeline.execute(request)
    except ValueError as e:
        print(f"\n❌ Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except LLMProviderError as e:
        print(f"\n❌ LLM provider error: {e}", file=sys.stderr)
        sys.exit(1)

    # ── Print result ──────────────────────────────────────────────────────────
    print("\n✅ Done!")
    print(f"\nCategory:    {result.category}")
    print(f"Confidence:  {result.confidence:.2f}")
    print(f"Reasoning:   {result.reasoning}")
    print()


if __name__ == "__main__":
    main()
