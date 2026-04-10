"""
Run the summarize feature from the command line.

ASSOCIATE 1 — this script should work once your service is implemented.
You can run it to manually test your feature end-to-end.

Setup:
    cp .env.example .env
    # Add your GEMINI_API_KEY to .env

Usage:
    python scripts/run_summarize.py --text "Artificial intelligence is changing the world in many ways..."
"""

import argparse
import sys
from pathlib import Path

from app.api.v1.schemas.requests.summarize import SummarizeRequest
from app.config import settings
from app.core.pipeline.summarize_pipeline import SummarizePipeline
from app.logging import get_logger, setup_logging
from app.providers.llm_provider import GeminiProvider, LLMProviderError
from app.services.summarize.service import SummarizeService

# Allow running from the repo root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()


setup_logging()
logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the summarize pipeline from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--text", type=str, required=True, help="Text to summarize")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    provider = GeminiProvider(model="gemini-2.0-flash", api_key=settings.llm_api_key)
    pipeline = SummarizePipeline(service=SummarizeService(provider=provider))

    request = SummarizeRequest(text=args.text)

    print("\nRunning summarize pipeline...")
    try:
        result = pipeline.execute(request)
    except ValueError as e:
        print(f"\nValidation error: {e}", file=sys.stderr)
        sys.exit(1)
    except LLMProviderError as e:
        print(f"\nLLM provider error: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nDone!")
    print(f"\nShort Summary:\n  {result.short_summary}")
    print(f"\nDetailed Summary:\n  {result.detailed_summary}")
    print("\nKey Points:")
    for point in result.key_points:
        print(f"  • {point}")
    print()


if __name__ == "__main__":
    main()
