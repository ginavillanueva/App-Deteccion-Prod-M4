# PLAN_05 Evidencia multimodal

## Application Overview

Plan Playwright exclusivamente para EVI-01, EVI-02 y EVI-03 de la aplicacion real App Deteccion Prod en http://127.0.0.1:8501/. La interfaz es Streamlit: la pestaña exacta es "2 · Evidencia multimodal". No se generan tests ni se planifican los 14 casos anteriores. Los casos parten de page.goto('/'); los cambios de widgets pueden provocar rerenders y deben validarse con assertions web-first o expect.poll, nunca con waitForTimeout/sleeps.

## Test Scenarios

### 1. Evidencia multimodal (bloque oficial EVI)

**Seed:** `NO USAR SEED NI GENERAR TEST; exploracion realizada sobre http://127.0.0.1:8501/`

#### 1.1. EVI-01 - Subir audio y confirmar transcripcion

**File:** `NO GENERAR TEST - solo plan`

**Steps:**
  1. ID y objetivo: EVI-01. Desde un estado independiente, navegar con page.goto('/') y abrir la pestaña accesible "2 · Evidencia multimodal". Confirmar que existe el flujo real para subir audio y escribir su transcripcion confirmada.
    - expect: La pestaña "2 · Evidencia multimodal" queda seleccionada; esperar el tabpanel por rol/nombre o por texto visible, porque el primer render puede dejarlo temporalmente vacio. La interfaz muestra el encabezado "🎤 Audio" y el texto de ayuda que indica WAV/MP3/M4A/OGG.
  2. Precondiciones y datos/fixture: usar el thread que la propia UI muestra como "Thread de evidencia: <id>"; no inventar ni fijar el valor del id. Fixture recomendado: un archivo real y pequeño de audio con contenido mínimo válido, preferiblemente WAV PCM mono, por ejemplo 1 segundo de silencio o una frase corta; la UI también acepta MP3, M4A y OGG y muestra límite de 200 MB por archivo. No existe fixture de audio identificado en el repositorio explorado.
    - expect: El caso es independiente y no reutiliza estado de otro caso. La transcripcion no se reconoce automáticamente: debe ser texto humano confirmado en el campo real "Transcripcion confirmada".
  3. Localizadores y upload: localizar el control por getByRole('button', {name: 'Subir evidencia de audio'}) o por su label accesible exacto; al activarlo, manejar el file chooser y aplicar setInputFiles al input asociado, con un único archivo del fixture y extensión permitida. No depender del botón interno genérico "Browse files" ni de clases CSS de Streamlit.
    - expect: La UI real abre un file chooser. Tras seleccionar el archivo, esperar web-first a que el nombre del archivo o el estado del uploader aparezca bajo "Subir evidencia de audio"; si el rerender reemplaza el nodo, volver a localizar por nombre accesible. No afirmar una transcripcion automática: la app solo dice que la confirmación es manual.
  4. Confirmación: localizar getByRole('textbox', {name: 'Transcripcion confirmada'}) y rellenar una frase determinista que corresponda al fixture, por ejemplo "Audio de evidencia de prueba.". Validar el valor con expect(locator).toHaveValue(...).
    - expect: El textbox conserva el texto después del rerender de Streamlit. El placeholder real observado es "Ej.: Estoy en Hipermaxi Calacoto; encontre este producto y vence pronto.".
  5. Resultado observable y persistencia: observar el estado inmediato del uploader y del textbox. La pestaña no expone botón de guardar/confirmar adicional. Para que la evidencia quede persistida y asociada al mismo thread, la implementación solo llama persist_evidence durante EJECUTAR, PAUSAR, REANUDAR o RECUPERAR en la pestaña "1 · Operacion"; esa acción es una dependencia de persistencia, no un nuevo caso EVI.
    - expect: Resultado inmediato verificable: archivo seleccionado visible en el uploader y transcripcion confirmada visible en el textbox. Resultado persistido verificable solo después de un disparador operativo: metadata bajo el thread actual contiene audio y transcripcion_confirmada; la UI comunica "Ejecucion real completada y evidencia trazada." cuando corresponde. No exigir una confirmación que la pestaña no expone.
  6. Estrategia de asincronía, riesgos y data-testid: después de cada interacción de widget, esperar el control o texto final con expect(...).toBeVisible(), toHaveValue() o expect.poll sobre la condición observable. No usar waitForTimeout ni sleeps. Riesgos: rerenders reemplazan locators; el hash SHA-256 y la asociación persistida no se muestran dentro de esta pestaña; seleccionar un archivo válido no equivale por sí solo a persistirlo; no hay data-testid expuesto ni indispensable.
    - expect: Automatizable: sí para upload y confirmación de texto; la verificación de persistencia requiere el disparador operativo descrito y una observación posterior de metadata/trazabilidad.

#### 1.2. EVI-02 - Subir imagen y confirmar descripcion

**File:** `NO GENERAR TEST - solo plan`

**Steps:**
  1. ID y objetivo: EVI-02. Desde un estado independiente, ejecutar page.goto('/') y abrir "2 · Evidencia multimodal". Confirmar el flujo real de imagen por upload, no el de cámara.
    - expect: La pestaña seleccionada muestra la sección real "📷 Foto", el control "O subir imagen" y el textbox "Lectura/descripcion confirmada".
  2. Precondiciones y datos/fixture: fixture de imagen pequeño, válido y no ambiguo, preferiblemente PNG o JPEG con una etiqueta/producto visible y una resolución moderada; la UI acepta JPG, JPEG, PNG y WEBP y muestra límite de 200 MB por archivo. No se inventa una descripción automática: el texto se confirma manualmente.
    - expect: El fixture debe permitir una descripción humana reproducible, por ejemplo que contenga producto, presentación y fecha visible. El repositorio no expone un fixture de imagen de producto dedicado; los PNG de docs/evidencias son capturas de documentación y no deben tratarse como fixture funcional sin verificar su contenido.
  3. Localizadores y upload: localizar getByRole('button', {name: 'O subir imagen'}) o su label accesible exacto, activar el file chooser y usar setInputFiles con el fixture. No usar el botón interno genérico "Browse files" como contrato principal.
    - expect: El selector real de archivo se abre. Tras setInputFiles, esperar que el archivo seleccionado sea visible en el uploader; si el preview se materializa, esperar la imagen/estado por assertions web-first, no por tiempo fijo.
  4. Confirmación: localizar getByRole('textbox', {name: 'Lectura/descripcion confirmada'}) y escribir una descripción determinista acorde al fixture. Comprobar toHaveValue() tras el rerender.
    - expect: El textbox conserva la descripción. El placeholder real observado es "Ej.: Producto, presentacion y fecha visible en la etiqueta.". Si hay archivo en session state, la app puede mostrar la evidencia visual con el caption real "Evidencia visual capturada".
  5. Resultado observable y persistencia: afirmar el archivo/preview y el valor confirmado en la misma pestaña. La asociación al thread no tiene botón propio: para persistirla la implementación recoge upload y texto y llama persist_evidence durante EJECUTAR, PAUSAR, REANUDAR o RECUPERAR; no mezclar ni volver a planificar los casos OPE ya terminados.
    - expect: Resultado inmediato: archivo de imagen seleccionado, posible preview con caption "Evidencia visual capturada" y descripción visible en el textbox. Resultado persistido, si se activa el disparador operativo permitido: metadata del thread contiene foto y lectura_foto_confirmada.
  6. Estrategia de asincronía, riesgos y data-testid: esperar la aparición del nombre/preview y el valor del textbox con locators semánticos y expect.poll solo para condiciones observables. No usar sleeps. Riesgos: rerender de Streamlit, preview no necesariamente expuesto como nombre accesible estable, hash no visible en esta pestaña, y fixture con contenido no legible haría la confirmación no auditable. No se observó data-testid útil o indispensable.
    - expect: Automatizable: sí para upload y confirmación de descripción; la persistencia completa depende del disparador operativo y de la observación de metadata/trazabilidad.

#### 1.3. EVI-03 - Activar camara y verificar captura disponible

**File:** `NO GENERAR TEST - solo plan`

**Steps:**
  1. ID y objetivo: EVI-03. Desde page.goto('/') independiente, abrir "2 · Evidencia multimodal", localizar la casilla accesible "Activar camara" y activarla.
    - expect: La casilla queda checked después del rerender de Streamlit. La UI real agrega el control con label "Tomar foto del producto" y el botón "Take Photo".
  2. Estrategia de permisos y browser configuration: ejecutar Chromium con permisos de contexto camera concedidos para http://127.0.0.1:8501 y con un dispositivo de vídeo falso, por ejemplo args --use-fake-device-for-media-stream, --use-fake-ui-for-media-stream y --use-file-for-fake-video-capture=<fixture.y4m>. El fixture de cámara debe ser un vídeo Y4M válido y corto, con una imagen estable del producto; no es un archivo de upload de imagen. Mantener la configuración en el proyecto/contexto Playwright, no intentar setInputFiles sobre camera_input.
    - expect: Con permisos y dispositivo disponibles, el widget puede habilitar el botón "Take Photo". En la exploración sin esos permisos/dispositivo, la UI mostró literalmente "This app would like to use your camera." y "Take Photo" disabled; ese estado es un bloqueo observable, no una captura disponible.
  3. Automatización de captura: después de que el botón "Take Photo" esté enabled, hacer click por getByRole('button', {name: 'Take Photo'}), esperar web-first el resultado de captura que exponga Streamlit y verificar que aparezca la evidencia visual/caption "Evidencia visual capturada" o el estado de imagen observable. No inventar un selector de input: st.camera_input no expone el mismo contrato que st.file_uploader.
    - expect: La captura queda disponible en el widget y puede ser tomada como photo_camera_key por la aplicación. La verificación mínima del inventario es control de captura de foto disponible; si además se confirma descripción, eso pertenece al control observado "Lectura/descripcion confirmada" y no debe confundirse con reconocimiento automático.
  4. Resultado observable, rerender y riesgos: esperar el checked state, la aparición del label y el enabled state con assertions web-first. Si el navegador no permite cámara, afirmar el aviso real de permiso y marcar el caso bloqueado por configuración, no simular un click exitoso. Streamlit puede rerenderizar y reemplazar el widget después de activar la casilla.
    - expect: Resultado exitoso: "Activar camara" checked, "Tomar foto del producto" visible y "Take Photo" habilitado para captura. Resultado observado en la sesión actual sin configuración especial: aviso de acceso y botón disabled. Riesgos: permisos del contexto, soporte de cámara en el navegador, disponibilidad del fake video, diferencias de plataforma y rerenders. No se observó data-testid útil o indispensable.
  5. Fixture requerido: no se necesita audio ni imagen para el control de cámara; sí se necesita un vídeo Y4M de cámara falsa si se desea automatizar el click de captura de extremo a extremo. No usar waitForTimeout ni sleeps; usar expect(locator).toBeEnabled(), toBeVisible() y, tras capturar, expect.poll sobre la aparición del preview/estado observable.
    - expect: Automatizable: sí, condicionado a Chromium configurado con permisos camera y fuente de vídeo falsa; no es automatizable de forma fiable en la configuración actual, donde el permiso/dispositivo no está disponible.
