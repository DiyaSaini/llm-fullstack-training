"""
Run the sentiment feature from the command line.

ASSOCIATE 4 — this script should work once your service is implemented.
You can run it to manually test your feature end-to-end.

Setup:
    cp .env.example .env
    # Add your GEMINI_API_KEY to .env

Usage:
    python scripts/run_sentiment.py --text "I absolutely loved this product!"
"""

import argparse
import sys
from pathlib import Path

from app.api.v1.schemas.requests.sentiment import SentimentRequest
from app.config import settings
from app.core.pipeline.sentiment_pipeline import SentimentPipeline
from app.logging import get_logger, setup_logging
from app.providers.llm_provider import GeminiProvider, LLMProviderError
from app.services.sentiment.service import SentimentService

# Allow running from the repo root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()


setup_logging()
logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the sentiment pipeline from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--text", type=str, required=True, help="Text to analyse")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    provider = GeminiProvider(model="gemini-2.0-flash", api_key=settings.llm_api_key)
    pipeline = SentimentPipeline(service=SentimentService(provider=provider))

    request = SentimentRequest(text=args.text)

    print("\nRunning sentiment pipeline...")
    try:
        result = pipeline.execute(request)
    except ValueError as e:
        print(f"\nValidation error: {e}", file=sys.stderr)
        sys.exit(1)
    except LLMProviderError as e:
        print(f"\nLLM provider error: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nDone!")
    print(f"\nSentiment:  {result.sentiment}")
    print(
        f"Score:      {result.score:.2f}  (-1.0 = very negative, 1.0 = very positive)"
    )
    print(f"Reasoning:  {result.reasoning}")
    print(
        f"Emotions:   {', '.join(result.emotions) if result.emotions else 'none detected'}"
    )
    print()


if __name__ == "__main__":
    main()
