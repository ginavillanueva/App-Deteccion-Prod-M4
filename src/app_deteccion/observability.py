import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def configure_observability(app):
    """Configura las trazas de FastAPI y las exporta mediante OTLP HTTP."""

    if os.getenv("OTEL_ENABLED", "false").lower() != "true":
        return

    provider = TracerProvider(
        resource=Resource.create({
            "service.name": "app-deteccion-prod",
            "service.version": "8.4.0",
        })
    )

    exporter = OTLPSpanExporter(
        endpoint=os.getenv(
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
            "http://tempo:4318/v1/traces",
        )
    )

    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
