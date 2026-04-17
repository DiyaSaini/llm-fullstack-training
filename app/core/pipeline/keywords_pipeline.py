"""Keywords pipeline — orchestrates the keyword extraction flow."""

from app.api.v1.schemas.requests.keywords import KeywordsRequest
from app.api.v1.schemas.responses.keywords import KeywordsResponse
from app.core.interfaces.keywords_interface import KeywordsServiceInterface
from app.core.pipeline.base_pipeline import BasePipeline
from app.logging import get_logger

logger = get_logger(__name__)


class KeywordsPipeline(BasePipeline):
    """
    Orchestrates the full keyword extraction flow.

    Depends only on KeywordsServiceInterface.
    """

    def __init__(self, service: KeywordsServiceInterface) -> None:
        self.service = service

    def execute(self, request: KeywordsRequest) -> KeywordsResponse:
        
        # Executes the full keyword extraction flow
        
        logger.info("KeywordsPipeline: starting execution")

        validated = self.service.validate_input(request)
        prompt = self.service.build_prompt(validated)
        raw = self.service.provider.generate(prompt)
        result = self.service.parse_response(raw)

        logger.info("KeywordsPipeline: execution complete")
        return result
