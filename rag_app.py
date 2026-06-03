import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    sys.stderr.write(
        "Error: GEMINI_API_KEY is not set.\n"
        "Add GEMINI_API_KEY to your .env file or export it in your environment.\n"
    )
    sys.exit(1)

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
