
# POC-02.md – Visualización KPIs

## 0. Metadatos
| Campo | Valor |
|-------|-------|
| ID | POC-02 |
| Título | Validación visualización KPIs |
| Grupo | G07 |
| Responsable(s) | Gina Fabiana Villanueva Viscarra |
| Fecha inicio | 14/05/2026 |
| Fecha objetivo de cierre | 15/05/2026 |
| Estado | Propuesta / En ejecución / Completada |
| ADR relacionado | ADR-0001 |

## 1. Riesgo que mitiga
Verificar que KPIService despliega métricas en tiempo real con latencia aceptable para supervisores y gerentes.

## 2. Hipótesis
Creemos que KPIService mostrará KPIs estratégicos con latencia < 2 seg y consistencia de datos para usuarios concurrentes.

## 3. Criterio de éxito medible (SMART)
- Métrica principal: Latencia de actualización de dashboard
- Umbral éxito: < 2 seg
- Umbral fracaso: > 3 seg

## 4. Alcance reducido (time-boxed)
- Funcionalidades incluidas: simulación de KPIs, actualización de dashboard y logs
- Funcionalidades excluidas: integración con ERP y alertas de producción
- Duración máxima: 1 día

## 5. Diseño de la prueba
### 5.1 Stack usado
| Componente | Tecnología | Versión |
|------------|------------|---------|
| KPIService | Node.js | 18 |
| Dashboard | React | 18 |
| Base de prueba | PostgreSQL | 15 |

### 5.2 Arquitectura de la POC

flowchart LR
  DB[Base de datos] --> KPI[KPIService]
  KPI --> Dashboard[Visualización en tiempo real]
  KPI --> Logs[Telemetría]

### 5.3 Datos de prueba
Origen: 500 métricas simuladas de productos críticos
Volumen: 500 métricas concurrentes
Sesgos conocidos: solo métricas válidas simuladas

### 5.4 Procedimiento experimental
Cargar métricas simuladas en DB
Ejecutar KPIService y actualizar dashboard
Medir latencia y consistencia de datos
Registrar resultados en logs

## 6. Entorno
Contenedores locales Node.js y PostgreSQL
CPU: 4 cores, RAM: 8GB
Costo estimado: nulo

### 7. Herramientas de medición
Scripts de latencia y carga
Logs de dashboard
Capturas de pantalla
### 8. Plan de ejecución
| Día | Actividad           | Responsable     |
| --- | ------------------- | --------------- |
| 1   | Setup entorno       | Responsable POC |
| 2   | Ejecución y captura | Responsable POC |
| 3   | Análisis y reporte  | Responsable POC |

## 9. Resultados
Completar al finalizar la POC.
### 9.1 Tabla de métricas
Métrica	Valor obtenido	Umbral éxito	Veredicto
Latencia dashboard		< 2 seg	✅/❌
Consistencia datos		100 %	✅/❌
## 9.2 Gráficos / capturas
Guardar en pocs/POC-02/evidencia/
## 10. Conclusiones y veredicto
Veredicto: ✅ / ⚠️ / ❌
Justificación basada en latencia y consistencia
Próximos pasos según resultado
## 11. Aprendizajes
Técnico: optimizar queries para dashboard
De equipo: coordinación front-end/back-end
De herramientas: carga concurrente simulada
## 12. Riesgos remanentes
Datos reales podrían variar
Integración con alertas en producción no probada
## 13. Referencias
Documentación interna KPIService
POC de dashboards internos
## 14. Historial
| Versión | Fecha      | Autor        | Cambio               |
| ------- | ---------- | ------------ | -------------------- |
| 1       | 14/05/2026 | Gina Fabiana | Creación             |
| 2       | 14/05/2026 | Gina Fabiana | Resultados agregados |
