# Text Parser API

A production-ready **FastAPI** service that converts freeform English text into
structured JSON using the **OpenAI function-calling** API.

---

## Project structure

```
text_parser/
├── main.py                      # App entry point
├── requirements.txt
├── .env.example
└── app/
    ├── api/
    │   └── routes.py            # POST /api/v1/parse  +  GET /api/v1/health
    ├── core/
    │   └── config.py            # Settings (reads .env)
    ├── schemas/
    │   └── parse.py             # Pydantic request / response models
    └── services/
        └── openai_service.py    # OpenAI function-calling logic
```

---

## Quick start

### 1 · Clone / download the project

```bash
cd text_parser
```

### 2 · Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3 · Install dependencies

```bash
pip install -r requirements.txt
```

### 4 · Configure environment variables

```bash
cp .env.example .env
# Open .env and set your OPENAI_API_KEY
```

### 5 · Run the server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API is now live at **http://localhost:8000**

---

## Endpoints

| Method | Path              | Description              |
|--------|-------------------|--------------------------|
| POST   | `/api/v1/parse`   | Parse text → structured JSON |
| GET    | `/api/v1/health`  | Health check             |
| GET    | `/docs`           | Swagger UI (auto-generated) |
| GET    | `/redoc`          | ReDoc UI (auto-generated)   |

---

## Example request

```bash
curl -X POST http://localhost:8000/api/v1/parse \
  -H "Content-Type: application/json" \
  -d '{"text": "Schedule a meeting at 3pm on Friday in New York. It will be 72°F outside."}'
```

### Response

```json
{
  "success": true,
  "input_text": "Schedule a meeting at 3pm on Friday in New York. It will be 72°F outside.",
  "parsed": {
    "date": "Friday",
    "time": "15:00",
    "location": "New York",
    "task": "Schedule a meeting",
    "temperature": "72°F"
  }
}
```

Missing fields are returned as `null`.

---

## Configuration reference

| Variable            | Default         | Description                     |
|---------------------|-----------------|---------------------------------|
| `OPENAI_API_KEY`    | *(required)*    | Your OpenAI secret key          |
| `OPENAI_MODEL`      | `gpt-4o-mini`   | Chat model to use               |
| `OPENAI_TEMPERATURE`| `0.0`           | Sampling temperature            |
| `OPENAI_MAX_TOKENS` | `512`           | Max tokens in the response      |
