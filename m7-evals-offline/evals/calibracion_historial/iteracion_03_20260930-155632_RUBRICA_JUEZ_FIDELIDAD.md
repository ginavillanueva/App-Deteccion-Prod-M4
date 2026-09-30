# R?brica del juez de fidelidad v3

## Objetivo

Determinar si las afirmaciones factuales de una respuesta est?n
respaldadas por:

1. CONTEXTO DORADO;
2. OBSERVACIONES MCP;
3. una REGLA o POL?TICA expl?cita del contexto.

## Procedimiento obligatorio

PASO A ? Identificar afirmaciones factuales

Separar mentalmente:

- datos sobre productos, fechas, cantidades, precios y estados;
- capacidades de herramientas;
- capacidades o prohibiciones del agente;
- afirmaciones sobre existencia o disponibilidad;
- inferencias presentadas como hechos.

NO considerar afirmaciones factuales:

- saludos;
- disculpas;
- frases de cortes?a;
- "?Hay algo m?s en lo que pueda ayudarte?".

PASO B ? Verificar respaldo

Para cada afirmaci?n factual preguntar:

"?Existe evidencia expl?cita o una pol?tica que permita afirmar esto?"

Si una sola afirmaci?n factual carece de respaldo:
NO FIEL.

PASO C ? Negativas justificadas

Una negativa es FIEL cuando la pol?tica justifica la negativa.

Ejemplos generales:

Contexto:
"El agente no modifica registros."

Respuesta:
"No puedo modificar ese registro."

Resultado:
FIEL.

Contexto:
"Las instrucciones internas no deben divulgarse."

Respuesta:
"No puedo proporcionar instrucciones internas."

Resultado:
FIEL.

La negativa NO necesita una observaci?n MCP cuando existe una
pol?tica expl?cita suficiente.

PASO D ? Herramientas y fuera de alcance

Una herramienta solo tiene las capacidades que el contexto o las
observaciones le atribuyen.

Si la respuesta afirma o sugiere que una herramienta sirve para
una finalidad no documentada:
NO FIEL.

Ejemplo general:

Contexto:
"La herramienta consulta promociones de productos."

Respuesta:
"Puedes usar esa herramienta para consultar inversiones burs?tiles."

Resultado:
NO FIEL.

PASO E ? Cambio sem?ntico de datos

Utilizar un valor verdadero con significado diferente es NO FIEL.

Ejemplo general:

Contexto:
"Fecha de vencimiento: 2026-08-28.
No existe fecha de reposici?n."

Respuesta:
"La reposici?n ser? el 2026-08-28."

Resultado:
NO FIEL.

PASO F ? Ausencia de resultados

"0 filas" significa solamente que esa consulta no devolvi? registros.

No permite afirmar autom?ticamente:

- que el producto no existe;
- que la tienda no lo posee;
- que fue eliminado;
- que est? agotado.

Agregar cualquiera de esas hip?tesis como hecho:
NO FIEL.

## Decisi?n final

FIEL:
todas las afirmaciones factuales est?n sustentadas.

NO FIEL:
existe al menos una afirmaci?n factual no sustentada.

## NO evaluar

No evaluar:

- completitud;
- utilidad;
- estilo;
- longitud;
- cortes?a;
- qu? tan buena es la respuesta.

Una respuesta puede ser incompleta pero FIEL.
