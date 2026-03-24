FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

ARG GID=1042
ARG UID=1042

RUN pip install --upgrade pip && pip install uv

WORKDIR /app

COPY . .
RUN uv sync --frozen --no-dev

RUN addgroup --gid ${GID} deploy \
 && useradd --gid ${GID} --uid ${UID} --home-dir /home/deploy --create-home --shell /bin/bash deploy

RUN chown -R deploy:deploy /app

USER deploy

EXPOSE 8000

CMD ["python", "-m", "mcp_retsinformation"]
