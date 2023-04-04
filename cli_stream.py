import argparse
import os

import openai

# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up argparse for CLI arguments
parser = argparse.ArgumentParser(description="Ask a question and get a response from OpenAI.")
parser.add_argument("question", help="The question you want to ask.")
args = parser.parse_args()

# Send a chat completion request with the question and stream the response
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": args.question}],
    temperature=0,
    stream=True
)

# Iterate over the response chunks and print the content
for chunk in response:
    delta = chunk["choices"][0]["delta"]

    if "content" in delta:
        print(delta["content"], end="")

    if "finish_reason" in delta and delta["finish_reason"] == "stop":
        break
