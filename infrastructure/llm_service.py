from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from config.settings import GEMINI_API_KEY, DEFAULT_LLM_MODEL
from services.callbacks.stream_handler import StreamHandler


class LLMService:
    def __init__(self, model: str = None, streaming: bool = False):
        self.model = model or DEFAULT_LLM_MODEL
        self.streaming = streaming
        
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=GEMINI_API_KEY,
            temperature=0.7,
            streaming=self.streaming,
            callbacks=[StreamHandler()] if self.streaming else None
        )

    def run(self, prompt: str) -> str:
        try:
            messages = [HumanMessage(content=prompt)]
            if self.streaming:
                self.llm.invoke(messages)
                return "" 
            else:
                response = self.llm.invoke(messages)
                return response.content
        except Exception as e:
            return f"🚨 LLM 호출 중 오류 발생: {str(e)}"
        