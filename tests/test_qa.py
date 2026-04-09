"""
Tests for the qa feature.

ASSOCIATE 5 — implement the tests marked with TODO.
The fixtures in conftest.py give you a MockLLMProvider so tests
never call the real Gemini API.

Run just these tests:
    pytest tests/test_qa.py -v
"""

import pytest

from app.api.v1.schemas.requests.qa import QARequest
from app.api.v1.schemas.responses.qa import QAResponse
from app.core.pipeline.qa_pipeline import QAPipeline
from app.services.qa.service import QAService

# ── Service unit tests ─────────────────────────────────────────────────────────


def test_validate_input_raises_on_empty_text(mock_provider):
    """validate_input must raise ValueError when text is empty or whitespace."""
    service = QAService(provider=mock_provider)
    request = QARequest(context="  ", question="Who created Python?")
    with pytest.raises(ValueError):
        service.validate_input(request)


def test_parse_response_raises_on_invalid_json(mock_provider):
    """parse_response must raise ValueError when the LLM returns non-JSON."""
    service = QAService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("this is not json at all")


def test_parse_response_raises_on_empty_string(mock_provider):
    """parse_response must raise ValueError on empty string."""
    service = QAService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("")


def test_parse_response_returns_correct_type(mock_provider, qa_mock_response):
    """parse_response must return a QAResponse instance."""
    mock_provider.response = qa_mock_response
    service = QAService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert isinstance(result, QAResponse)


def test_parse_response_has_expected_fields(mock_provider, qa_mock_response):
    """Response object must have all required fields populated."""
    mock_provider.response = qa_mock_response
    service = QAService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert hasattr(result, "answer")
    assert hasattr(result, "confidence")
    assert hasattr(result, "is_answerable")


def test_validate_input_raises_on_empty_question(mock_provider):
    service = QAService(provider=mock_provider)
    request = QARequest(
        context="Some valid context text here.",
        question="   ",
    )
    with pytest.raises(ValueError):
        service.validate_input(request)


def test_build_prompt_contains_context_and_question(mock_provider):
    service = QAService(provider=mock_provider)
    from app.services.qa.models import QAInput

    validated = QAInput(context="Python context.", question="What is Python?")
    prompt = service.build_prompt(validated)
    assert "Python context." in prompt
    assert "What is Python?" in prompt


def test_is_answerable_is_bool(mock_provider, qa_mock_response):
    mock_provider.response = qa_mock_response
    service = QAService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert isinstance(result.is_answerable, bool)


# ── Pipeline integration tests ─────────────────────────────────────────────────


def test_pipeline_execute_returns_response(mock_provider, qa_mock_response):
    """
    Full pipeline run with mock provider must return a valid response.

    TODO (Associate 5):
        - This test calls the full pipeline end to end
        - It will pass once your service methods are all implemented
        - Do not modify this test
    """
    mock_provider.response = qa_mock_response
    from app.services.qa.service import QAService

    pipeline = QAPipeline(service=QAService(provider=mock_provider))
    request = QARequest(
        context="Python was created by Guido van Rossum and first released in 1991.",
        question="Who created Python?",
    )
    result = pipeline.execute(request)
    assert isinstance(result, QAResponse)


def test_pipeline_provider_receives_prompt(mock_provider, qa_mock_response):
    """
    After pipeline execution, the mock provider should have recorded
    the prompt that was sent to it.

    TODO (Associate 5):
        - Verifies build_prompt was called and produced a non-empty string
    """
    mock_provider.response = qa_mock_response
    from app.services.qa.service import QAService

    pipeline = QAPipeline(service=QAService(provider=mock_provider))
    request = QARequest(
        context="Python was created by Guido van Rossum and first released in 1991.",
        question="Who created Python?",
    )
    pipeline.execute(request)
    assert mock_provider.last_prompt is not None
    assert len(mock_provider.last_prompt) > 0


def test_pipeline_propagates_value_error(mock_provider):
    """
    Pipeline must propagate ValueError from validate_input upward.
    The controller catches it — the pipeline itself should not swallow it.
    """
    from app.services.qa.service import QAService

    pipeline = QAPipeline(service=QAService(provider=mock_provider))
    request = QARequest(context="  ", question="Who created Python?")
    with pytest.raises(ValueError):
        pipeline.execute(request)
