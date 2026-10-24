import "dotenv/config";

import { createServer } from "node:http";
import { timingSafeEqual } from "node:crypto";

import { auditSecurityEvent } from "../javascript_layer_4/audit_logger.js";

const PORT = Number(process.env.POLICY_PORT || 3001);
const INTERNAL_KEY = process.env.SENTINEL_INTERNAL_KEY;

function secureEquals(received, expected) {
    if (typeof received !== "string" || !expected) {
        return false;
    }

    const a = Buffer.from(received);
    const b = Buffer.from(expected);

    if (a.length !== b.length) {
        return false;
    }

    return timingSafeEqual(a, b);
}

function sendJson(response, status, data) {
    response.writeHead(status, {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
    });

    response.end(JSON.stringify(data));
}

async function readJson(request) {
    let body = "";

    for await (const chunk of request) {
        body += chunk;

        if (Buffer.byteLength(body, "utf8") > 16_384) {
            throw new Error("Request body too large");
        }
    }

    return JSON.parse(body);
}

function validateAssessment(data) {
    if (!data || typeof data !== "object") {
        return false;
    }

    if (!Number.isInteger(data.score) || data.score < 0 || data.score > 100) {
        return false;
    }

    if (!["low", "medium", "high"].includes(data.level)) {
        return false;
    }

    if (
        !Array.isArray(data.reasons) ||
        !data.reasons.every(
            (reason) => typeof reason === "string" && reason.length <= 300
        )
    ) {
        return false;
    }

    return true;
}

function evaluatePolicy(assessment) {
    if (assessment.score >= 70) {
        return {
            action: "review",
            message: "High risk: additional security review recommended.",
        };
    }

    if (assessment.score >= 30) {
        return {
            action: "monitor",
            message: "Medium risk: enhanced monitoring recommended.",
        };
    }

    return {
        action: "allow",
        message: "Low risk: no additional action recommended by this policy.",
    };
}

const server = createServer(async (request, response) => {
    if (request.method !== "POST" || request.url !== "/evaluate") {
        sendJson(response, 404, {
            error: "Route not found",
        });

        return;
    }

    if (!INTERNAL_KEY || INTERNAL_KEY.length < 32) {
        sendJson(response, 503, {
            error: "Internal service authentication is not configured",
        });

        return;
    }

    const receivedKey = request.headers["x-internal-key"];

    if (!secureEquals(receivedKey, INTERNAL_KEY)) {
        sendJson(response, 401, {
            error: "Unauthorized internal request",
        });

        return;
    }

    try {
        const assessment = await readJson(request);

        if (!validateAssessment(assessment)) {
            sendJson(response, 400, {
                error: "Invalid risk assessment",
            });

            return;
        }

        const policy = evaluatePolicy(assessment);

        const result = {
            score: assessment.score,
            level: assessment.level,
            reasons: assessment.reasons,
            action: policy.action,
            message: policy.message,
        };

        await auditSecurityEvent(result);

        sendJson(response, 200, result);
    } catch (error) {
        const message =
            error instanceof Error ? error.message : "Unknown error";

        const status = message === "Request body too large" ? 413 : 400;

        sendJson(response, status, {
            error:
                status === 413
                    ? "Request body too large"
                    : "Invalid request or processing failure",
        });
    }
});

server.listen(PORT, "127.0.0.1", () => {
    console.log(`Sentinel policy engine listening on 127.0.0.1:${PORT}`);
});