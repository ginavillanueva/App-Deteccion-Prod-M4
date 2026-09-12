# Plan 01 Navegacion y sesion

## Application Overview

Plan exclusivo para los flujos NAV-01 y THR-01 de App Deteccion Prod. La exploracion real se realizo en http://127.0.0.1:8501/ con estado inicial limpio por caso. La interfaz expone localizadores humanos adecuados: getByRole('heading', {name: /App Deteccion Prod/i}), getByRole('heading', {name: 'Salud del sistema'}), getByRole('button', {name: /Nuevo thread/i}) y el Thread ID visible como elemento code cercano al texto 'Thread ID'. No se verificara redaccion de LLM ni se analizaran otros flujos. tokens no expuestos por la interfaz.

## Test Scenarios

### 1. Navegacion y sesion

**Seed:** `seed.spec.ts`

#### 1.1. NAV-01 - La apertura muestra el encabezado y la salud del sistema

**File:** `NO_GENERAR_TEST_NAV-01.spec.ts`

**Steps:**
  1. Precondicion: iniciar el caso en estado fresco y navegar a page.goto('/').
    - expect: La pagina queda en http://127.0.0.1:8501/.
    - expect: El caso es independiente y no depende de otro caso.
  2. La persona abre App Deteccion Prod navegando a la ruta raiz.
    - expect: Es visible un encabezado de nivel 1 cuyo nombre contiene 'App Deteccion Prod'.
    - expect: Es visible el bloque con el encabezado 'Salud del sistema'.
    - expect: El resultado observable cubre NAV-01: titulo de la aplicacion y salud del sistema visibles.
  3. Localizadores recomendados: getByRole('heading', {name: /App Deteccion Prod/i, level: 1}) y getByRole('heading', {name: 'Salud del sistema', level: 3}). No hace falta localizar por emoji, clase CSS o snapshot ref.
    - expect: Los localizadores humanos encuentran un unico encabezado de aplicacion y un unico encabezado de salud del sistema.
  4. Datos propios necesarios: ninguno.
    - expect: No se requiere dato de entrada ni estado persistido previo.
  5. Riesgos o fragilidad: el encabezado visible incluye un icono/emoji y la aplicacion puede tardar en renderizar; usar coincidencia parcial/case-insensitive y esperar la visibilidad de ambos encabezados. El texto observado no lleva tilde en 'Deteccion'.
    - expect: El caso falla si cualquiera de los dos encabezados no aparece visible tras la carga.

#### 1.2. THR-01 - Nuevo thread cambia el Thread ID activo

**File:** `NO_GENERAR_TEST_THR-01.spec.ts`

**Steps:**
  1. Precondicion: iniciar el caso en estado fresco y navegar a page.goto('/').
    - expect: La pagina queda en http://127.0.0.1:8501/.
    - expect: El caso es independiente y no depende de NAV-01 ni de otro caso.
  2. Antes de pulsar nada, localizar el valor visible asociado a 'Thread ID' y guardar su texto como threadIdAnterior. En la exploracion fue un elemento code cercano al parrafo 'Thread ID'.
    - expect: Existe un Thread ID anterior no vacio y se conserva su valor para la comparacion.
  3. La persona pulsa el boton Nuevo thread usando getByRole('button', {name: /Nuevo thread/i}).
    - expect: La aplicacion actualiza el estado visible del thread sin navegar fuera de la ruta raiz.
  4. Esperar a que termine la actualizacion y volver a leer el valor visible asociado a 'Thread ID' como threadIdNuevo.
    - expect: Existe un Thread ID nuevo no vacio.
  5. Comparar realmente threadIdNuevo con threadIdAnterior mediante una asercion de desigualdad.
    - expect: threadIdNuevo es distinto de threadIdAnterior.
    - expect: El resultado observable cubre THR-01: aparece un Thread ID activo distinto al anterior.
  6. Localizadores recomendados: getByRole('button', {name: /Nuevo thread/i}) para la accion; para el valor, localizar el elemento code dentro del contenedor que contiene el texto 'Thread ID' o usar un localizador semantico estable equivalente si el runner lo ofrece. No depender de los valores dinamicos ni de refs e* del snapshot.
    - expect: El boton se encuentra por nombre humano.
    - expect: El valor anterior y el nuevo se leen del mismo campo visible de Thread ID.
  7. Datos propios necesarios: ninguno; los dos IDs son generados por la aplicacion.
    - expect: No se fija un ID literal. La unica condicion de datos es que el segundo valor sea distinto del primero.
  8. Riesgos o fragilidad: el ID es dinamico y puede no estar disponible durante el rerender de Streamlit; esperar a que el valor nuevo sea visible antes de leerlo. El boton puede tener un nombre accesible que incluya el icono '➕', por lo que se recomienda regex parcial. Si no existe un selector semantico unico para el code, queda como localizador potencialmente fragil y debe documentarse antes de automatizar, sin modificar codigo ahora.
    - expect: El caso falla si no se puede leer el ID anterior, si el nuevo ID esta vacio, o si ambos valores son iguales.
    - expect: El caso no debe considerar suficiente que el boton haya sido pulsado: debe comprobar la desigualdad de los dos valores.
