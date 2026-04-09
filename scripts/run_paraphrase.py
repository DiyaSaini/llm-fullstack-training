"""
Run the paraphrase feature from the command line.

ASSOCIATE 6 — this script should work once your service is implemented.
You can run it to manually test your feature end-to-end.

Setup:
    cp .env.example .env
    # Add your GEMINI_API_KEY to .env

Usage:
    python scripts/run_paraphrase.py --text "The utilisation of advanced methods." --tones "formal,casual,simple"
"""

import argparse
import sys
from pathlib import Path

from app.api.v1.schemas.requests.paraphrase import ParaphraseRequest
from app.config import settings
from app.core.pipeline.paraphrase_pipeline import ParaphrasePipeline
from app.logging import get_logger, setup_logging
from app.providers.llm_provider import GeminiProvider, LLMProviderError
from app.services.paraphrase.service import ParaphraseService

# Allow running from the repo root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()


setup_logging()
logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the paraphrase pipeline from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--text", type=str, required=True, help="Text to paraphrase")
    parser.add_argument(
        "--tones",
        type=str,
        default="formal,casual",
        dest="tones",
        help="Comma-separated tones (default: formal,casual)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # ── Initialise provider and pipeline ──────────────────────────────────────
    provider = GeminiProvider(model="gemini-2.0-flash", api_key=settings.llm_api_key)
    pipeline = ParaphrasePipeline(service=ParaphraseService(provider=provider))

    # ── Build request ─────────────────────────────────────────────────────────
    tones = [t.strip() for t in args.tones.split(",")]
    request = ParaphraseRequest(text=args.text, tones=tones)

    # ── Execute ───────────────────────────────────────────────────────────────
    print("\n⏳ Running paraphrase pipeline...")
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
    print("\nParaphrases:")
    for variant in result.paraphrases:
        print(f"\n  [{variant.tone.upper()}]")
        print(f"  {variant.text}")
    print()


if __name__ == "__main__":
    main()
