import logging
from fastapi import APIRouter, HTTPException, status

from app.schemas.parse import ParseRequest, ParseResponse
from app.services.openai_service import parse_text

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Parser"])


@router.post(
    "/parse",
    response_model=ParseResponse,
    status_code=status.HTTP_200_OK,
    summary="Parse freeform text into structured JSON",
    response_description="Structured extraction result",
)
async def parse_endpoint(body: ParseRequest) -> ParseResponse:
    """
    **POST /api/v1/parse**

    Accepts a freeform English sentence and returns a structured JSON object
    containing any detected *date*, *time*, *location*, *task*, and
    *temperature* values.

    Fields absent from the input text are returned as **null**.
    """
    logger.info("Received parse request | text_length=%d", len(body.text))

    try:
        parsed = await parse_text(body.text)
    except RuntimeError as exc:
        logger.error("Parsing failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )

    logger.info("Parse successful")
    return ParseResponse(success=True, input_text=body.text, parsed=parsed)


# ── Health check ───────────────────────────────────────────────────────────────
@router.get("/health", tags=["Health"], summary="Health check")
async def health_check():
    return {"status": "ok"}
