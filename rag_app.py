import logging
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai

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
