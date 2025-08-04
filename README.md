# 🤖 뮤즈봇 - AI 업무 비서

---

## 1. 프로젝트 소개

**뮤즈봇**은 아뮤즈(Amuz)의 ‘뮤즈’가 되어, 회사 업무 효율을 높이는 AI 업무 비서입니다.  
LangChain을 기반으로 LLM을 연동하여 **사용자 의도 분석 → 적절한 처리 → 구조화된 응답 제공**의 흐름을 구현했습니다.

**주요 기능**
- 번역 (Translation)
- 요약 (Summarization)
- 날짜 계산 (Date Calculation)
- 나라별 시각 조회 (Time Conversion)
- 감정 케어 (Mental Care)
- 일반 대화 (General Chat)

---

## 2. 기술 스택

| 구분 | 사용 기술 |
|------|----------|
| **언어** | Python 3.12.3 |
| **LLM** | Google Gemini Pro 1.5 Flash |
| **프레임워크** | LangChain |
| **UI** | Streamlit |
| **데이터 모델링** | Pydantic |
| **기타** | dateparser, pytz, queue |

---

## 3. 디렉터리 구조

```plaintext
musebot/
├── config/
│   └── settings.py
├── core/
│   └── models.py
├── infrastructure/
│   ├── db_service.py          # 프롬프트 DB 관리(미래 확장용)
│   ├── llm_service.py         # LLM 호출 래퍼
│   ├── log_service.py         # 파싱 실패 및 시스템 로그
├── prompts/
│   ├── translation.txt        # 번역 프롬프트
│   ├── summarization.txt      # 요약 프롬프트
│   ├── mental_care.txt        # 감정 케어 프롬프트
│   ├── time_conversion.txt    # 나라별 시각 변환 프롬프트
│   ├── date_calculation.txt   # 날짜 계산 프롬프트
│   └── general_chat.txt       # 일반 대화 프롬프트
├── services/
│   ├── chat_service.py        # 전체 챗봇 흐름 제어
│   ├── intent_service.py      # 의도 분석
│   ├── prompt_service.py      # 프롬프트 로딩(DB 또는 파일)
│   ├── tool_service.py        # 날짜/시간 툴
│   ├── response_parser_service.py # 응답 파싱
│   ├── callbacks/
│   │   └── stream_handler.py  # 스트리밍 콜백 핸들러
├── ui/
│   ├── app.py
│   └── styles.css
├── utils/
│   └── json_utils.py          # JSON 전처리 유틸
├── requirements.txt
├── .env.example               # 환경 변수 예시 파일
└── README.md
```

---

## 4. 시스템 아키텍처

```plaintext
[User]
   ↓
[Streamlit UI]
   ↓
[ChatService]
   ↓
 ┌───────────────┬───────────────┬───────────────┐
 │ IntentService │ ToolService   │ PromptService │
 │ (의도 분석)   │ (로컬 툴 실행)│ (프롬프트 선택)│
 └───────────────┴───────────────┴───────────────┘
   ↓
[LLMService] → Google Gemini API
   ↓
[ResponseParserService] → JSON 전처리 + Pydantic 파싱
   ↓
[결과 반환 + 스트리밍]
```

---

## 5.🎥 스트리밍 예시 (실시간 응답)
뮤즈봇은 사용자의 질문에 대해 LLM 응답을 실시간 스트리밍으로 제공합니다.
<p align="center">
  <img src="docs/screenshots/musebot.gif" alt="스트리밍 예시">
</p>

📌 요약 기능 (SummarizationResponse 모델 예시)
```
class SummarizationResponse(BaseModel):
    summary_main_text: str = Field(
        description="입력된 텍스트의 핵심 내용을 간결하게 요약한 결과."
    )
    key_bullet_points: Optional[List[str]] = Field(
        None,
        description="요약의 주요 핵심 내용들을 3~5가지의 핵심 불릿 포인트로 정리."
    )
    original_text_word_count: Optional[int] = Field(
        None,
        description="원문 텍스트의 대략적인 단어 수."
    )
    summary_text_word_count: Optional[int] = Field(
        None,
        description="요약된 텍스트의 대략적인 단어 수."
    )
```

---

## 🛠 6. 설치 및 실행 방법
**1)저장소 클론**
```
git clone https://github.com/kang-subin/musebot.git
cd musebot
```

**2)가상환경 생성 및 활성화**
```
# Mac / Linux
python -m venv venv
source venv/bin/activate  

# Windows
python -m venv venv
venv\Scripts\activate
```
**3)패키지 설치**
```
pip install -r requirements.txt
```
**4)환경 변수 설정**
프로젝트에는 .env.example 파일이 포함되어 있습니다.
이 파일을 복사하여 .env로 이름을 변경한 뒤, 실제 API Key를 입력하세요.
```
cp .env.example .env
```
**.env.example**
```
GEMINI_API_KEY= 💡 GEMINI_API_KEY 값만 입력하면 실행 가능
DEFAULT_LLM_MODEL=gemini-1.5-flash
DATABASE_URL=
DEFAULT_LANGUAGE=ko
DEBUG_MODE=True
ENV=development
```
**5)실행**
```
streamlit run ui/app.py
```

---

## 7. 설계 의도와 확장성

### **1) 의도 분석 최적화**
- **1차 분석:** 키워드 하드코딩(문자열 매칭) 방식으로 **LLM 호출 없이** 빠르게 판별  
- **2차 분석:** 1차 분석에서 판별 불가 시 **LLM 기반 분석**으로 전환  
- **효과:** 응답 속도 향상 및 LLM 호출 비용 절감

### **2) ToolService 활용**
- LLM 호출이 불필요한 **단순 날짜 계산 / 시간 변환 요청**은  
  Python 로직으로 처리하여 **LLM 호출 최소화**  
- **효과:** 처리 속도 향상 및 API 사용량 절감

### **3) DBService**
- 현재는 `prompts/` 디렉터리 내 `.txt` 파일에서 프롬프트를 로드  
- **미래 확장 시:**
  - 프롬프트를 **DB로 관리**하여 버전 관리, 다국어 지원, A/B 테스트 가능  
  - DB 전환 시 **코드 변경 최소화**를 위해 현재 구조에서 DBService를 설계

### **4) 로깅 서비스(LogService)**
- `ResponseParserService`에서 **파싱 실패** 및 **재시도 이력**을 로그 파일로 저장  
- **운영 시:** 로그 분석을 통해 오류 발생 패턴 파악 및 개선 가능  
- **유지보수:** 프롬프트 수정 및 예외 처리 보완 시 활용