from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SecurityEvent(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    event_type: Literal[
        "login",
        "checkout",
        "data_access",
        "api_request",
    ]

    requests_last_minute: int = Field(
        ge=0,
        le=1_000_000,
    )

    failed_attempts: int = Field(
        ge=0,
        le=1_000_000,
    )

    unique_accounts: int = Field(
        ge=0,
        le=1_000_000,
    )

    sensitive_data_exposed: bool