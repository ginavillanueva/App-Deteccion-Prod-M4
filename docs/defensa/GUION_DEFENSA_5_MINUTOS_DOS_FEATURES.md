# Guion de defensa — máximo 5 minutos

Buenos días. En esta entrega presento dos features aplicadas de App Detección Prod.

Primero, el problema: actualmente los productos próximos a vencer se reportan con WhatsApp, fotos y Excel. Esto genera información dispersa, falta de trazabilidad, control débil de precios y poca visibilidad para supervisión y gerencia.

La primera feature es el **registro visual de producto crítico**. El mercaderista registra tienda, producto, lote, vencimiento, cantidad, precio actual, nuevo precio, acción comercial y evidencia. Al guardar, el sistema calcula riesgo, score, SLA, valor financiero en riesgo, valor intervenido, diferencia de precio y descuento promedio.

La segunda feature es la **bandeja de supervisión y dashboard gerencial**. El supervisor selecciona el caso, lo valida con una decisión y comentario, y luego el dashboard gerencial se actualiza con total de casos, casos validados, riesgo, valor financiero, cantidad intervenida, cambios de precio y acciones comerciales.

La implementación mantiene trazabilidad completa: FSD, Design Doc, ADR, prompt implementation, código, tests y DTP. También conserva la regla de AGENTS.md: cobertura mínima de 90%. En esta fase se alcanzan 50 tests pasados y 100% de cobertura.

El valor de la demo es que transforma un reporte informal en un dato estructurado, auditable y útil para tomar decisiones operativas, tácticas y gerenciales.
