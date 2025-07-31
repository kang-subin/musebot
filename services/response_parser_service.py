from langchain.output_parsers import PydanticOutputParser
from pydantic import ValidationError
from pydantic_core import ValidationError as ValidationErrorV2
from core.log_service import LogService
from core.models import BaseModel
from typing import Type

class ResponseParserService:
    def __init__(self, max_retries: int = 2):
        self.logger = LogService()
        self.max_retries = max_retries

    def parse_llm_response(
        self,
        raw_llm_output: str,
        pydantic_model_type: Type[BaseModel],
        context_intent: str = "unknown"
    ) -> dict:
        parser = PydanticOutputParser(pydantic_object=pydantic_model_type)
        self.logger.info(f"[Parser] Parsing intent '{context_intent}' with model '{pydantic_model_type.__name__}'")

        for attempt in range(1, self.max_retries + 2):
            try:
                parsed = parser.parse(raw_llm_output)
                self.logger.info(f"[Parser] Success on attempt {attempt}")
                return parsed.dict()

            except (ValidationError, ValidationErrorV2) as e:
                self.logger.error(f"[Parser] Validation error on attempt {attempt}: {e.__class__.__name__}")
                if attempt > self.max_retries:
                    break

            except Exception as e:
                self.logger.error(f"[Parser] Unexpected error: {e.__class__.__name__}")
                break

        self.logger.error(f"[Parser] Parsing failed after {self.max_retries + 1} attempts. Using fallback.")
        return self._fallback_response(context_intent)

    def _fallback_response(self, intent: str) -> dict:
        return {
            "response_text": "죄송합니다. 요청을 이해하지 못했습니다. 다른 표현으로 다시 시도해주시겠어요?",
            "detected_intent": intent,
            "confidence_score": 0.0,
            "error_type": "PARSING_FAILED_FALLBACK",
            "error_message": "LLM 응답 파싱 실패로 인한 통일된 폴백 메시지."
        }
