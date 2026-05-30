# syntax=docker/dockerfile:1.7

FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv

WORKDIR /build

RUN python -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src ./src
COPY tests ./tests
RUN pytest tests -q

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_HOST=0.0.0.0 \
    APP_PORT=8000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system taskpulse \
    && adduser --system --ingroup taskpulse taskpulse

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /build/src ./src

RUN cat > /app/src/health_server.py <<'PY'
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

from src.app import calculate_completion_rate, has_wip_limit_violation, task_status


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._send_json({"status": "ok", "service": "taskpulse-ci-demo"})
            return
        if self.path == "/metrics/demo":
            self._send_json(
                {
                    "completion_rate": calculate_completion_rate(3, 4),
                    "task_status": task_status(2, 4),
                    "wip_limit_violation": has_wip_limit_violation(4),
                }
            )
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        return

    def _send_json(self, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    HTTPServer((host, port), HealthHandler).serve_forever()
PY

USER taskpulse

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS "http://127.0.0.1:${APP_PORT}/health" || exit 1

CMD ["python", "-m", "src.health_server"]
