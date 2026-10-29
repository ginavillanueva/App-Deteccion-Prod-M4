FROM python:3.11-slim

WORKDIR /app

RUN groupadd --system appgroup && useradd --system --gid appgroup appuser

COPY src/ ./src/

RUN pip install --no-cache-dir \
    "fastapi>=0.110,<1.0" \
    "uvicorn[standard]>=0.29,<1.0" \
    "pydantic>=2.0,<3.0"

ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app/data && chown -R 999:999 /app/data

ENV APP_DB_PATH=/app/data/app_deteccion_demo.db

USER 999:999

EXPOSE 8000

CMD ["uvicorn", "app_deteccion.main:app", "--host", "0.0.0.0", "--port", "8000"]

