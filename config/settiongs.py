import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gemini-pro")
DATABASE_URL = os.getenv("DATABASE_URL", None)
DEFAULT_LANGUAGE = "ko"
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

if not GEMINI_API_KEY:
    raise ValueError("🚨 [환경변수 오류] GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

if DEBUG_MODE:
    print("[DEBUG] GEMINI_API_KEY 로드 완료:", GEMINI_API_KEY[:5] + "****")
    print("[DEBUG] DEFAULT_LLM_MODEL:", DEFAULT_LLM_MODEL)
    print("[DEBUG] DATABASE_URL:", DATABASE_URL)
