FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG GID=1042
ARG UID=1042

WORKDIR /app

COPY . .
RUN pip install --upgrade pip \
 && pip install uv \
 && pip install .

RUN addgroup --gid ${GID} deploy \
 && useradd --gid ${GID} --uid ${UID} --home-dir /home/deploy --create-home --shell /bin/bash deploy

RUN chown -R deploy:deploy /app

USER deploy

EXPOSE 8000

CMD ["python", "-m", "mcp_retsinformation"]
