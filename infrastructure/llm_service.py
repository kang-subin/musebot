from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from config.settings import GEMINI_API_KEY, DEFAULT_LLM_MODEL
from services.callbacks.stream_handler import StreamHandler


class LLMService:
    def __init__(self, model: str = None, streaming: bool = False, on_chunk=None, on_complete=None):
        self.model = model or DEFAULT_LLM_MODEL
        self.streaming = streaming

        callbacks = None
        if self.streaming:
            callbacks = [StreamHandler(
                on_chunk=on_chunk,
                on_complete=on_complete,
                flush_interval=0.05
            )]

        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=GEMINI_API_KEY,
            temperature=0.7,
            callbacks=callbacks
        )

    def run(self, prompt: str) -> str:
        try:
            messages = [HumanMessage(content=prompt)]
            if self.streaming:
                self.full_text = ""
                for chunk in self.llm.stream(messages):
                    token = chunk.content
                    self.full_text += token
                return self.full_text
            else:
                response = self.llm.invoke(messages)
                return response.content
        except Exception as e:
            return f"🚨 LLM 호출 중 오류 발생: {str(e)}"
        