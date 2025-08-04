import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from services.chat_service import ChatService
import services.callbacks.stream_handler as sh
import inspect

print("[DEBUG] StreamHandler file path:", sh.__file__)
print("[DEBUG] StreamHandler init signature:", inspect.signature(sh.StreamHandler))


def main():
    def on_chunk(chunk: str):
     print(f"[CHUNK] {repr(chunk)}\n", end="")


    def on_complete(full_text: str):
        print("\n\n[STREAM COMPLETE]")
        print(full_text)

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

        result, prompt_used = chat_service.process_message(user_input)

        if prompt_used:
            print("\n[DEBUG] Prompt Used:")
            print(prompt_used)

        print("\n[RESULT]")
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
