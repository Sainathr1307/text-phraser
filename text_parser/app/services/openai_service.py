import json
import logging
from openai import AsyncOpenAI, OpenAIError

from app.core.config import settings
from app.schemas.parse import ParsedData

logger = logging.getLogger(__name__)

# ── OpenAI client (module-level singleton) ────────────────────────────────────
_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# ── Tool / function schema ─────────────────────────────────────────────────────
_EXTRACT_TOOL = {
    "type": "function",
    "function": {
        "name": "extract_structured_data",
        "description": (
            "Extract structured information from a freeform sentence. "
            "Return null for any field that is not mentioned."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": ["string", "null"],
                    "description": "The date mentioned (ISO-8601 if possible, otherwise natural language).",
                },
                "time": {
                    "type": ["string", "null"],
                    "description": "The time mentioned (24-hour HH:MM if possible, otherwise natural language).",
                },
                "location": {
                    "type": ["string", "null"],
                    "description": "The location or place mentioned.",
                },
                "task": {
                    "type": ["string", "null"],
                    "description": "The main action, task, or event described.",
                },
                "temperature": {
                    "type": ["string", "null"],
                    "description": "The temperature value with its unit (e.g. '72°F', '22°C').",
                },
            },
            "required": ["date", "time", "location", "task", "temperature"],
        },
    },
}

_SYSTEM_PROMPT = (
    "You are a precise information-extraction assistant. "
    "Given any sentence, extract the requested fields as accurately as possible. "
    "Do not invent information that is not present in the input."
)


# ── Public service function ────────────────────────────────────────────────────
async def parse_text(text: str) -> ParsedData:
    """
    Call the OpenAI API with function-calling to extract structured data
    from *text*. Returns a :class:`ParsedData` instance.
    """
    logger.info("Calling OpenAI model '%s' for text: %.80s…", settings.OPENAI_MODEL, text)

    try:
        response = await _client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            tools=[_EXTRACT_TOOL],
            tool_choice={"type": "function", "function": {"name": "extract_structured_data"}},
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        )
    except OpenAIError as exc:
        logger.exception("OpenAI API error")
        raise RuntimeError(f"OpenAI request failed: {exc}") from exc

    # ── Extract the tool-call arguments ───────────────────────────────────────
    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls:
        raise RuntimeError("OpenAI returned no tool calls – unexpected response format.")

    raw_args: str = tool_calls[0].function.arguments
    logger.debug("Raw tool arguments: %s", raw_args)

    try:
        args: dict = json.loads(raw_args)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to parse tool arguments as JSON: {exc}") from exc

    return ParsedData(**args)
