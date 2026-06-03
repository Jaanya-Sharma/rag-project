# RAG Project

This repository contains my Retrieval-Augmented Generation (RAG) project for the GenAI Secure Coding course.

The project is built incrementally each week. The current milestone covers environment setup, API key validation, and a minimal FastAPI server.

## Application (`rag_app.py`)

### Environment variables

On import, `load_dotenv()` (from `python-dotenv`) reads a `.env` file in the project directory and loads values into `os.environ`. Shell environment variables are not overwritten unless configured otherwise.

Create a local `.env` file (gitignored) with:

```
GEMINI_API_KEY=your_key_here
```

### Gemini API key

`GEMINI_API_KEY` is read with `os.getenv("GEMINI_API_KEY")` after dotenv runs. If the key is missing or empty, the process prints a clear error to stderr and exits with code `1`. Uvicorn will not start without a valid key.

The key is stored in the module variable `GEMINI_API_KEY` for use in later steps.

### Gemini configuration

Gemini is **not** configured in code yet. `google-generativeai` is listed in `requirements.txt` but is not imported or called. There is no `genai.configure()`, model selection, or generation logic yet—only startup validation of the API key.

### FastAPI app

The ASGI application is a single instance:

```python
app = FastAPI()
```

Run the server from the project root:

```bash
uvicorn rag_app:app --reload
```

### Endpoints

| Endpoint   | Method | Description                                      |
| ---------- | ------ | ------------------------------------------------ |
| `/health`  | GET    | Returns `{"status": "ok"}`. Liveness check only. |

Other paths (for example `/`) return `404 Not Found`.

### Why Gemini calls are not implemented yet

This week’s scope is infrastructure: load secrets safely, fail fast on misconfiguration, and expose a health endpoint. Retrieval, prompting, and Gemini API calls will be added in later milestones as the RAG pipeline is built out.

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## Git Commands Used So Far

- git clone
- git status
- git add
- git commit
- git push
