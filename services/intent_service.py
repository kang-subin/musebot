from infrastructure.llm_service import LLMService

class IntentService:
    def __init__(self):
        self.llm_service = LLMService()
        self.intent_keywords = {
            "translation": ["번역", "translate"],
            "summarization": ["요약", "summarize"],
            "date_calculation": ["며칠", "d-day", "디데이", "언제까지", "며칠 후", "며칠 전"],
            "time_conversion": ["시간", "몇 시", "몇시", "current time", "time in", "지금 시각", "현재 시각"],
            "mental_care": ["감정", "sentiment", "기분"]
        }
        
        self.intent_list = [
            "translation",
            "summarization",
            "date_calculation",
            "time_conversion",
            "mental_care",
            "general_chat"
        ]


    def detect_intent(self, user_input: str) -> str:
        for intent, keywords in self.intent_keywords.items():
            if any(kw.lower() in user_input.lower() for kw in keywords):
                return intent
               
        prompt = f"""
        당신은 사용자의 입력 문장을 아래 6가지 의도(Intent) 중 하나로 분류하는 전문가입니다.

        의도 종류:
        1. translation: 문장을 다른 언어로 번역 요청
        2. summarization: 긴 내용을 간단히 요약 요청
        3. date_calculation: 날짜 차이 계산, 특정 날짜까지 남은 일수/경과 일수
        4. time_conversion: 특정 도시·지역의 현재 시각 요청
        5. mental_care: 감정 위로·공감·정신적 도움 요청
        6. general_chat: 위에 해당하지 않는 일반 대화

        판단 규칙:
        - 감정/위로 요청(예: "우울해", "위로해줘", "힘들어") → mental_care
        - 번역 관련 키워드("번역", "translate", "~로 번역") → translation
        - 요약 요청("요약", "정리해줘") → summarization
        - 날짜 계산 관련 표현("며칠 남았어", "며칠 전", "기한", "D-Day") → date_calculation
        - 시각 변환 관련 표현(도시명 + "시간", "현재 시각") → time_conversion
        - 그 외 모든 경우 → general_chat

        출력 형식 규칙:
        - 반드시 아래 단어 중 **하나만** 출력
        - 추가 설명·문장·기호 절대 포함 금지

        가능한 값:
        translation
        summarization
        date_calculation
        time_conversion
        mental_care
        general_chat

        사용자 입력: "{user_input}"
        """
        
        print("[2차 의도 검증]")
        
        llm_result = self.llm_service.run(prompt)
        return self._normalize_intent(llm_result)
    
    def _normalize_intent(self, text: str) -> str:
        text = text.lower()
        if text in self.intent_list:
            return text
        
        for intent in self.intent_list:
            if intent in text:
                return intent
        return "general_chat"