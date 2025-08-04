import time
import threading
from langchain.callbacks.base import BaseCallbackHandler
from typing import Callable


class StreamHandler(BaseCallbackHandler):
    def __init__(
        self,
        on_chunk: Callable[[str], None],
        on_complete: Callable[[str], None],
        flush_interval=0.05
    ):
        self.on_chunk = on_chunk
        self.on_complete = on_complete
        self.flush_interval = flush_interval

        self.lock = threading.Lock()
        self.reset()

    def reset(self):
        with self.lock:
            self.buffer = ""
            self.full_text = ""
        self.running = True
        self.thread = threading.Thread(target=self._flush_loop, daemon=True)
        self.thread.start()

    def on_llm_start(self, *args, **kwargs):
        self.reset()

    def on_llm_new_token(self, token: str, **kwargs):
        with self.lock:
            self.buffer += token
            self.full_text += token

    def _flush_loop(self):
        while self.running:
            time.sleep(self.flush_interval)
            with self.lock:
                if self.buffer.strip():
                    chunk = self.buffer
                    self.buffer = ""
                    if self.on_chunk:
                        self.on_chunk(chunk)

    def on_llm_end(self, *args, **kwargs):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()

        if self.on_complete:
            self.on_complete(self.full_text)
