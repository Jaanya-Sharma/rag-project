import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    sys.stderr.write(
        "Error: GEMINI_API_KEY is not set.\n"
        "Add GEMINI_API_KEY to your .env file or export it in your environment.\n"
    )
    sys.exit(1)

genai_client = genai.Client(api_key=GEMINI_API_KEY)

GEMINI_TEST_PROMPT = "Explain what a large language model is in one paragraph."

app = FastAPI()


def test_gemini() -> str:
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=GEMINI_TEST_PROMPT,
    )
    return response.text


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/test-gemini")
def test_gemini_endpoint():
    return {"response": test_gemini()}
