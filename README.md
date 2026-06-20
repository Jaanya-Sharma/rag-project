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

`GET /test-gemini` now uses a two-step Gemini flow to generate a final answer from an intermediate output.

1. The route calls `test_gemini()`, which uses the shared `genai_client`.
2. The first Gemini call sends a fixed prompt:

   > Create a short 3-point outline explaining what a large language model is.

3. The first call captures the response as an intermediate value, logs that intermediate output safely, and does not expose it to the client.
4. The second Gemini call uses the captured outline as input and asks the model to generate a refined paragraph based on that outline.
5. The endpoint returns JSON with only the final model text:

   ```json
   {"response": "...refined Gemini output..."}
   ```

Why the steps are separated

- Separating the workflow into two steps makes it easier to inspect and validate the intermediate reasoning or structure before producing the final answer. For example, if the final paragraph is wrong, the developer can first verify whether the outline itself was incorrect, which narrows debugging to a specific stage.
- It supports a stronger multi-step generation pattern, where the first step produces a scaffold and the second step refines it. This makes the architecture more modular and easier to extend with retrieval or fact-checking later.
- It also creates a clearer place to add logging, validation, or retrieval logic in the future without immediately exposing intermediate content to the client. For instance, an intermediate outline could be used to select relevant documents or apply prompt correction before the second call.

Why input validation exists

- Input validation ensures the API receives a real question rather than empty, missing, or trivially short text.
- This avoids wasted Gemini requests and gives the client fast, consistent feedback when the request is invalid.

Why output validation exists

- Output validation checks that the AI returned a usable response and helps catch empty, incomplete, or malformed results before they are sent back to the caller.
- It prevents the endpoint from returning low-quality or meaningless answers as if they were valid.

Why a second AI model is used to review responses

- The review step lets the app improve or clean up the primary model output without exposing the raw intermediate answer directly.
- It helps catch issues such as unclear phrasing, omission, or poor structure and produces a more polished final result.

Challenges and open questions

- The current implementation is still synchronous and blocking; an async client, background thread, or FastAPI dependency that runs I/O off the main thread may be needed for production performance.
- There is no retrieval step yet, so the flow is still only model-to-model generation rather than true RAG. A next step would be to add document embedding, vector search, and prompt augmentation with retrieved context before the first or second Gemini call.
- Sensitive or secret data should never be logged; the current logs only record that an intermediate result was captured, not the API key or request metadata. A safer approach is structured logging with redaction and environment-based log levels.
- If Gemini fails, the endpoint returns a clean 502 response instead of exposing raw exceptions or secret details. Future work could include retry logic, more specific error mapping, and graceful fallback messaging for transient API issues.

Example: open `http://127.0.0.1:8000/test-gemini` in a browser while the server is running.

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
