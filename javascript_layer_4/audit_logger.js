import "dotenv/config";

import { mkdir, appendFile } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import path from "node:path";

const LOG_DIRECTORY = path.resolve("logs");

export async function auditSecurityEvent(event) {
    await mkdir(LOG_DIRECTORY, {
        recursive: true,
    });

    const record = {
        id: randomUUID(),
        timestamp: new Date().toISOString(),
        score: event.score,
        level: event.level,
        action: event.action,
        reasons: event.reasons,
    };

    const logPath = path.join(
        LOG_DIRECTORY,
        "security-events.jsonl"
    );

    await appendFile(
        logPath,
        JSON.stringify(record) + "\n",
        {
            encoding: "utf8",
            mode: 0o600,
        }
    );

    return record;
}