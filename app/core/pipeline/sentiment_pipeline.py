"""Sentiment pipeline — orchestrates the sentiment analysis flow."""

from app.api.v1.schemas.requests.sentiment import SentimentRequest
from app.api.v1.schemas.responses.sentiment import SentimentResponse
from app.core.interfaces.sentiment_interface import SentimentServiceInterface
from app.core.pipeline.base_pipeline import BasePipeline
from app.logging import get_logger

logger = get_logger(__name__)


class SentimentPipeline(BasePipeline):
    """
    Orchestrates the full sentiment analysis flow.

    Depends only on SentimentServiceInterface.
    """

    def __init__(self, service: SentimentServiceInterface) -> None:
        self.service = service

    def execute(self, request: SentimentRequest) -> SentimentResponse:
        """
        Run the sentiment analysis pipeline.

        Steps:
            1. Validate and normalise the incoming request
            2. Build the LLM prompt from validated input
            3. Call the LLM provider and get the raw response
            4. Parse the raw response into a structured SentimentResponse

        Args:
            request: Validated SentimentRequest from the controller.

        Returns:
            SentimentResponse with sentiment label, score, reasoning, and emotions.
        """
        logger.info("SentimentPipeline: starting execution")

        validated = self.service.validate_input(request)
        prompt = self.service.build_prompt(validated)
        raw = self.service.provider.generate(prompt)
        result = self.service.parse_response(raw)

        logger.info("SentimentPipeline: execution complete")
        return result
