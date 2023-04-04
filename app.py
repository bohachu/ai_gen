import os

import openai
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

load_dotenv()  # 讀取.env文件
api_key = os.getenv("OPENAI_API_KEY")  # 獲取API密鑰

app = FastAPI()


# OpenAI GPT-4 模型
class GeneralModel:
    def __init__(self):
        print("Model Initialization--->")

    def query(self, prompt, myKwargs={}):
        kwargs = {
            "temperature": 0.9,
            "max_tokens": 600,
        }
        for kwarg in myKwargs:
            kwargs[kwarg] = myKwargs[kwarg]

        r = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt}], **kwargs
        )
        return r["choices"][0]["message"]["content"].strip()

    def model_prediction(self, inp):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        output = self.query(inp)
        return output


model = GeneralModel()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI GPT Code Generator</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1 class="mt-5">FastAPI GPT-4 Code Generator</h1>
            <form id="input-form">
                <div class="form-group">
                    <label for="input-text">Enter your natural language:</label>
                    <textarea class="form-control" id="input-text" rows="5"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Generate Code</button>
            </form>
            <div class="mt-3">
                <h3>Generated Code:</h3>
                <pre id="output-code"></pre>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        <script>
            const form = document.getElementById("input-form");
            const inputText = document.getElementById("input-text");
            const outputCode = document.getElementById("output-code");
            form.addEventListener("submit", async (event) => {
                event.preventDefault();
                const response = await fetch("/generate-code", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ text: inputText.value }),
                });
                const generatedCode = await response.text();
                outputCode.textContent = generatedCode;
            });
        </script>
    </body>
    </html>
    """
    return html_content


@app.post("/generate-code")
async def generate_code(request: Request):
    data = await request.json()
    input_text = data["text"]
    generated_code = model.model_prediction(input_text)
    return generated_code
