from services.intent_service import IntentService

def main():
    intent_service = IntentService()

    while True:
        user_input = input("\n사용자 입력 (종료하려면 'exit'): ")
        if user_input.lower() == "exit":
            break

        intent = intent_service.detect_intent(user_input)
        print(f"[의도 분석 결과] {intent}")

if __name__ == "__main__":
    main()