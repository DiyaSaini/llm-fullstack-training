"""
LLM Provider abstraction layer.

Defines the contract that ALL provider implementations must satisfy.
Services depend only on `BaseLLMProvider` — never on a concrete class.

To add a new provider (e.g. OpenAI):
    1. Subclass BaseLLMProvider
    2. Implement `generate()`
    3. Register it in deps.py
"""

from abc import ABC, abstractmethod

from app.logging import get_logger

logger = get_logger(__name__)


class LLMProviderError(Exception):
    """Raised when an LLM API call fails for any reason."""


class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM provider implementations.

    Every provider, regardless of the underlying model or vendor,
    must expose a single `generate` method that accepts a prompt
    string and returns the model's text response.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Send a prompt to the language model and return its response.

        Args:
            prompt: The fully constructed prompt string to send.

        Returns:
            The raw text response from the model.

        Raises:
            LLMProviderError: If the API call fails, times out,
                              or returns an unexpected response.
        """
        raise NotImplementedError


class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini implementation of BaseLLMProvider.

    Uses the `google-generativeai` SDK.
    The model name and API key are injected at construction time
    from config — this class never reads environment variables directly.

    Example:
        provider = GeminiProvider(
            model="gemini-2.0-flash",
            api_key=settings.llm_api_key,
        )
        response = provider.generate("Summarise the following text: ...")

    You are free to choose any Gemini model available on your API key.
    Recommended free-tier models:
        - gemini-2.0-flash          (fast, good quality)
        - gemini-2.0-flash-lite     (fastest, lower quota cost)
        - gemini-2.5-flash-preview  (best quality, higher latency)
    """

    def __init__(self, model: str, api_key: str) -> None:
        """
        Initialise the Gemini client.

        Args:
            model:   Gemini model identifier string.
            api_key: Google AI Studio API key.

        TODO:
            - Import google.generativeai
            - Call genai.configure(api_key=api_key)
            - Store self.model = model
            - Instantiate the GenerativeModel and store as self._client
        """
        raise NotImplementedError

    def generate(self, prompt: str) -> str:
        """
        Call the Gemini API with the given prompt.

        Args:
            prompt: Fully constructed prompt string.

        Returns:
            The model's text response as a plain string.

        Raises:
            LLMProviderError: Wraps any SDK or network exception.

        TODO:
            - Call self._client.generate_content(prompt)
            - Extract and return the text from the response
            - Wrap exceptions in LLMProviderError
            - Log the call at DEBUG level (never log the full prompt in production)
        """
        raise NotImplementedError
