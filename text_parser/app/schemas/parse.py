from pydantic import BaseModel, Field
from typing import Optional


# ── Request ────────────────────────────────────────────────────────────────────
class ParseRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        examples=["Schedule a meeting at 3pm on Friday in New York. It will be 72°F outside."],
    )


# ── Response ───────────────────────────────────────────────────────────────────
class ParsedData(BaseModel):
    date: Optional[str] = Field(None, description="Extracted date (e.g. '2024-12-20' or 'Friday')")
    time: Optional[str] = Field(None, description="Extracted time (e.g. '15:00' or '3pm')")
    location: Optional[str] = Field(None, description="Extracted location")
    task: Optional[str] = Field(None, description="Extracted action or task")
    temperature: Optional[str] = Field(None, description="Extracted temperature value with unit")


class ParseResponse(BaseModel):
    success: bool
    input_text: str
    parsed: ParsedData
