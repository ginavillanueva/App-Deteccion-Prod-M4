# POC-01.md – Alertas predictivas

## 0. Metadatos
| Campo | Valor |
|-------|-------|
| ID | POC-01 |
| Título | Validación de alertas predictivas |
| Grupo | G07 |
| Responsable(s) | Gina Fabiana Villanueva Viscarra |
| Fecha inicio | 14/05/2026 |
| Fecha objetivo de cierre | 15/05/2026 |
| Estado | Propuesta / En ejecución / Completada |
| ADR relacionado | ADR-0003 |

## 1. Riesgo que mitiga
Validar que el agent-orchestrator detecte productos críticos con precisión suficiente para alertar oportunamente a supervisores y gerentes.

## 2. Hipótesis
Creemos que agent-orchestrator permitirá identificar ≥ 80 % de productos críticos con alerta en menos de 500 ms bajo condiciones de prueba simuladas.

## 3. Criterio de éxito medible (SMART)
- Métrica principal: precisión de alertas y latencia p95 < 500 ms
- Umbral éxito: ≥ 80 % de detección correcta
- Umbral fracaso: < 70 % de detección

## 4. Alcance reducido (time-boxed)
- Funcionalidades incluidas: simulación de productos críticos, generación de alertas, registro de eventos.
- Funcionalidades excluidas: integración con ERP y dashboards en producción.
- Duración máxima: 1 día.

## 5. Diseño de la prueba
### 5.1 Stack usado
| Componente | Tecnología | Versión |
|------------|------------|---------|
| agent-orchestrator | Python | 3.10 |
| RAG-service | Python | 3.10 |
| Base de prueba | PostgreSQL | 15 |

### 5.2 Arquitectura de la POC
flowchart LR
  Prod[Producto crítico] --> AO[agent-orchestrator]
  AO --> Alerts[Alertas generadas]
  AO --> Logs[Telemetría]

### 5.3 Datos de prueba
Origen: 1000 registros sintéticos de productos críticos.
Volumen: 1000 productos
Sesgos conocidos: no incluye productos no críticos
### 5.4 Procedimiento experimental
Cargar productos críticos en DB de prueba.
Ejecutar agent-orchestrator para generar alertas.
Medir latencia y precisión.
Registrar resultados en logs.
## 6. Entorno
Contenedores locales con Python y PostgreSQL
CPU: 4 cores, RAM: 8GB
Costo estimado: nulo (entorno local)
## 7. Herramientas de medición
Logs de telemetría
Scripts de validación de alertas
Dashboards temporales de control
## 8. Plan de ejecución
| Día | Actividad                       | Responsable     |
| --- | ------------------------------- | --------------- |
| 1   | Setup entorno                   | Responsable POC |
| 2   | Ejecución y captura de métricas | Responsable POC |
| 3   | Análisis y reporte              | Responsable POC |


## 9. Resultados

Completar al finalizar la POC.

### 9.1 Tabla de métricas
| Métrica           | Valor obtenido | Umbral éxito | Veredicto |
| ----------------- | -------------- | ------------ | --------- |
| Precisión alertas |                | 80 %         | ✅/❌       |
| Latencia p95      |                | 500 ms       | ✅/❌       |

### 9.2 Gráficos / capturas
Guardar en pocs/POC-01/evidencia/
## 10. Conclusiones y veredicto
Veredicto: ✅ / ⚠️ / ❌
Justificación basada en métricas
Próximos pasos según resultado
## 11. Aprendizajes
Técnico: ajustar guardrails para casos extremos
De equipo: coordinación entre generación de alertas y logs
De herramientas: optimizar latencia del agent-orchestrator
## 12. Riesgos remanentes
Productos no incluidos en test sintético
Integración real con dashboards no probada
## 13. Referencias
Documentación interna de agent-orchestrator
POC previas de RAG-service
## 14. Historial
| Versión | Fecha      | Autor        | Cambio               |
| ------- | ---------- | ------------ | -------------------- |
| 1       | 14/05/2026 | Gina Fabiana | Creación             |
| 2       | 14/05/2026 | Gina Fabiana | Resultados agregados |
