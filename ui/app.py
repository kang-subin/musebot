import sys
import os
import time
import streamlit as st
import queue

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.chat_service import ChatService

st.title("💬 뮤즈봇 - AI 업무 비서")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 기존 채팅 기록 출력
for msg in st.session_state["messages"]:
    role_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
    st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.markdown(f"<div class='user-bubble'>{user_input}</div>", unsafe_allow_html=True)

    # 🔹 Queue 생성 (토큰을 담을 곳)
    q = queue.Queue()

    def on_chunk(chunk: str):
        q.put(chunk)

    def on_complete(full_text: str):
        q.put(None)  # 스트리밍 종료 신호
        st.session_state["messages"].append({"role": "assistant", "content": full_text})

    # 🔹 제너레이터 함수
    def stream_generator():
        chat_service = ChatService(on_chunk=on_chunk, on_complete=on_complete)
        # 백그라운드에서 메시지 처리 시작
        import threading
        threading.Thread(target=chat_service.process_message, args=(user_input,)).start()

        # 큐에서 꺼내면서 yield
        while True:
            item = q.get()
            if item is None:
                break
            yield item

    # 🔹 스트리밍 출력
    st.write_stream(stream_generator()) 