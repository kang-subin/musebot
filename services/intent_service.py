from core.llm_service import LLMService

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
        self.intent_mapping = {
            "translation": ["translation", "번역"],
            "summarization": ["summarization", "요약"],
            "date_calculation": ["date", "며칠", "d-day"],
            "time_conversion": ["time", "timezone", "현재 시각", "몇 시"],
            "mental_care": ["감정", "sentiment", "기분"]
        }

    def detect_intent(self, user_input: str) -> str:
        for intent, keywords in self.intent_keywords.items():
            if any(kw.lower() in user_input.lower() for kw in keywords):
                return intent
            
        prompt = f"""
        당신은 사용자의 입력 문장을 읽고, 그 문장이 어떤 의도(Intent)에 속하는지 분류하는 전문가입니다.
        의도는 아래 6가지 중 하나입니다.

        1. translation: 문장을 다른 언어로 번역 요청하는 경우
        2. summarization: 긴 내용을 간단하게 요약 요청하는 경우
        3. date_calculation: 오늘을 기준으로 날짜 차이 계산, 특정 날짜까지 남은 일수, 과거/미래 날짜를 묻는 경우
        4. time_conversion: 특정 도시/지역의 현재 시각을 묻는 경우
        5. mental_care: 사용자가 감정적 위로, 공감, 정신적 도움을 필요로 하는 경우
        6. general_chat: 위의 카테고리에 해당하지 않는 일반 대화

        ---

        판단 규칙:
        - 감정/위로 요청은 반드시 mental_care로 분류합니다. 예: "기분이 너무 우울해", "위로해줘", "마음이 힘들어"
        - 번역 요청은 문장에 '번역', 'translate', '~로 번역' 같은 표현이 있는 경우 translation
        - 요약 요청은 "요약", "정리해줘"가 포함되면 summarization
        - 날짜 계산은 '며칠 남았어', '며칠 전이야', '기한', 'D-Day' 등의 표현이 있으면 date_calculation
        - 시각 변환은 특정 도시 이름 + '시간', '현재 시각'이 포함되면 time_conversion
        - 그 외는 general_chat

        ---

        예시:
        - "기분이 너무 우울해. 위로 좀 해줄래?" → mental_care
        - "영어로 번역해줘" → translation
        - "이 내용 간단히 정리해줘" → summarization
        - "내 생일까지 며칠 남았어?" → date_calculation
        - "뉴욕 현재 시각이 몇 시야?" → time_conversion
        - "오늘 저녁 뭐 먹을까?" → general_chat

        ---

        사용자 입력: "{user_input}"
        위 문장의 의도를 위 6가지 중 하나로만 출력하세요.
        """
        print("[2차 의도 검증]:", user_input)
        llm_result = self.llm_service.run(prompt)
        return self._normalize_intent(llm_result)
    
    def _normalize_intent(self, text: str) -> str:
        text = text.lower()
        for intent, keywords in self.intent_mapping.items():
            if any(kw in text for kw in keywords):
                return intent
        return "general_chat"
