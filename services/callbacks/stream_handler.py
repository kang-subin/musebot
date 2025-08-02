from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(token, end="", flush=True)
