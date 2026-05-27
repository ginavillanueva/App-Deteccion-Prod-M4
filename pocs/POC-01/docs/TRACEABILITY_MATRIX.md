# Matriz de trazabilidad — POC-01

| Dolor / necesidad | Documento origen | Solución arquitectónica | Evidencia POC |
|---|---|---|---|
| Información dispersa en WhatsApp/Excel | BRD/MRD | Registro estructurado | `product_case` en SQLite |
| Falta de visibilidad gerencial | BRD/PRD/FSD | Dashboard inmediato | `dashboard_snapshot.json` |
| No se mide impacto financiero | BRD/PRD | Valor financiero en riesgo | `metrics.json` |
| Cambio de precio no trazable | PRD/FSD/ADR-0003 | Precio anterior/nuevo + evento | `PriceChanged.v1` |
| Riesgo de pérdida de eventos | ADR-0003 | Outbox transaccional | `outbox_event` |
| Evitar sobreingeniería | ADR-0001 | Monolito modular evolutivo | POC local sin microservicios |
| Proteger dominio | ADR-0002 | Caso de uso aislado | `poc01_benchmark.py` |
| IA no debe decidir precios | ADR-0004 | IA posterior/no fuente de verdad | Eventos consumibles, no mutación IA |
| Evolución AWS | ADR-0005 | RDS/EventBridge/SQS/CloudWatch | Mapeo en POC-01.md |
