from typing import Type
from services.intent_service import IntentService
from services.prompt_service import PromptService
from services.tool_service import ToolService
from services.response_parser_service import ResponseParserService
from core.llm_service import LLMService
from core.models import (
    ChatResponse,
    TranslationResponse,
    SummarizationResponse,
    MentalCareResponse,
    BaseModel
)
from langchain.output_parsers import PydanticOutputParser


class ChatService:
    def __init__(self):
        self.intent_service = IntentService()
        self.prompt_service = PromptService()
        self.tool_service = ToolService()
        self.llm_service = LLMService()
        self.parser_service = ResponseParserService()
        self.model_map = {
            "translation": TranslationResponse,
            "summarization": SummarizationResponse,
            "sentiment_analysis": MentalCareResponse
        }

    def process_message(self, user_input: str) -> dict:
        intent = self.intent_service.detect_intent(user_input)

        if intent == "date_calculation":
            return {
                "response_text": self.tool_service.calculate_days_from_text(user_input),
                "detected_intent": intent,
                "confidence_score": 1.0
            }

        prompt_template = self.prompt_service.get_prompt(intent)
        if not prompt_template:
            return {
                "response_text": "죄송합니다. 해당 요청을 처리할 수 없습니다.",
                "detected_intent": intent,
                "confidence_score": 0.0
            }

        model_type: Type[BaseModel] = self.model_map.get(intent, ChatResponse)
        parser = PydanticOutputParser(pydantic_object=model_type)
        format_instructions = parser.get_format_instructions()

        processed_prompt_template_content = prompt_template.format(user_input=user_input)

        final_prompt = (
            f"{processed_prompt_template_content}\n\n"
            f"{format_instructions}"
        )

        raw_output = self.llm_service.run(final_prompt)
        parsed_result = self.parser_service.parse_llm_response(
            raw_llm_output=raw_output,
            pydantic_model_type=model_type,
            context_intent=intent
        )

        return parsed_result
