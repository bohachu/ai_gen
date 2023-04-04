import os

import openai
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
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
        # Iterate over the response chunks and concatenate the content
        for chunk in response:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                yield delta["content"]
            if "finish_reason" in delta and delta["finish_reason"] == "stop":
                break

    return StreamingResponse(generate())


# Run the FastAPI app with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
