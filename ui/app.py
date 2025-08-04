import sys
import os
import streamlit as st
import queue
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.chat_service import ChatService

st.set_page_config(
    page_title="뮤즈봇 - AI 업무 비서",
    page_icon="🤖",
    layout="wide"
)

css_file = Path(__file__).parent / "styles.css"
with open(css_file, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🤖 뮤즈봇</h1>
    <p>업무 효율을 위한 AI 업무 비서</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="intro-box">
    <div class="intro-content">
        <div class="bot-icon">🤖</div>
        <div class="intro-text">
            <h3>안녕하세요! 뮤즈봇입니다 👋</h3>
            <p>
            아뮤즈(Amuz)의 ‘뮤즈’가 되어 드릴 AI 업무 비서입니다.<br>
            번역, 요약, 일정·남은 기간 계산, 나라별 현재 시간 확인,<br>
            감정 케어까지 다양한 업무를 지원합니다.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

chat_container = st.container()

with chat_container:
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble"><div>{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble"><div>{msg["content"]}</div></div>', unsafe_allow_html=True)

user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with chat_container:
        st.markdown(f'<div class="user-bubble"><div>{user_input}</div></div>', unsafe_allow_html=True)

    temp_chat_service = ChatService()
    intent = temp_chat_service.intent_service.detect_intent(user_input)
    tool_result = temp_chat_service.tool_service.execute_tool(intent, user_input)

    if tool_result and tool_result.success:
        bot_response = tool_result.message
        st.session_state["messages"].append({"role": "assistant", "content": bot_response})
        with chat_container:
            st.markdown(f'<div class="bot-bubble"><div>{bot_response}</div></div>', unsafe_allow_html=True)
    else:
        q = queue.Queue()

        def on_chunk(chunk: str):
            q.put(chunk)

        def on_complete(full_text: str):
            q.put(None)
            st.session_state["messages"].append({"role": "assistant", "content": full_text})

        def stream_generator():
            chat_service = ChatService(on_chunk=on_chunk, on_complete=on_complete)
            import threading
            threading.Thread(target=chat_service.process_message, args=(user_input,)).start()
            while True:
                item = q.get()
                if item is None:
                    break
                yield item

        with chat_container:
            st.write_stream(stream_generator())
