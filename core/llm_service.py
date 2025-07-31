from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from config.settings import GEMINI_API_KEY, DEFAULT_LLM_MODEL


class LLMService:
    def __init__(self, model: str = None):
        self.model = model or DEFAULT_LLM_MODEL
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=GEMINI_API_KEY,
            temperature=0.7
        )

    def run(self, prompt: str) -> str:
        try:
            messages = [HumanMessage(content=prompt)]
            # invoke() 사용 권장
            response = self.llm.invoke(messages)
            return response.content  # content가 str 형태로 반환됨
        except Exception as e:
            return f"🚨 LLM 호출 중 오류 발생: {str(e)}"
