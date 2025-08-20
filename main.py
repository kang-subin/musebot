from fastapi import FastAPI
from api.routers.chat_router import router as chat_router

app = FastAPI()

app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# todo: 리턴 값 튜플 <> 딕셔너리 구조 차이 때문에 500 에러 발생 이거 수정하고 notion 정리 해둔 다음 방식 진행하기
# 뮤즈봇에 db (회사에 필요한 정보 넣어서) 이걸 분석해서 뿌려주는 형식으로 만들어 보기 근데 mssql 로 진행해보기
