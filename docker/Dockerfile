FROM python:3.12-slim AS builder

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mkdocs.yml .
COPY docs ./docs
RUN mkdocs build --strict

FROM nginx:1.27-alpine

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /workspace/site /usr/share/nginx/html

EXPOSE 8080

