"""QA pipeline — orchestrates the question & answer flow."""

from app.api.v1.schemas.requests.qa import QARequest
from app.api.v1.schemas.responses.qa import QAResponse
from app.core.interfaces.qa_interface import QAServiceInterface
from app.core.pipeline.base_pipeline import BasePipeline
from app.logging import get_logger

logger = get_logger(__name__)


class QAPipeline(BasePipeline):
    """
    Orchestrates the full Q&A flow.

    Depends only on QAServiceInterface.
    """

    def __init__(self, service: QAServiceInterface) -> None:
        self.service = service

    def execute(self, request: QARequest) -> QAResponse:
        """
        Run the Q&A pipeline.

        Steps:
            1. Validate and normalise the incoming request
            2. Build the LLM prompt from validated input
            3. Call the LLM provider and get the raw response
            4. Parse the raw response into a structured QAResponse

        Args:
            request: Validated QARequest from the controller.

        Returns:
            QAResponse with answer, confidence, and is_answerable flag.
        """
        logger.info("QAPipeline: starting execution")

        validated = self.service.validate_input(request)
        prompt = self.service.build_prompt(validated)
        raw = self.service.provider.generate(prompt)
        result = self.service.parse_response(raw)

        logger.info("QAPipeline: execution complete")
        return result
