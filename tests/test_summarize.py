"""
Tests for the summarize feature.

ASSOCIATE 1 — implement the tests marked with TODO.
The fixtures in conftest.py give you a MockLLMProvider so tests
never call the real Gemini API.

Run just these tests:
    pytest tests/test_summarize.py -v
"""

import pytest

from app.api.v1.schemas.requests.summarize import SummarizeRequest
from app.api.v1.schemas.responses.summarize import SummarizeResponse
from app.core.pipeline.summarize_pipeline import SummarizePipeline
from app.services.summarize.service import SummarizeService

# ── Service unit tests ─────────────────────────────────────────────────────────


def test_validate_input_raises_on_empty_text(mock_provider):
    """validate_input must raise ValueError when text is empty or whitespace."""
    service = SummarizeService(provider=mock_provider)
    request = SummarizeRequest(text="Hi")
    with pytest.raises(ValueError):
        service.validate_input(request)


def test_parse_response_raises_on_invalid_json(mock_provider):
    """parse_response must raise ValueError when the LLM returns non-JSON."""
    service = SummarizeService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("this is not json at all")


def test_parse_response_raises_on_empty_string(mock_provider):
    """parse_response must raise ValueError on empty string."""
    service = SummarizeService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("")


def test_parse_response_returns_correct_type(mock_provider, summarize_mock_response):
    """parse_response must return a SummarizeResponse instance."""
    mock_provider.response = summarize_mock_response
    service = SummarizeService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert isinstance(result, SummarizeResponse)


def test_parse_response_has_expected_fields(mock_provider, summarize_mock_response):
    """Response object must have all required fields populated."""
    mock_provider.response = summarize_mock_response
    service = SummarizeService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert hasattr(result, "short_summary")
    assert hasattr(result, "detailed_summary")
    assert hasattr(result, "key_points")


def test_validate_input_strips_whitespace(mock_provider):
    service = SummarizeService(provider=mock_provider)
    request = SummarizeRequest(text="  Some text with whitespace.  ")
    result = service.validate_input(request)
    assert result.text == "Some text with whitespace."


def test_build_prompt_contains_text(mock_provider):
    service = SummarizeService(provider=mock_provider)
    from app.services.summarize.models import SummarizeInput

    validated = SummarizeInput(text="Test content for prompt.")
    prompt = service.build_prompt(validated)
    assert "Test content for prompt." in prompt


def test_build_prompt_includes_max_length_when_set(mock_provider):
    service = SummarizeService(provider=mock_provider)
    from app.services.summarize.models import SummarizeInput

    validated = SummarizeInput(text="Some text.", max_length=100)
    prompt = service.build_prompt(validated)
    assert "100" in prompt


# ── Pipeline integration tests ─────────────────────────────────────────────────


def test_pipeline_execute_returns_response(mock_provider, summarize_mock_response):
    """
    Full pipeline run with mock provider must return a valid response.

    TODO (Associate 1):
        - This test calls the full pipeline end to end
        - It will pass once your service methods are all implemented
        - Do not modify this test
    """
    mock_provider.response = summarize_mock_response
    from app.services.summarize.service import SummarizeService

    pipeline = SummarizePipeline(service=SummarizeService(provider=mock_provider))
    request = SummarizeRequest(
        text="Artificial intelligence is transforming the world in many ways."
    )
    result = pipeline.execute(request)
    assert isinstance(result, SummarizeResponse)


def test_pipeline_provider_receives_prompt(mock_provider, summarize_mock_response):
    """
    After pipeline execution, the mock provider should have recorded
    the prompt that was sent to it.

    TODO (Associate 1):
        - Verifies build_prompt was called and produced a non-empty string
    """
    mock_provider.response = summarize_mock_response
    from app.services.summarize.service import SummarizeService

    pipeline = SummarizePipeline(service=SummarizeService(provider=mock_provider))
    request = SummarizeRequest(
        text="Artificial intelligence is transforming the world in many ways."
    )
    pipeline.execute(request)
    assert mock_provider.last_prompt is not None
    assert len(mock_provider.last_prompt) > 0


def test_pipeline_propagates_value_error(mock_provider):
    """
    Pipeline must propagate ValueError from validate_input upward.
    The controller catches it — the pipeline itself should not swallow it.
    """
    from app.services.summarize.service import SummarizeService

    pipeline = SummarizePipeline(service=SummarizeService(provider=mock_provider))
    request = SummarizeRequest(text="Hi")
    with pytest.raises(ValueError):
        pipeline.execute(request)
