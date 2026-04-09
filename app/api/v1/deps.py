"""
FastAPI dependency injection.

All `Depends()` callables live here.
Controllers import from this module — they never instantiate
providers or pipelines directly.

This is the only place where concrete classes are wired together.
"""

from functools import lru_cache

from fastapi import Depends

from app.config import settings
from app.core.pipeline.classify_pipeline import ClassifyPipeline
from app.core.pipeline.keywords_pipeline import KeywordsPipeline
from app.core.pipeline.paraphrase_pipeline import ParaphrasePipeline
from app.core.pipeline.qa_pipeline import QAPipeline
from app.core.pipeline.sentiment_pipeline import SentimentPipeline
from app.core.pipeline.summarize_pipeline import SummarizePipeline
from app.core.pipeline.translate_pipeline import TranslatePipeline
from app.providers.llm_provider import BaseLLMProvider, GeminiProvider
from app.services.classify.service import ClassifyService
from app.services.keywords.service import KeywordsService
from app.services.paraphrase.service import ParaphraseService
from app.services.qa.service import QAService
from app.services.sentiment.service import SentimentService
from app.services.summarize.service import SummarizeService
from app.services.translate.service import TranslateService


@lru_cache
def get_llm_provider() -> BaseLLMProvider:
    """
    Instantiate and cache the LLM provider for the lifetime of the process.

    Returns a GeminiProvider configured from settings.
    Swap this implementation to change the provider globally.
    """
    return GeminiProvider(
        model="gemini-2.0-flash",
        api_key=settings.llm_api_key,
    )


# Each function injects the LLM provider into the concrete service,
# then wraps the service in its pipeline.


def get_summarize_pipeline(
    provider: BaseLLMProvider = Depends(get_llm_provider),
) -> SummarizePipeline:
    return SummarizePipeline(service=SummarizeService(provider=provider))


def get_classify_pipeline(
    provider: BaseLLMProvider = Depends(get_llm_provider),
) -> ClassifyPipeline:
    return ClassifyPipeline(service=ClassifyService(provider=provider))


def get_keywords_pipeline(
    provider: BaseLLMProvider = Depends(get_llm_provider),
) -> KeywordsPipeline:
    return KeywordsPipeline(service=KeywordsService(provider=provider))


def get_sentiment_pipeline(
    provider: BaseLLMProvider = Depends(get_llm_provider),
) -> SentimentPipeline:
    return SentimentPipeline(service=SentimentService(provider=provider))


def get_qa_pipeline(
    provider: BaseLLMProvider = Depends(get_llm_provider),
) -> QAPipeline:
    return QAPipeline(service=QAService(provider=provider))


def get_paraphrase_pipeline(
    provider: BaseLLMProvider = Depends(get_llm_provider),
) -> ParaphrasePipeline:
    return ParaphrasePipeline(service=ParaphraseService(provider=provider))


def get_translate_pipeline(
    provider: BaseLLMProvider = Depends(get_llm_provider),
) -> TranslatePipeline:
    return TranslatePipeline(service=TranslateService(provider=provider))
