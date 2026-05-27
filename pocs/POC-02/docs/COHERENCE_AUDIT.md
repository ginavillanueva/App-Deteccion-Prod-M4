# Auditoría de coherencia — POC-02

## Validación transversal

- No contradice ADR-0001: se mantiene dentro del monolito modular evolutivo.
- No contradice ADR-0002: la IA entra por puerto/adaptador.
- No contradice ADR-0003: la IA no reemplaza el dashboard transaccional inmediato.
- Valida ADR-0004: guardrails y human-in-the-loop.
- Complementa ADR-0005: deja métricas y logs observables.
- Complementa POC-01: POC-01 valida registro; POC-02 valida priorización segura.

## Control de precio

El cambio de precio es tratado como variable crítica de riesgo. La IA puede detectar que un cambio no aprobado aumenta riesgo, pero no puede aprobar ni aplicar el cambio.
