from dataclasses import dataclass

from app.python_layer_1.validation import SecurityEvent


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    level: str
    reasons: list[str]


def assess_risk(event: SecurityEvent) -> RiskAssessment:
    score = 0
    reasons = []

    # Muitas requisições podem indicar comportamento anormal.
    if event.requests_last_minute >= 100:
        score += 25
        reasons.append("High request volume")

    # Muitas tentativas de login malsucedidas podem indicar abuso.
    if event.failed_attempts >= 5:
        score += 25
        reasons.append("Multiple failed attempts")

    # Muitas contas diferentes podem indicar automação suspeita.
    if event.unique_accounts >= 10:
        score += 20
        reasons.append("Multiple accounts observed")

    # A exposição de dados sensíveis exige atenção imediata.
    if event.sensitive_data_exposed:
        score += 50
        reasons.append("Sensitive data exposure reported")

    # A pontuação nunca ultrapassa 100.
    score = min(score, 100)

    # Classifica o risco.
    if score >= 70:
        level = "high"
    elif score >= 30:
        level = "medium"
    else:
        level = "low"

    if not reasons:
        reasons.append("No configured risk indicators detected")

    return RiskAssessment(
        score=score,
        level=level,
        reasons=reasons,
    )