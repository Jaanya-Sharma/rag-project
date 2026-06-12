# RAG Project

This repository contains my Retrieval-Augmented Generation (RAG) project for the GenAI Secure Coding course.

The project is built incrementally each week. The current milestone covers environment setup, API key validation, a minimal FastAPI server, and a basic Gemini connectivity test.

## Application (`rag_app.py`)

### Environment variables

On import, `load_dotenv()` (from `python-dotenv`) reads a `.env` file in the project directory and loads values into `os.environ`. Shell environment variables are not overwritten unless configured otherwise.

Create a local `.env` file (gitignored) with:

```
GEMINI_API_KEY=your_key_here
```

### Gemini API key

`GEMINI_API_KEY` is read with `os.getenv("GEMINI_API_KEY")` after dotenv runs. If the key is missing or empty, the process prints a clear error to stderr and exits with code `1`. Uvicorn will not start without a valid key.

### Gemini configuration

The app uses the [`google-genai`](https://github.com/googleapis/python-genai) SDK. At startup, a client is created with the API key:

```python
genai_client = genai.Client(api_key=GEMINI_API_KEY)
```

Generation calls go through `genai_client.models.generate_content()`. There is no user input, document loading, chunking, embeddings, or retrieval yet.

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

| Endpoint       | Method | Description |
| -------------- | ------ | ----------- |
| `/health`      | GET    | Returns `{"status": "ok"}`. Liveness check only. |
| `/test-gemini` | GET    | Sends a hardcoded prompt to Gemini and returns the model response. See below. |

Other paths (for example `/`) return `404 Not Found`.

### What `/test-gemini` does

`GET /test-gemini` is a simple end-to-end test that confirms the Gemini API key and client work.

1. The route calls `test_gemini()`, which uses the shared `genai_client`.
2. It sends a **fixed prompt** (no user input):

   > Explain what a large language model is in one paragraph.

3. The request goes to the **`gemini-2.5-flash`** model via `generate_content()`.
4. The endpoint returns JSON with the model’s text:

   ```json
   {"response": "...Gemini output..."}
   ```

Example: open `http://127.0.0.1:8000/test-gemini` in a browser while the server is running.

If the Gemini API rejects the request (for example quota exceeded or an invalid key), the error is not handled in the route and the browser may show **500 Internal Server Error**. Check the Uvicorn terminal output for the underlying `google.genai.errors.ClientError`.

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
