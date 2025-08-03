from typing import Type, Callable
from services.intent_service import IntentService
from services.prompt_service import PromptService
from services.tool_service import ToolService, ToolResult
from services.response_parser_service import ResponseParserService
from infrastructure.llm_service import LLMService
from langchain.output_parsers import PydanticOutputParser
from utils.json_utils import extract_json_from_text
from core.models import (
    ChatResponse,
    TranslationResponse,
    SummarizationResponse,
    MentalCareResponse,
    TimeConversionResponse,
    DateCalculationResponse,
    BaseModel
)


class ChatService:
    def __init__(
        self,
        on_chunk: Callable[[str], None] = None,
        on_complete: Callable[[str], None] = None
    ):
        self.on_chunk = on_chunk
        self.on_complete = on_complete

        # 기본 서비스 초기화
        self.intent_service = IntentService()
        self.prompt_service = PromptService()
        self.tool_service = ToolService()
        self.parser_service = ResponseParserService()

        # LLM 서비스 초기화 (스트리밍 활성화)
        self.llm_service = LLMService(
            streaming=True,
            on_chunk=self.on_chunk,
            on_complete=self.on_complete
        )

        # 의도별 모델 매핑
        self.model_map = {
            "translation": TranslationResponse,
            "summarization": SummarizationResponse,
            "mental_care": MentalCareResponse,
            "time_conversion": TimeConversionResponse,
            "date_calculation": DateCalculationResponse
        }

    def process_message(self, user_input: str) -> dict:
        # 1. 의도 감지
        intent = self.intent_service.detect_intent(user_input)

        # 2. 툴 실행 (예: 시간 변환, 날짜 계산)
        tool_result: ToolResult | None = self.tool_service.execute_tool(intent, user_input)
        if tool_result and tool_result.success:
            return {
                "response_text": tool_result.message,
                "detected_intent": intent,
                "confidence_score": 1.0
            }, None

        # 3. 프롬프트 생성
        prompt_template = self.prompt_service.get_prompt(intent)
        if not prompt_template:
            return {
                "response_text": "죄송합니다. 해당 요청을 처리할 수 없습니다.",
                "detected_intent": intent,
                "confidence_score": 0.0
            }, None

        # 4. 응답 모델 선택
        model_type: Type[BaseModel] = self.model_map.get(intent, ChatResponse)
        parser = PydanticOutputParser(pydantic_object=model_type)
        format_instructions = parser.get_format_instructions()

        processed_prompt_template_content = prompt_template.format(user_input=user_input)
        final_prompt = f"{processed_prompt_template_content}\n\n{format_instructions}"

        # 5. LLM 실행
        raw_output = self.llm_service.run(final_prompt)

        # 6. JSON 추출
        extracted_json = extract_json_from_text(raw_output)

        # 7. 파싱
        parsed_result = self.parser_service.parse_llm_response(
            raw_llm_output=raw_output or extracted_json,
            pydantic_model_type=model_type,
            context_intent=intent
        )

        return parsed_result, processed_prompt_template_content
