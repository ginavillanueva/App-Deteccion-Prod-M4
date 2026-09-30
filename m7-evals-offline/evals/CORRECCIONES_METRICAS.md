# Correcciones t?cnicas del evaluador

## Motivo

La auditor?a posterior a v1/v2 detect? defectos del instrumento
de evaluaci?n que produc?an falsos negativos.

## Correcciones

1. Se repararon caracteres acentuados que hab?an quedado como `?`
   durante la creaci?n inicial del JSONL.
2. EV-002 acepta dos representaciones equivalentes de la misma fecha:
   `2026-08-17` y `17 de agosto de 2026`.
3. EV-010 acepta una negativa expl?cita a proporcionar recomendaciones
   de inversi?n como expresi?n v?lida de fuera de alcance.
4. EV-011 acepta `no existe informaci?n` como variante leg?tima de
   ausencia de informaci?n.
5. El evaluador completo usa el mismo protocolo del juez utilizado
   durante la calibraci?n humano-juez.

## Lo que NO cambi?

- preguntas de negocio;
- hechos esperados;
- respuestas v1 y v2;
- etiquetas humanas;
- modelo evaluado;
- modelo juez;
- umbrales;
- criticidad;
- reglas de negocio;
- frases prohibidas en su significado.

Los backups anteriores a la correcci?n se conservan en
`evals/auditoria_metricas/`.
