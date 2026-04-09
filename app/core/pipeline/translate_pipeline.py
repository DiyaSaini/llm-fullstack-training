"""Translate pipeline — orchestrates the translation flow."""

from app.api.v1.schemas.requests.translate import TranslateRequest
from app.api.v1.schemas.responses.translate import TranslateResponse
from app.core.interfaces.translate_interface import TranslateServiceInterface
from app.core.pipeline.base_pipeline import BasePipeline
from app.logging import get_logger

logger = get_logger(__name__)


class TranslatePipeline(BasePipeline):
    """
    Orchestrates the full translation flow.

    Depends only on TranslateServiceInterface.
    """

    def __init__(self, service: TranslateServiceInterface) -> None:
        self.service = service

    def execute(self, request: TranslateRequest) -> TranslateResponse:
        """
        Run the translation pipeline.

        Steps:
            1. Validate and normalise the incoming request
            2. Build the LLM prompt from validated input
            3. Call the LLM provider and get the raw response
            4. Parse the raw response into a structured TranslateResponse

        Args:
            request: Validated TranslateRequest from the controller.

        Returns:
            TranslateResponse with detected language, target language,
            translated text, and confidence score.
        """
        logger.info("TranslatePipeline: starting execution")

        validated = self.service.validate_input(request)
        prompt = self.service.build_prompt(validated)
        raw = self.service.provider.generate(prompt)
        result = self.service.parse_response(raw)

        logger.info("TranslatePipeline: execution complete")
        return result
