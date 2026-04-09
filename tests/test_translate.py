"""
Tests for the translate feature.

ASSOCIATE 7 — implement the tests marked with TODO.
The fixtures in conftest.py give you a MockLLMProvider so tests
never call the real Gemini API.

Run just these tests:
    pytest tests/test_translate.py -v
"""

import pytest

from app.api.v1.schemas.requests.translate import TranslateRequest
from app.api.v1.schemas.responses.translate import TranslateResponse
from app.core.pipeline.translate_pipeline import TranslatePipeline
from app.services.translate.service import TranslateService

# ── Service unit tests ─────────────────────────────────────────────────────────


def test_validate_input_raises_on_empty_text(mock_provider):
    """validate_input must raise ValueError when text is empty or whitespace."""
    service = TranslateService(provider=mock_provider)
    request = TranslateRequest(text="  ", target_language="English")
    with pytest.raises(ValueError):
        service.validate_input(request)


def test_parse_response_raises_on_invalid_json(mock_provider):
    """parse_response must raise ValueError when the LLM returns non-JSON."""
    service = TranslateService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("this is not json at all")


def test_parse_response_raises_on_empty_string(mock_provider):
    """parse_response must raise ValueError on empty string."""
    service = TranslateService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("")


def test_parse_response_returns_correct_type(mock_provider, translate_mock_response):
    """parse_response must return a TranslateResponse instance."""
    mock_provider.response = translate_mock_response
    service = TranslateService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert isinstance(result, TranslateResponse)


def test_parse_response_has_expected_fields(mock_provider, translate_mock_response):
    """Response object must have all required fields populated."""
    mock_provider.response = translate_mock_response
    service = TranslateService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert hasattr(result, "detected_language")
    assert hasattr(result, "target_language")
    assert hasattr(result, "translated_text")
    assert hasattr(result, "confidence")


def test_validate_input_raises_on_empty_target_language(mock_provider):
    service = TranslateService(provider=mock_provider)
    request = TranslateRequest(text="Bonjour.", target_language="  ")
    with pytest.raises(ValueError):
        service.validate_input(request)


def test_build_prompt_contains_target_language(mock_provider):
    service = TranslateService(provider=mock_provider)
    from app.services.translate.models import TranslateInput

    validated = TranslateInput(text="Bonjour.", target_language="English")
    prompt = service.build_prompt(validated)
    assert "English" in prompt


def test_confidence_within_range(mock_provider, translate_mock_response):
    mock_provider.response = translate_mock_response
    service = TranslateService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert 0.0 <= result.confidence <= 1.0


# ── Pipeline integration tests ─────────────────────────────────────────────────


def test_pipeline_execute_returns_response(mock_provider, translate_mock_response):
    """
    Full pipeline run with mock provider must return a valid response.

    TODO (Associate 7):
        - This test calls the full pipeline end to end
        - It will pass once your service methods are all implemented
        - Do not modify this test
    """
    mock_provider.response = translate_mock_response
    from app.services.translate.service import TranslateService

    pipeline = TranslatePipeline(service=TranslateService(provider=mock_provider))
    request = TranslateRequest(
        text="Bonjour, comment allez-vous?", target_language="English"
    )
    result = pipeline.execute(request)
    assert isinstance(result, TranslateResponse)


def test_pipeline_provider_receives_prompt(mock_provider, translate_mock_response):
    """
    After pipeline execution, the mock provider should have recorded
    the prompt that was sent to it.

    TODO (Associate 7):
        - Verifies build_prompt was called and produced a non-empty string
    """
    mock_provider.response = translate_mock_response
    from app.services.translate.service import TranslateService

    pipeline = TranslatePipeline(service=TranslateService(provider=mock_provider))
    request = TranslateRequest(
        text="Bonjour, comment allez-vous?", target_language="English"
    )
    pipeline.execute(request)
    assert mock_provider.last_prompt is not None
    assert len(mock_provider.last_prompt) > 0


def test_pipeline_propagates_value_error(mock_provider):
    """
    Pipeline must propagate ValueError from validate_input upward.
    The controller catches it — the pipeline itself should not swallow it.
    """
    from app.services.translate.service import TranslateService

    pipeline = TranslatePipeline(service=TranslateService(provider=mock_provider))
    request = TranslateRequest(text="  ", target_language="English")
    with pytest.raises(ValueError):
        pipeline.execute(request)
