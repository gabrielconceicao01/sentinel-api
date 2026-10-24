import hmac
import os
from contextlib import asynccontextmanager

import httpx
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

from app.python_layer_1.validation import SecurityEvent
from app.python_layer_2.risk_engine import assess_risk


load_dotenv()

API_KEY = os.getenv("SENTINEL_API_KEY", "")
INTERNAL_KEY = os.getenv("SENTINEL_INTERNAL_KEY", "")

POLICY_URL = os.getenv(
    "POLICY_URL",
    "http://127.0.0.1:3001/evaluate",
)

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if len(API_KEY) < 32:
        raise RuntimeError(
            "Configure SENTINEL_API_KEY com pelo menos 32 caracteres."
        )

    if len(INTERNAL_KEY) < 32:
        raise RuntimeError(
            "Configure SENTINEL_INTERNAL_KEY com pelo menos 32 caracteres."
        )

    async with httpx.AsyncClient(timeout=5.0) as client:
        app.state.policy_client = client
        yield


app = FastAPI(
    title="Sentinel Security API",
    description="API demonstrativa de validação e análise de risco.",
    version="1.0.0",
    lifespan=lifespan,
)


async def verify_api_key(
    received_key: str | None = Depends(api_key_header),
):
    if not received_key or not hmac.compare_digest(
        received_key,
        API_KEY,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
        )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "sentinel-api",
    }


@app.post(
    "/v1/analyze",
    dependencies=[Depends(verify_api_key)],
)
async def analyze_event(event: SecurityEvent):
    assessment = assess_risk(event)

    payload = {
        "score": assessment.score,
        "level": assessment.level,
        "reasons": assessment.reasons,
    }

    try:
        response = await app.state.policy_client.post(
            POLICY_URL,
            json=payload,
            headers={
                "X-Internal-Key": INTERNAL_KEY,
            },
        )

        response.raise_for_status()

        return response.json()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Policy engine timed out",
        ) from None

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="Policy engine returned an error",
        ) from None

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Policy engine is unavailable",
        ) from None