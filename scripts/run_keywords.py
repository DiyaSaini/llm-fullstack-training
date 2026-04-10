"""
Run the keywords feature from the command line.

ASSOCIATE 3 — this script should work once your service is implemented.
You can run it to manually test your feature end-to-end.

Setup:
    cp .env.example .env
    # Add your GEMINI_API_KEY to .env

Usage:
    python scripts/run_keywords.py --text "Climate change is reshaping our world." --max-keywords 5
"""

import argparse
import sys
from pathlib import Path

from app.api.v1.schemas.requests.keywords import KeywordsRequest
from app.config import settings
from app.core.pipeline.keywords_pipeline import KeywordsPipeline
from app.logging import get_logger, setup_logging
from app.providers.llm_provider import GeminiProvider, LLMProviderError
from app.services.keywords.service import KeywordsService

# Allow running from the repo root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()


setup_logging()
logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the keywords pipeline from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--text", type=str, required=True, help="Text to extract keywords from"
    )
    parser.add_argument(
        "--max-keywords",
        type=int,
        default=10,
        dest="max_keywords",
        help="Maximum number of keywords (default: 10)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    provider = GeminiProvider(model="gemini-2.0-flash", api_key=settings.llm_api_key)
    pipeline = KeywordsPipeline(service=KeywordsService(provider=provider))

    request = KeywordsRequest(text=args.text, max_keywords=args.max_keywords)

    print("\nRunning keywords pipeline...")
    try:
        result = pipeline.execute(request)
    except ValueError as e:
        print(f"\nValidation error: {e}", file=sys.stderr)
        sys.exit(1)
    except LLMProviderError as e:
        print(f"\nLLM provider error: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nDone!")
    print("\nKeywords (by relevance):")
    for kw in result.keywords:
        print(f"  {kw.relevance_score:.2f}  {kw.word}")
    print()


if __name__ == "__main__":
    main()
