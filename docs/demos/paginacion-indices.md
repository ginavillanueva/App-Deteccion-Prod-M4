# Paginacion e indices - Evidencia tecnica

Archivo: src/app_deteccion/infrastructure/sqlite_repository.py

Consulta SQL:

SELECT payload FROM cases
ORDER BY created_at DESC, id DESC
LIMIT ? OFFSET ?;

Indice SQL:

CREATE INDEX IF NOT EXISTS idx_cases_created_id
ON cases(created_at DESC, id DESC);

## Resultado de la prueba

Registros simulados: 100
Pagina 1: 10 registros
Pagina 2: 10 registros diferentes

EXPLAIN QUERY PLAN:

SCAN cases USING INDEX idx_cases_created_id

## Interpretacion

SQLite utiliza el indice para recorrer los registros ordenados.
OFFSET no garantiza costo constante en paginas profundas.
Prueba realizada con datos simulados, no con produccion.
