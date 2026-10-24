import pytest
from pydantic import ValidationError

from app.python_layer_1.validation import SecurityEvent


def test_valid_security_event():
    event = SecurityEvent(
        event_type="login",
        requests_last_minute=10,
        failed_attempts=0,
        unique_accounts=1,
        sensitive_data_exposed=False,
    )

    assert event.event_type == "login"
    assert event.requests_last_minute == 10


def test_rejects_negative_request_count():
    with pytest.raises(ValidationError):
        SecurityEvent(
            event_type="login",
            requests_last_minute=-1,
            failed_attempts=0,
            unique_accounts=1,
            sensitive_data_exposed=False,
        )


def test_rejects_unknown_event_type():
    with pytest.raises(ValidationError):
        SecurityEvent(
            event_type="unknown",
            requests_last_minute=10,
            failed_attempts=0,
            unique_accounts=1,
            sensitive_data_exposed=False,
        )


def test_rejects_unexpected_fields():
    with pytest.raises(ValidationError):
        SecurityEvent(
            event_type="login",
            requests_last_minute=10,
            failed_attempts=0,
            unique_accounts=1,
            sensitive_data_exposed=False,
            password="secret",
        )