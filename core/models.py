from pydantic import BaseModel, Field
from typing import List, Optional

class ChatResponse(BaseModel):
    response_text: str = Field(description="사용자에게 전달할 챗봇의 최종 답변 텍스트.")
    detected_intent: str = Field(description="시스템이 분류한 사용자의 주된 의도 (예: 'general_chat', 'translation').")
    confidence_score: float = Field(description="시스템이 파악한 의도 분류의 신뢰도 (0.0~1.0).")

class TranslationResponse(BaseModel):
    original_input: str = Field(description="번역을 요청받은 원문 텍스트.")
    translated_output: str = Field(description="요청된 언어로 번역된 최종 텍스트.")
    inferred_source_lang: Optional[str] = Field(None, description="LLM이 추론한 원문의 언어 코드 (예: 'ko', 'en', 'auto').")
    target_lang_code: Optional[str] = Field(None, description="번역된 결과물의 목표 언어 코드 (예: 'en', 'ja').")

class SummarizationResponse(BaseModel):
    summary_main_text: str = Field(description="입력된 텍스트의 핵심 내용을 간결하게 요약한 결과.")
    key_bullet_points: Optional[List[str]] = Field(
        None, description="요약의 주요 핵심 내용들을 3~5가지의 핵심 불릿 포인트로 정리."
    )
    original_text_word_count: Optional[int] = Field(None, description="원문 텍스트의 대략적인 단어 수.")
    summary_text_word_count: Optional[int] = Field(None, description="요약된 텍스트의 대략적인 단어 수.")

class MentalCareResponse(BaseModel):
    user_emotional_state: str = Field(description="사용자가 표현한 주된 감정 상태 (예: '피곤함', '좌절', '스트레스', '희망').")
    empathetic_reflection: str = Field(description="사용자의 감정에 공감하고 이해함을 보여주는 위로의 메시지.")
    encouragement_for_action: str = Field(description="긍정적인 전환을 위한 작지만 구체적인 행동이나 사고방식을 격려하는 메시지.")
