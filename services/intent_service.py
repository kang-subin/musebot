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
        아래 문장의 의도를 분류하세요.
        규칙:
        - 날짜가 명시되어 있고, 오늘 기준으로 미래 또는 과거를 비교하거나 남은 기간, 며칠 전/후, 기한 등을 묻는 경우: date_calculation
        - 특정 도시/지역과 함께 현재 시각을 묻는 경우: time_conversion
        - 번역 요청: translation
        - 요약 요청: summarization
        - 감정/위로/멘탈 케어 요청: mental_care
        - 그 외는 general_chat
        가능한 카테고리:
        translation, summarization, date_calculation, time_conversion, mental_care, general_chat
        문장: "{user_input}"
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
