# Guía de defensa — POC-02

## Pitch breve

Esta POC valida que la IA de App Detección Prod puede priorizar productos próximos a vencer con criterios cuantificados y auditables, manteniendo decisiones comerciales bajo control humano.

## Qué significa BAJO/MEDIO/ALTO

- BAJO: score 0–29, seguimiento normal.
- MEDIO: score 30–59, revisión táctica en máximo 48 horas.
- ALTO: score >=60 o regla crítica, revisión hoy o máximo 24 horas.

## Preguntas probables

### ¿Por qué no automatizar descuentos?
Porque impactan margen y rentabilidad. La IA no debe tomar decisiones irreversibles.

### ¿Por qué usar scoring si se habla de IA?
Porque en fase temprana se valida el contrato de decisión, seguridad y explicabilidad. Luego puede conectarse un LLM real por adaptador.

### ¿Qué evidencia generó?
CSV de resultados, JSON de métricas, pruebas de prompt injection, auditoría IA y gráficos.
