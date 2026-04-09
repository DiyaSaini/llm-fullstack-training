"""
Tests for the paraphrase feature.

ASSOCIATE 6 — implement the tests marked with TODO.
The fixtures in conftest.py give you a MockLLMProvider so tests
never call the real Gemini API.

Run just these tests:
    pytest tests/test_paraphrase.py -v
"""

import pytest

from app.api.v1.schemas.requests.paraphrase import ParaphraseRequest
from app.api.v1.schemas.responses.paraphrase import ParaphraseResponse
from app.core.pipeline.paraphrase_pipeline import ParaphrasePipeline
from app.services.paraphrase.service import ParaphraseService

# ── Service unit tests ─────────────────────────────────────────────────────────


def test_validate_input_raises_on_empty_text(mock_provider):
    """validate_input must raise ValueError when text is empty or whitespace."""
    service = ParaphraseService(provider=mock_provider)
    request = ParaphraseRequest(text="  ", tones=["formal"])
    with pytest.raises(ValueError):
        service.validate_input(request)


def test_parse_response_raises_on_invalid_json(mock_provider):
    """parse_response must raise ValueError when the LLM returns non-JSON."""
    service = ParaphraseService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("this is not json at all")


def test_parse_response_raises_on_empty_string(mock_provider):
    """parse_response must raise ValueError on empty string."""
    service = ParaphraseService(provider=mock_provider)
    with pytest.raises(ValueError):
        service.parse_response("")


def test_parse_response_returns_correct_type(mock_provider, paraphrase_mock_response):
    """parse_response must return a ParaphraseResponse instance."""
    mock_provider.response = paraphrase_mock_response
    service = ParaphraseService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert isinstance(result, ParaphraseResponse)


def test_parse_response_has_expected_fields(mock_provider, paraphrase_mock_response):
    """Response object must have all required fields populated."""
    mock_provider.response = paraphrase_mock_response
    service = ParaphraseService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    assert hasattr(result, "paraphrases")


def test_validate_input_raises_on_invalid_tone(mock_provider):
    service = ParaphraseService(provider=mock_provider)
    request = ParaphraseRequest(
        text="Some valid text here.", tones=["formal", "pirate"]
    )
    with pytest.raises(ValueError):
        service.validate_input(request)


def test_validate_input_deduplicates_tones(mock_provider):
    service = ParaphraseService(provider=mock_provider)
    request = ParaphraseRequest(
        text="Some valid text.", tones=["formal", "formal", "casual"]
    )
    result = service.validate_input(request)
    assert len(result.tones) == len(set(result.tones))


def test_paraphrases_match_requested_tones(mock_provider, paraphrase_mock_response):
    mock_provider.response = paraphrase_mock_response
    service = ParaphraseService(provider=mock_provider)
    result = service.parse_response(mock_provider.response)
    tones = {p.tone for p in result.paraphrases}
    assert "formal" in tones
    assert "casual" in tones


# ── Pipeline integration tests ─────────────────────────────────────────────────


def test_pipeline_execute_returns_response(mock_provider, paraphrase_mock_response):
    """
    Full pipeline run with mock provider must return a valid response.

    TODO (Associate 6):
        - This test calls the full pipeline end to end
        - It will pass once your service methods are all implemented
        - Do not modify this test
    """
    mock_provider.response = paraphrase_mock_response
    from app.services.paraphrase.service import ParaphraseService

    pipeline = ParaphrasePipeline(service=ParaphraseService(provider=mock_provider))
    request = ParaphraseRequest(
        text="The utilisation of advanced methods has produced results.",
        tones=["formal", "casual"],
    )
    result = pipeline.execute(request)
    assert isinstance(result, ParaphraseResponse)


def test_pipeline_provider_receives_prompt(mock_provider, paraphrase_mock_response):
    """
    After pipeline execution, the mock provider should have recorded
    the prompt that was sent to it.

    TODO (Associate 6):
        - Verifies build_prompt was called and produced a non-empty string
    """
    mock_provider.response = paraphrase_mock_response
    from app.services.paraphrase.service import ParaphraseService

    pipeline = ParaphrasePipeline(service=ParaphraseService(provider=mock_provider))
    request = ParaphraseRequest(
        text="The utilisation of advanced methods has produced results.",
        tones=["formal", "casual"],
    )
    pipeline.execute(request)
    assert mock_provider.last_prompt is not None
    assert len(mock_provider.last_prompt) > 0


def test_pipeline_propagates_value_error(mock_provider):
    """
    Pipeline must propagate ValueError from validate_input upward.
    The controller catches it — the pipeline itself should not swallow it.
    """
    from app.services.paraphrase.service import ParaphraseService

    pipeline = ParaphrasePipeline(service=ParaphraseService(provider=mock_provider))
    request = ParaphraseRequest(text="  ", tones=["formal"])
    with pytest.raises(ValueError):
        pipeline.execute(request)
