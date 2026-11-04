# Etapa 1: instalacion de dependencias
FROM python:3.11-slim AS builder

WORKDIR /build

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade setuptools==84.2.1 wheel==0.48.0 && pip install --no-cache-dir \
    "fastapi>=0.110,<1.0" \
    "uvicorn[standard]>=0.29,<1.0" \
    "pydantic>=2.0,<3.0"

# Etapa 2: imagen de ejecucion
FROM python:3.11-slim AS runtime

RUN python -m pip install --no-cache-dir --upgrade setuptools==84.2.1 wheel==0.48.0

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY src/ ./src/

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_DB_PATH=/app/data/app_deteccion_demo.db

RUN groupadd --system appgroup && \
    useradd --system --uid 999 --gid appgroup appuser && \
    mkdir -p /app/data && \
    chown -R 999:999 /app/data

USER 999:999

EXPOSE 8000

CMD ["uvicorn", "app_deteccion.main:app", "--host", "0.0.0.0", "--port", "8000"]



