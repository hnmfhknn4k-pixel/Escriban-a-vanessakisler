FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    ESCRIBANIA_DATA=/app/runtime

WORKDIR /app
COPY escribania/requirements.lock ./requirements.lock
RUN python -m pip install -r requirements.lock \
    && useradd --create-home --uid 10001 escribania
COPY --chown=escribania:escribania escribania/ ./
RUN mkdir -p /app/runtime && chown escribania:escribania /app/runtime \
    && chmod 700 /app/runtime
USER escribania
EXPOSE 8001
CMD ["sh", "scripts/start-render.sh"]
