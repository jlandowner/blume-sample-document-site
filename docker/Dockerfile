FROM python:3.12-slim AS builder

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mkdocs.yml .
COPY docs ./docs
COPY tools ./tools
RUN python tools/document-validator/validate_docs.py
RUN python tools/ai-artifacts/generate_ai_artifacts.py
RUN mkdocs build --strict

FROM python:3.12-slim AS mcp

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /workspace/ai /app/ai
COPY tools/docs-mcp/server.py /app/server.py

ENV AI_DIR=/app/ai
ENTRYPOINT ["python", "/app/server.py"]

FROM nginx:1.27-alpine

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /workspace/site /usr/share/nginx/html
COPY --from=builder /workspace/ai /usr/share/nginx/html/ai

EXPOSE 8080
