import json
from services.chat_service import ChatService
import services.callbacks.stream_handler as sh
import inspect

print("[DEBUG] StreamHandler file path:", sh.__file__)
print("[DEBUG] StreamHandler init signature:", inspect.signature(sh.StreamHandler))


def main():
    # 토큰 나올 때마다 호출
    def on_chunk(chunk: str):
        print(chunk, end="", flush=True)  # 실시간 출력

    # 전체 토큰이 끝나면 호출
    def on_complete(full_text: str):
        print("\n\n[STREAM COMPLETE]")
        print(full_text)  # 전체 결과 한 번 더 출력

    # 콜백을 ChatService에 전달
    chat_service = ChatService(
        on_chunk=on_chunk,
        on_complete=on_complete
    )

    print("=== Chat Service Test ===")
    print("종료하려면 'exit' 입력\n")

    while True:
        user_input = input("\nUser: ")

        if user_input.lower() == "exit":
            print("종료합니다.")
            break

        # 메시지 처리 → 스트리밍 출력은 콜백에서 바로 실행됨
        result, prompt_used = chat_service.process_message(user_input)

        if prompt_used:
            print("\n[DEBUG] Prompt Used:")
            print(prompt_used)

        print("\n[RESULT]")
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
