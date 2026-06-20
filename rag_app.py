import logging
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    sys.stderr.write(
        "Error: GEMINI_API_KEY is not set.\n"
        "Add GEMINI_API_KEY to your .env file or export it in your environment.\n"
    )
    sys.exit(1)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

genai_client = genai.Client(api_key=GEMINI_API_KEY)

GEMINI_MODEL = "gemini-2.5-flash"
OUTLINE_PROMPT = (
    "Create a short 3-point outline explaining what a large language model is."
)

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

def validate_user_input(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if len(text) < 5:
        raise HTTPException(status_code=400, detail="Question is too short")

    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Question is too long")

def validate_model_output(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=500, detail="AI returned an empty response")

    if len(text) < 10:
        raise HTTPException(status_code=500, detail="AI response is too short")

def review_model_output(original_answer: str) -> str:
    review_prompt = f"""
You are reviewing an AI-generated response.

Your job:
- If the response is unclear, incomplete, or poorly written, improve it.
- If the response is already good, return it unchanged.

AI response to review:
{original_answer}
"""

    review_response = genai_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=review_prompt,
    )

    return review_response.text

def test_gemini() -> str:
    try:
        outline_response = genai_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=OUTLINE_PROMPT,
        )
        outline = outline_response.text
        logger.info("Gemini first-step output captured successfully.")
        logger.debug("Gemini first-step intermediate output: %s", outline)

        full_response_prompt = (
            "Using this outline:\n\n"
            f"{outline}\n\n"
            "Write one paragraph explaining what a large language model is."
        )
        final_response = genai_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=full_response_prompt,
        )
        return final_response.text
    except Exception as exc:
        logger.error("Gemini API request failed: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="Failed to generate content from Gemini. Please try again later.",
        )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/test-gemini")
def test_gemini_endpoint() -> dict[str, str]:
    return {"response": test_gemini()}


@app.post("/query")
def query_ai(request: QueryRequest):
    validate_user_input(request.question)

    try:
        primary_response = genai_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=request.question,
        )
    except Exception as exc:
        logger.error("Gemini primary generation failed: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="Failed to generate a response from Gemini. Please try again later.",
        )

    raw_answer = primary_response.text
    validate_model_output(raw_answer)

    reviewed_answer = review_model_output(raw_answer)

    return {
        "question": request.question,
        "answer": reviewed_answer
    }
