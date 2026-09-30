# Correcci?n v3

## Variable modificada

?nicamente `SYSTEM_PROMPT`.

## Variables que permanecen constantes

- Modelo evaluado: `llama3.2:3b-instruct-q4_K_M`
- Dataset dorado
- Temperatura
- MAX_PASOS
- Servidor MCP
- Herramientas
- Base de negocio
- Guardrails
- Umbrales de la compuerta

## Motivo de la correcci?n

La evaluaci?n de v1 y v2 revel? fallos reproducibles de completitud y precisi?n sem?ntica.

La v3 refuerza:

1. reporte expl?cito de estados;
2. prohibici?n de inferir datos ausentes;
3. separaci?n entre vencimiento y reposici?n;
4. pol?tica de cambio de precio como consulta informativa sin aprobaci?n;
5. imposibilidad de modificar estados comerciales;
6. manejo expl?cito de consultas fuera de alcance;
7. resistencia a instrucciones que pidan omitir herramientas;
8. negativas informativas en lugar de rechazos gen?ricos.

## Regla de negocio cr?tica

`CAMBIO_PRECIO = CONSULTA_INFORMATIVA_SIN_APROBACION`

El agente puede informar el estado almacenado de un registro, incluso si dicho campo contiene `APROBADO`, pero el agente nunca aprueba, autoriza ni aplica cambios.
