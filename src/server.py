# server_dummy.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 요청 데이터 모델 (선택)
class Query(BaseModel):
    question: str = None  # optional

# 더미 마크다운 문자열
DUMMY_MARKDOWN = """
# 제목
여기는 **강조된 텍스트**입니다.

- 리스트 항목 1
- 리스트 항목 2

[링크](https://example.com)
"""

@app.get("/dummy")
def get_dummy():
    return {"markdown": DUMMY_MARKDOWN}

@app.post("/dummy-ask")
def post_dummy(query: Query):
    # 질문은 받아서 그냥 echo 또는 더미 응답
    return {
        "question": query.question,
        "markdown": f"답변: {query.question}\n\n{DUMMY_MARKDOWN}"
    }

@app.get("/hello")
def hello():
    return {"message": "Hello, 일병쥐피티 😎"}