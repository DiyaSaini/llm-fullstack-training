"""
Shared pytest fixtures.

The MockLLMProvider allows all tests to run without a real API key.
Each test that needs a specific LLM response should override the
`mock_response` fixture or patch `MockLLMProvider.generate` directly.

Usage in a test:
    def test_something(mock_provider, summarize_pipeline):
        # pipeline already uses mock_provider
        result = summarize_pipeline.execute(SummarizeRequest(text="hello world..."))
        assert result.short_summary != ""
"""

import json

import pytest

from app.providers.llm_provider import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    """
    Test double for BaseLLMProvider.

    Returns a configurable JSON string instead of calling any real API.
    Override `response` on the instance to control what get returned.
    """

    def __init__(self, response: str = "{}") -> None:
        self.response = response
        self.last_prompt: str | None = None  # inspect what prompt was built

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self.response


# ── Provider fixture ───────────────────────────────────────────────────────────


@pytest.fixture
def mock_provider() -> MockLLMProvider:
    """Returns a MockLLMProvider with an empty JSON response by default."""
    return MockLLMProvider(response="{}")


# ── Per-feature mock response fixtures ────────────────────────────────────────
# Each fixture returns a valid JSON string matching the expected LLM response
# shape for that feature. Associates should use these in their tests.


@pytest.fixture
def summarize_mock_response() -> str:
    return json.dumps(
        {
            "short_summary": "AI is transforming industries.",
            "detailed_summary": "Artificial intelligence is rapidly transforming multiple industries by automating tasks and enabling new capabilities.",
            "key_points": [
                "AI automates repetitive tasks",
                "Machine learning enables pattern recognition",
                "Natural language processing powers chatbots",
            ],
        }
    )


@pytest.fixture
def classify_mock_response() -> str:
    return json.dumps(
        {
            "category": "technology",
            "confidence": 0.95,
            "reasoning": "The text discusses artificial intelligence and computing.",
        }
    )


@pytest.fixture
def keywords_mock_response() -> str:
    return json.dumps(
        {
            "keywords": [
                {"word": "artificial intelligence", "relevance_score": 0.98},
                {"word": "machine learning", "relevance_score": 0.91},
                {"word": "automation", "relevance_score": 0.85},
            ]
        }
    )


@pytest.fixture
def sentiment_mock_response() -> str:
    return json.dumps(
        {
            "sentiment": "positive",
            "score": 0.87,
            "reasoning": "The text expresses enthusiasm and satisfaction.",
            "emotions": ["joy", "excitement"],
        }
    )


@pytest.fixture
def qa_mock_response() -> str:
    return json.dumps(
        {
            "answer": "Guido van Rossum created Python.",
            "confidence": 0.99,
            "is_answerable": True,
        }
    )


@pytest.fixture
def paraphrase_mock_response() -> str:
    return json.dumps(
        {
            "paraphrases": [
                {
                    "tone": "formal",
                    "text": "The utilisation of advanced methodologies has yielded significant outcomes.",
                },
                {
                    "tone": "casual",
                    "text": "Using advanced methods has worked out really well.",
                },
            ]
        }
    )


@pytest.fixture
def translate_mock_response() -> str:
    return json.dumps(
        {
            "detected_language": "French",
            "target_language": "English",
            "translated_text": "Hello, how are you?",
            "confidence": 0.99,
        }
    )
