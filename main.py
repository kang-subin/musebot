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

        result = chat_service.process_message(user_input)

        print("\n[Result]")
        for key, value in result.items():
            print(f"{key}: {value}")
        print("\n")

if __name__ == "__main__":
    main()
