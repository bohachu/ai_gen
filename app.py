import os
import time

import openai
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import StreamingResponse

# 載入 .env 檔案
load_dotenv()
# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Define the request body for the API endpoint
class QuestionRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    return RedirectResponse("/static/index.html")


# Define the API endpoint
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    # Send a chat completion request with the question and stream the response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": request.question}],
        temperature=0,
        stream=True
    )

    async def generate():
        start_time = time.time()
        timeout = 60 * 5
        max_tokens = 2048
        total_tokens = 0

        for chunk in response:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                yield delta["content"]
                total_tokens += len(delta["content"].strip().split())

            if total_tokens >= max_tokens:
                break

            if "finish_reason" in delta and delta["finish_reason"] != "null":
                break

            current_time = time.time()
            if current_time - start_time > timeout:
                break

    return StreamingResponse(generate())


class FileRequest(BaseModel):
    file_name: str
    path: str
    content: str


@app.post("/write_file")
async def write_file(request: FileRequest):
    # 確保路徑以 "./static" 開頭
    if not request.path.startswith("./static"):
        raise HTTPException(status_code=400, detail="Invalid path. Must start with './static'.")

    # 檢查路徑是否存在，如果不存在則遞迴地建立目錄
    os.makedirs(request.path, exist_ok=True)

    print("request.path",request.path)
    print("request.file_name",request.file_name)
    # 寫入檔案內容
    with open(os.path.join(request.path, request.file_name), "w") as file:
        file.write(request.content)

    return {"status": "success", "message": f"File '{request.file_name}' saved at '{request.path}'"}


# Run the FastAPI app with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
