"""
Run the translate feature from the command line.

ASSOCIATE 7 — this script should work once your service is implemented.
You can run it to manually test your feature end-to-end.

Setup:
    cp .env.example .env
    # Add your GEMINI_API_KEY to .env

Usage:
    python scripts/run_translate.py --text "Bonjour, comment allez-vous?" --target-language "English"
"""

import argparse
import sys
from pathlib import Path

from app.api.v1.schemas.requests.translate import TranslateRequest
from app.config import settings
from app.core.pipeline.translate_pipeline import TranslatePipeline
from app.logging import get_logger, setup_logging
from app.providers.llm_provider import GeminiProvider, LLMProviderError
from app.services.translate.service import TranslateService

# Allow running from the repo root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()


setup_logging()
logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the translate pipeline from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--text", type=str, required=True, help="Text to translate")
    parser.add_argument(
        "--target-language",
        type=str,
        required=True,
        help="Target language (e.g. French, Spanish, Hindi)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    provider = GeminiProvider(model="gemini-2.0-flash", api_key=settings.llm_api_key)
    pipeline = TranslatePipeline(service=TranslateService(provider=provider))

    request = TranslateRequest(text=args.text, target_language=args.target_language)

    print("\nRunning translate pipeline...")
    try:
        result = pipeline.execute(request)
    except ValueError as e:
        print(f"\nValidation error: {e}", file=sys.stderr)
        sys.exit(1)
    except LLMProviderError as e:
        print(f"\nLLM provider error: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nDone!")
    print(f"\nDetected language: {result.detected_language}")
    print(f"Target language:   {result.target_language}")
    print(f"Confidence:        {result.confidence:.2f}")
    print(f"\nTranslation:\n  {result.translated_text}")
    print()


if __name__ == "__main__":
    main()
