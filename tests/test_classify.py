"""
Tests for the classify feature.

ASSOCIATE 2 — implement the tests marked with TODO.
The fixtures in conftest.py give you a MockLLMProvider so tests
never call the real Gemini API.

Run just these tests:
    pytest tests/test_classify.py -v
"""

import pytest

from app.api.v1.schemas.requests.classify import ClassifyRequest
from app.api.v1.schemas.responses.classify import ClassifyResponse
from app.core.pipeline.classify_pipeline import ClassifyPipeline
from app.services.classify.service import ClassifyService

# ── Service unit tests ─────────────────────────────────────────────────────────


def test_validate_input_raises_on_empty_text(mock_provider):
    """validate_input must raise ValueError when text is empty or whitespace."""
    service = ClassifyService(provider=mock_provider)
    request = ClassifyRequest(text="  ")
    with pytest.raises(ValueError):
        service.validate_input(request)


def test_parse_response_raises_on_invalid_json(mock_provider):
    """parse_response must raise ValueError when the LLM returns non-JSON."""
    service = ClassifyService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("this is not json at all")


def test_parse_response_raises_on_empty_string(mock_provider):
    """parse_response must raise ValueError on empty string."""
    service = ClassifyService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("")


def test_parse_response_returns_correct_type(mock_provider, classify_mock_response):
    """parse_response must return a ClassifyResponse instance."""
    mock_provider.response = classify_mock_response
    service = ClassifyService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert isinstance(result, ClassifyResponse)


def test_parse_response_has_expected_fields(mock_provider, classify_mock_response):
    """Response object must have all required fields populated."""
    mock_provider.response = classify_mock_response
    service = ClassifyService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert hasattr(result, "category")
    assert hasattr(result, "confidence")
    assert hasattr(result, "reasoning")


def test_validate_input_normalises_categories(mock_provider):
    service = ClassifyService(provider=mock_provider)
    request = ClassifyRequest(text="Some text.", categories=["TECH", "Sports"])
    result = service.validate_input(request)
    assert all(c == c.lower() for c in result.categories)


def test_build_prompt_includes_categories_when_provided(mock_provider):
    service = ClassifyService(provider=mock_provider)
    from app.services.classify.models import ClassifyInput

    validated = ClassifyInput(text="Some text.", categories=["technology", "sports"])
    prompt = service.build_prompt(validated)
    assert "technology" in prompt
    assert "sports" in prompt


def test_confidence_within_range(mock_provider, classify_mock_response):
    mock_provider.response = classify_mock_response
    service = ClassifyService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert 0.0 <= result.confidence <= 1.0


# ── Pipeline integration tests ─────────────────────────────────────────────────


def test_pipeline_execute_returns_response(mock_provider, classify_mock_response):
    """
    Full pipeline run with mock provider must return a valid response.

    TODO (Associate 2):
        - This test calls the full pipeline end to end
        - It will pass once your service methods are all implemented
        - Do not modify this test
    """
    mock_provider.response = classify_mock_response
    from app.services.classify.service import ClassifyService

    pipeline = ClassifyPipeline(service=ClassifyService(provider=mock_provider))
    request = ClassifyRequest(
        text="The new iPhone features a revolutionary camera system."
    )
    result = pipeline.execute(request)
    assert isinstance(result, ClassifyResponse)


def test_pipeline_provider_receives_prompt(mock_provider, classify_mock_response):
    """
    After pipeline execution, the mock provider should have recorded
    the prompt that was sent to it.

    TODO (Associate 2):
        - Verifies build_prompt was called and produced a non-empty string
    """
    mock_provider.response = classify_mock_response
    from app.services.classify.service import ClassifyService

    pipeline = ClassifyPipeline(service=ClassifyService(provider=mock_provider))
    request = ClassifyRequest(
        text="The new iPhone features a revolutionary camera system."
    )
    pipeline.execute(request)
    assert mock_provider.last_prompt is not None
    assert len(mock_provider.last_prompt) > 0


def test_pipeline_propagates_value_error(mock_provider):
    """
    Pipeline must propagate ValueError from validate_input upward.
    The controller catches it — the pipeline itself should not swallow it.
    """
    from app.services.classify.service import ClassifyService

    pipeline = ClassifyPipeline(service=ClassifyService(provider=mock_provider))
    request = ClassifyRequest(text="  ")
    with pytest.raises(ValueError):
        pipeline.execute(request)
