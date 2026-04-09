"""
Tests for the sentiment feature.

ASSOCIATE 4 — implement the tests marked with TODO.
The fixtures in conftest.py give you a MockLLMProvider so tests
never call the real Gemini API.

Run just these tests:
    pytest tests/test_sentiment.py -v
"""

import pytest

from app.api.v1.schemas.requests.sentiment import SentimentRequest
from app.api.v1.schemas.responses.sentiment import SentimentResponse
from app.core.pipeline.sentiment_pipeline import SentimentPipeline
from app.services.sentiment.service import SentimentService

# ── Service unit tests ─────────────────────────────────────────────────────────


def test_validate_input_raises_on_empty_text(mock_provider):
    """validate_input must raise ValueError when text is empty or whitespace."""
    service = SentimentService(provider=mock_provider)
    request = SentimentRequest(text="  ")
    with pytest.raises(ValueError):
        service.validate_input(request)


def test_parse_response_raises_on_invalid_json(mock_provider):
    """parse_response must raise ValueError when the LLM returns non-JSON."""
    service = SentimentService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("this is not json at all")


def test_parse_response_raises_on_empty_string(mock_provider):
    """parse_response must raise ValueError on empty string."""
    service = SentimentService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("")


def test_parse_response_returns_correct_type(mock_provider, sentiment_mock_response):
    """parse_response must return a SentimentResponse instance."""
    mock_provider.response = sentiment_mock_response
    service = SentimentService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert isinstance(result, SentimentResponse)


def test_parse_response_has_expected_fields(mock_provider, sentiment_mock_response):
    """Response object must have all required fields populated."""
    mock_provider.response = sentiment_mock_response
    service = SentimentService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert hasattr(result, "sentiment")
    assert hasattr(result, "score")
    assert hasattr(result, "reasoning")
    assert hasattr(result, "emotions")


def test_sentiment_is_valid_label(mock_provider, sentiment_mock_response):
    mock_provider.response = sentiment_mock_response
    service = SentimentService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert result.sentiment in {"positive", "negative", "neutral", "mixed"}


def test_score_within_range(mock_provider, sentiment_mock_response):
    mock_provider.response = sentiment_mock_response
    service = SentimentService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert -1.0 <= result.score <= 1.0


def test_emotions_is_list(mock_provider, sentiment_mock_response):
    mock_provider.response = sentiment_mock_response
    service = SentimentService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert isinstance(result.emotions, list)


# ── Pipeline integration tests ─────────────────────────────────────────────────


def test_pipeline_execute_returns_response(mock_provider, sentiment_mock_response):
    """
    Full pipeline run with mock provider must return a valid response.

    TODO (Associate 4):
        - This test calls the full pipeline end to end
        - It will pass once your service methods are all implemented
        - Do not modify this test
    """
    mock_provider.response = sentiment_mock_response
    from app.services.sentiment.service import SentimentService

    pipeline = SentimentPipeline(service=SentimentService(provider=mock_provider))
    request = SentimentRequest(
        text="I absolutely loved this product! Highly recommend it."
    )
    result = pipeline.execute(request)
    assert isinstance(result, SentimentResponse)


def test_pipeline_provider_receives_prompt(mock_provider, sentiment_mock_response):
    """
    After pipeline execution, the mock provider should have recorded
    the prompt that was sent to it.

    TODO (Associate 4):
        - Verifies build_prompt was called and produced a non-empty string
    """
    mock_provider.response = sentiment_mock_response
    from app.services.sentiment.service import SentimentService

    pipeline = SentimentPipeline(service=SentimentService(provider=mock_provider))
    request = SentimentRequest(
        text="I absolutely loved this product! Highly recommend it."
    )
    pipeline.execute(request)
    assert mock_provider.last_prompt is not None
    assert len(mock_provider.last_prompt) > 0


def test_pipeline_propagates_value_error(mock_provider):
    """
    Pipeline must propagate ValueError from validate_input upward.
    The controller catches it — the pipeline itself should not swallow it.
    """
    from app.services.sentiment.service import SentimentService

    pipeline = SentimentPipeline(service=SentimentService(provider=mock_provider))
    request = SentimentRequest(text="  ")
    with pytest.raises(ValueError):
        pipeline.execute(request)
