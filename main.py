import json
from services.chat_service import ChatService

def main():
    chat_service = ChatService()

    print("=== Chat Service Test ===")
    print("종료하려면 'exit' 입력\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            print("종료합니다.")
            break

        result, prompt_used = chat_service.process_message(user_input)

        if prompt_used:
            print("[DEBUG] Prompt Used:")
            print(prompt_used)

        print("\n[RESULT]")
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
