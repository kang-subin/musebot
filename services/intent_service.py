from core.llm_service import LLMService

class IntentService:
    def __init__(self):
        self.llm_service = LLMService()
        self.intent_keywords = {
            "translation": ["번역", "translate"],
            "summarization": ["요약", "summarize"],
            "date_calculation": ["며칠", "d-day", "디데이"],
            "mental_care" : ["감정", "sentiment", "기분"]
        }
        self.intent_mapping = {
            "translation": ["translation", "번역"],
            "summarization": ["summarization", "요약"],
            "date_calculation": ["date", "며칠", "d-day"],
            "mental_care" : ["감정", "sentiment", "기분"]
        }

    def detect_intent(self, user_input: str) -> str:
        for intent, keywords in self.intent_keywords.items():
            if any(kw.lower() in user_input.lower() for kw in keywords):
                return intent
            
   
            
        prompt = f"""
        아래 문장의 의도를 분류하세요.
        가능한 카테고리:
        translation, summarization, date_calculation, mental_care, general_chat
        문장: "{user_input}"
        """
        
        print("[2차 의도 검증:",user_input)
        
        llm_result = self.llm_service.run(prompt)
        return self._normalize_intent(llm_result)
    

    def _normalize_intent(self, text: str) -> str:
        text = text.lower()
        for intent, keywords in self.intent_mapping.items():
            if any(kw in text for kw in keywords):
                return intent
        return "general_chat"
