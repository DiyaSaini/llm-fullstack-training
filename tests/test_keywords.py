"""
Tests for the keywords feature.

ASSOCIATE 3 — implement the tests marked with TODO.
The fixtures in conftest.py give you a MockLLMProvider so tests
never call the real Gemini API.

Run just these tests:
    pytest tests/test_keywords.py -v
"""

import pytest

from app.api.v1.schemas.requests.keywords import KeywordsRequest
from app.api.v1.schemas.responses.keywords import KeywordsResponse
from app.core.pipeline.keywords_pipeline import KeywordsPipeline
from app.services.keywords.service import KeywordsService

# ── Service unit tests ─────────────────────────────────────────────────────────


def test_validate_input_raises_on_empty_text(mock_provider):
    """validate_input must raise ValueError when text is empty or whitespace."""
    service = KeywordsService(provider=mock_provider)
    request = KeywordsRequest(text="  ")
    with pytest.raises(ValueError):
        service.validate_input(request)


def test_parse_response_raises_on_invalid_json(mock_provider):
    """parse_response must raise ValueError when the LLM returns non-JSON."""
    service = KeywordsService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("this is not json at all")


def test_parse_response_raises_on_empty_string(mock_provider):
    """parse_response must raise ValueError on empty string."""
    service = KeywordsService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("")


def test_parse_response_returns_correct_type(mock_provider, keywords_mock_response):
    """parse_response must return a KeywordsResponse instance."""
    mock_provider.response = keywords_mock_response
    service = KeywordsService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert isinstance(result, KeywordsResponse)


def test_parse_response_has_expected_fields(mock_provider, keywords_mock_response):
    """Response object must have all required fields populated."""
    mock_provider.response = keywords_mock_response
    service = KeywordsService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert hasattr(result, "keywords")


def test_keywords_ordered_by_relevance(mock_provider, keywords_mock_response):
    mock_provider.response = keywords_mock_response
    service = KeywordsService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    scores = [k.relevance_score for k in result.keywords]
    assert scores == sorted(scores, reverse=True)


def test_build_prompt_includes_max_keywords(mock_provider):
    service = KeywordsService(provider=mock_provider)
    from app.services.keywords.models import KeywordsInput

    validated = KeywordsInput(text="Some text.", max_keywords=5)
    prompt = service.build_prompt(validated)
    assert "5" in prompt


def test_relevance_scores_within_range(mock_provider, keywords_mock_response):
    mock_provider.response = keywords_mock_response
    service = KeywordsService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    for kw in result.keywords:
        assert 0.0 <= kw.relevance_score <= 1.0


# ── Pipeline integration tests ─────────────────────────────────────────────────


def test_pipeline_execute_returns_response(mock_provider, keywords_mock_response):
    """
    Full pipeline run with mock provider must return a valid response.

    TODO (Associate 3):
        - This test calls the full pipeline end to end
        - It will pass once your service methods are all implemented
        - Do not modify this test
    """
    mock_provider.response = keywords_mock_response
    from app.services.keywords.service import KeywordsService

    pipeline = KeywordsPipeline(service=KeywordsService(provider=mock_provider))
    request = KeywordsRequest(
        text="Climate change is accelerating the frequency of extreme weather events globally."
    )
    result = pipeline.execute(request)
    assert isinstance(result, KeywordsResponse)


def test_pipeline_provider_receives_prompt(mock_provider, keywords_mock_response):
    """
    After pipeline execution, the mock provider should have recorded
    the prompt that was sent to it.

    TODO (Associate 3):
        - Verifies build_prompt was called and produced a non-empty string
    """
    mock_provider.response = keywords_mock_response
    from app.services.keywords.service import KeywordsService

    pipeline = KeywordsPipeline(service=KeywordsService(provider=mock_provider))
    request = KeywordsRequest(
        text="Climate change is accelerating the frequency of extreme weather events globally."
    )
    pipeline.execute(request)
    assert mock_provider.last_prompt is not None
    assert len(mock_provider.last_prompt) > 0


def test_pipeline_propagates_value_error(mock_provider):
    """
    Pipeline must propagate ValueError from validate_input upward.
    The controller catches it — the pipeline itself should not swallow it.
    """
    from app.services.keywords.service import KeywordsService

    pipeline = KeywordsPipeline(service=KeywordsService(provider=mock_provider))
    request = KeywordsRequest(text="  ")
    with pytest.raises(ValueError):
        pipeline.execute(request)
