from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["demo-ui"])


@router.get("/app", response_class=HTMLResponse)
def demo_app() -> str:
    """Interfaz aplicada para demostrar dos features trazables.

    La UI consume los endpoints existentes de la API. Las reglas de negocio siguen
    viviendo en dominio/aplicación y la capa visual solo presenta el flujo para
    mercaderista, supervisor y gerencia.
    """

    return r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>App Detección Prod · Demo visual trazable</title>
  <style>
    :root {
      --bg: #f3f6fb;
      --panel: #ffffff;
      --ink: #101828;
      --muted: #667085;
      --line: #d6deea;
      --brand: #175cd3;
      --brand-dark: #0b2f66;
      --brand-2: #0f766e;
      --soft: #edf4ff;
      --warn: #b45309;
      --danger: #b42318;
      --ok: #047857;
      --violet: #6941c6;
      --shadow: 0 12px 28px rgba(16, 24, 40, 0.10);
      --radius: 18px;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--bg); color: var(--ink); }
    header {
      background: radial-gradient(circle at top left, #2e90fa, #174ea6 45%, #102a43 100%);
      color: white;
      padding: 28px 32px 42px;
    }
    .hero { max-width: 1240px; margin: 0 auto; display: grid; gap: 14px; }
    .hero h1 { margin: 0; font-size: 34px; line-height: 1.05; }
    .hero p { margin: 0; max-width: 960px; color: #dbeafe; font-size: 16px; }
    .badges { display: flex; flex-wrap: wrap; gap: 8px; }
    .badge { background: rgba(255,255,255,.17); border: 1px solid rgba(255,255,255,.30); color: white; border-radius: 999px; padding: 7px 11px; font-size: 12px; font-weight: 700; }
    main { max-width: 1240px; margin: -26px auto 56px; padding: 0 18px; }
    nav { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 18px; position: sticky; top: 0; z-index: 20; padding: 8px 0; background: linear-gradient(180deg, rgba(243,246,251,.96), rgba(243,246,251,.72)); backdrop-filter: blur(6px); }
    nav button, .btn {
      border: 0; background: var(--panel); color: var(--ink); padding: 10px 14px; border-radius: 999px;
      box-shadow: var(--shadow); cursor: pointer; font-weight: 800;
    }
    nav button.active { background: var(--brand); color: white; }
    section { display: none; }
    section.active { display: block; }
    .grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 18px; }
    .card { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 18px; box-shadow: var(--shadow); }
    .card.soft { background: linear-gradient(180deg, #ffffff, #f8fbff); }
    .span-3 { grid-column: span 3; }
    .span-4 { grid-column: span 4; }
    .span-5 { grid-column: span 5; }
    .span-6 { grid-column: span 6; }
    .span-7 { grid-column: span 7; }
    .span-8 { grid-column: span 8; }
    .span-9 { grid-column: span 9; }
    .span-12 { grid-column: span 12; }
    @media (max-width: 980px) { .span-3, .span-4, .span-5, .span-6, .span-7, .span-8, .span-9 { grid-column: span 12; } }
    h2, h3 { margin-top: 0; }
    h2 { font-size: 24px; }
    label { display: block; font-size: 12px; color: var(--muted); font-weight: 800; margin: 12px 0 6px; text-transform: uppercase; letter-spacing: .03em; }
    input, select, textarea {
      width: 100%; padding: 11px 12px; border: 1px solid var(--line); border-radius: 12px; font-size: 14px; background: #fff;
    }
    textarea { min-height: 78px; resize: vertical; }
    .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0 14px; }
    @media (max-width: 760px) { .form-grid { grid-template-columns: 1fr; } }
    .primary { background: var(--brand); color: white; border: 0; padding: 12px 16px; border-radius: 12px; cursor: pointer; font-weight: 900; margin-top: 14px; }
    .secondary { background: var(--brand-2); color: white; border: 0; padding: 11px 14px; border-radius: 12px; cursor: pointer; font-weight: 900; margin-right: 8px; }
    .danger { background: var(--danger); color: white; border: 0; padding: 11px 14px; border-radius: 12px; cursor: pointer; font-weight: 900; margin-right: 8px; }
    .ghost { background: #eef4ff; color: #1849a9; border: 1px solid #b2ccff; padding: 10px 12px; border-radius: 12px; cursor: pointer; font-weight: 900; margin-right: 8px; }
    .metric { padding: 15px; border: 1px solid var(--line); border-radius: 16px; background: #f8fafc; }
    .metric .value { font-size: 28px; font-weight: 950; margin-bottom: 3px; }
    .metric .label { font-size: 11px; color: var(--muted); font-weight: 800; text-transform: uppercase; letter-spacing: .05em; }
    .status { min-height: 36px; padding: 11px 13px; border-radius: 12px; margin: 12px 0 0; background: #eff6ff; color: #1849a9; font-weight: 800; }
    .status.ok { background: #ecfdf3; color: #027a48; }
    .status.warn { background: #fffaeb; color: #b54708; }
    .risk-BAJO { color: var(--ok); font-weight: 950; }
    .risk-MEDIO { color: var(--warn); font-weight: 950; }
    .risk-ALTO { color: var(--danger); font-weight: 950; }
    .case-list { display: grid; gap: 10px; max-height: 560px; overflow: auto; }
    .case-item { border: 1px solid var(--line); border-radius: 16px; padding: 13px; background: #fff; cursor: pointer; }
    .case-item:hover { border-color: var(--brand); }
    .case-item.selected { outline: 3px solid rgba(23,92,211,.18); border-color: var(--brand); }
    .small { font-size: 12px; color: var(--muted); }
    .note { color: var(--muted); line-height: 1.45; }
    pre { background: #101828; color: #e5e7eb; padding: 14px; border-radius: 14px; overflow: auto; max-height: 430px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th, td { text-align: left; border-bottom: 1px solid var(--line); padding: 9px; vertical-align: top; }
    th { color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: .04em; }
    .flow { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 12px; }
    .flow div { background: #eef4ff; border: 1px solid #b2ccff; border-radius: 14px; padding: 12px; text-align: center; font-weight: 900; font-size: 13px; }
    .step-card { display: flex; gap: 12px; align-items: flex-start; }
    .step-num { min-width: 34px; height: 34px; border-radius: 50%; background: var(--brand); color: white; display: grid; place-items: center; font-weight: 950; }
    .pill { display: inline-block; padding: 5px 9px; border-radius: 999px; background: #eef4ff; color: #1849a9; font-weight: 900; font-size: 12px; margin: 2px; }
    .filter-row { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; }
    @media (max-width: 980px) { .filter-row { grid-template-columns: repeat(2, 1fr); } }
    .chart { min-height: 250px; }
    .bar-row { display: grid; grid-template-columns: 120px 1fr 72px; gap: 10px; align-items: center; margin: 9px 0; }
    .bar-bg { height: 18px; background: #e6edf7; border-radius: 999px; overflow: hidden; }
    .bar-fill { height: 18px; border-radius: 999px; background: linear-gradient(90deg, #2e90fa, #175cd3); min-width: 3px; }
    .bar-fill.warn { background: linear-gradient(90deg, #f79009, #b54708); }
    .bar-fill.ok { background: linear-gradient(90deg, #12b76a, #027a48); }
    .bar-fill.danger { background: linear-gradient(90deg, #f04438, #b42318); }
    .chart-title { font-size: 14px; color: var(--muted); font-weight: 800; margin-bottom: 10px; }
    .donut-wrap { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }
    .donut { width: 150px; height: 150px; border-radius: 50%; background: conic-gradient(#175cd3 0 33%, #12b76a 33% 66%, #f79009 66% 100%); position: relative; }
    .donut::after { content: ''; position: absolute; inset: 34px; background: white; border-radius: 50%; box-shadow: inset 0 0 0 1px var(--line); }
    .legend { display: grid; gap: 8px; font-size: 13px; }
    .legend span { display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 6px; }
    .insight { border-left: 5px solid var(--brand); background: #f8fbff; padding: 12px; border-radius: 10px; margin: 10px 0; }
    .persona { display: grid; grid-template-columns: 64px 1fr; gap: 12px; align-items: center; }
    .evidence-box { margin-top: 10px; border: 1px dashed #98a2b3; border-radius: 16px; padding: 12px; background: #f8fbff; }
    .evidence-preview { display: grid; grid-template-columns: 132px 1fr; gap: 12px; align-items: center; margin-top: 10px; }
    .evidence-preview img { width: 132px; height: 92px; object-fit: cover; border-radius: 12px; border: 1px solid var(--line); background: white; }
    .evidence-thumb { width: 100%; max-width: 280px; border-radius: 14px; border: 1px solid var(--line); margin-top: 8px; box-shadow: var(--shadow); }
    .evidence-empty { padding: 12px; border-radius: 12px; background: #fffaeb; color: #b54708; font-weight: 800; }
    .avatar { width: 58px; height: 58px; border-radius: 18px; display: grid; place-items: center; background: #eef4ff; font-size: 30px; }
    @media (max-width: 800px) { .flow { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <h1>App Detección Prod · Demo aplicada de 2 features · visual trazable</h1>
      <p>Demostración para evaluación: registro de producto crítico por mercaderista, validación supervisora y dashboard gerencial con filtros, análisis regional/nacional, gráficos e indicadores de precio, riesgo y acciones comerciales.</p>
      <div class="badges">
        <span class="badge">FEAT-001 · Registro mercaderista</span>
        <span class="badge">FEAT-002 · Supervisión + Dashboard gerencial</span>
        <span class="badge">Trazabilidad: FSD → DD → ADR → Prompt → Código → Tests</span>
        <span class="badge">Cobertura objetivo ≥90%</span>
      </div>
    </div>
  </header>

  <main>
    <nav>
      <button data-tab="inicio" class="active">Inicio</button>
      <button data-tab="registro">1. Mercaderista registra</button>
      <button data-tab="supervisor">2. Bandeja supervisor</button>
      <button data-tab="dashboard">3. Gerencia analiza</button>
      <button data-tab="eventos">4. Eventos y trazabilidad</button>
    </nav>

    <section id="inicio" class="active">
      <div class="grid">
        <div class="card span-12 soft">
          <h2>Recorrido de la demo desde cero</h2>
          <p class="note">Esta pantalla está dirigida al docente y al público evaluador. La demo muestra el producto aplicado, no solamente endpoints: el flujo inicia con el mercaderista en campo, pasa por la validación del supervisor y termina en un dashboard gerencial con análisis nacional, regional y operativo.</p>
          <div class="flow">
            <div>1. Detectar producto</div><div>2. Registrar evidencia</div><div>3. Calcular riesgo</div><div>4. Validar caso</div><div>5. Analizar KPIs</div>
          </div>
        </div>
        <div class="card span-4">
          <div class="persona"><div class="avatar">🛒</div><div><h3>Mercaderista</h3><p class="note">Registra tienda, producto, lote, vencimiento, cantidad, precio, acción comercial y evidencia desde una pantalla estructurada.</p></div></div>
        </div>
        <div class="card span-4">
          <div class="persona"><div class="avatar">✅</div><div><h3>Supervisor</h3><p class="note">Revisa el caso, observa el score, valida o rechaza, y deja comentario para auditoría.</p></div></div>
        </div>
        <div class="card span-4">
          <div class="persona"><div class="avatar">📊</div><div><h3>Gerencia</h3><p class="note">Filtra por vista nacional, región, canal, cadena, riesgo y acción comercial para priorizar decisiones.</p></div></div>
        </div>
        <div class="card span-12">
          <button class="danger" id="resetBtn">Reiniciar demo</button>
          <button class="secondary" id="seedBtn">Cargar un caso ejemplo</button>
          <button class="ghost" id="portfolioBtn">Cargar cartera nacional para dashboard</button>
          <div class="status" id="homeStatus">Lista para iniciar una demo limpia.</div>
        </div>
      </div>
    </section>

    <section id="registro">
      <div class="grid">
        <div class="card span-7">
          <h2>FEAT-001 · Registro visual desde rol mercaderista</h2>
          <p class="note">El formulario reemplaza reportes dispersos por WhatsApp/Excel. Cada campo genera datos útiles para auditoría, riesgo, precio y dashboard.</p>
          <div id="storeContext" class="status">Contexto tienda: seleccione tienda para ver región, canal y cadena.</div>
          <form id="caseForm">
            <div class="form-grid">

<div><label>Departamento</label>
<select id="departmentSelect" required></select></div>
<div><label>Cadena comercial</label>
<select id="chainSelect" required></select></div>
<div><label>Tienda / punto de venta</label>
<select name="store" id="storeSelect" required></select></div>
              <div><label>Producto</label><input name="product_name" value="0000093000-ACEITE DE OLIVA EXTRA VIRGEN 6X1L" required /></div>
              <div><label>Lote</label><input name="batch" value="DEMO-ACEITE-001" required /></div>
              <div><label>Fecha de vencimiento</label><input name="expiration_date" type="date" required /></div>
              <div><label>Cantidad detectada</label><input name="quantity" type="number" value="12" min="1" required /></div>
              <div><label>Precio actual</label><input name="current_price" type="number" step="0.01" value="150" required /></div>
              <div><label>Nuevo precio sugerido/aplicado</label><input name="new_price" type="number" step="0.01" value="120" /></div>
              <div><label>Acción comercial</label><select name="commercial_action"><option>DESCUENTO</option><option>BANDEO</option><option>PROMOCION</option><option>RETIRO</option><option>PENDIENTE</option></select></div>
              <div><label>Cambio de precio aprobado</label><select name="price_change_approved"><option value="true">Sí</option><option value="false">No</option></select></div>
              <div><label>Usuario que registra</label><input name="created_by" value="mercaderista.demo" /></div>
            </div>
            <label>Motivo del cambio de precio</label><textarea name="price_change_reason">Descuento autorizado por supervisor</textarea>
            <label>Evidencia observada en sala</label><textarea name="evidence_note">Foto clara de góndola y etiqueta de precio</textarea>
            <div class="evidence-box">
              <label>Evidencia fotográfica visible para supervisión</label>
              <input id="evidencePhoto" name="evidence_photo_file" type="file" accept="image/*" />
              <div id="evidencePreview" class="evidence-preview">
                <img id="evidencePreviewImg" alt="Vista previa de evidencia fotográfica" src="" style="display:none" />
                <div><b id="evidencePreviewTitle">Sin foto adjunta todavía</b><p class="small">Para una demo completa, adjunte una captura o foto de góndola/etiqueta. La imagen se vincula al caso y luego aparece en la bandeja del supervisor.</p></div>
              </div>
            </div>
            <button class="primary" type="submit">Registrar caso crítico</button>
          </form>
          <div class="status" id="registerStatus">Completa el formulario y registra el caso.</div>
        </div>
        <div class="card span-5">
          <h3>Resultado explicado</h3>
          <div id="lastCaseSummary" class="case-list"><p class="small">Aquí aparecerán riesgo, score, SLA, precio, descuento y explicación de variables.</p></div>
        </div>
      </div>
    </section>

    <section id="supervisor">
      <div class="grid">
        <div class="card span-7">
          <h2>FEAT-002 · Bandeja de supervisión</h2>
          <p class="note">El supervisor deja de validar mensajes dispersos. Selecciona un caso centralizado, revisa su riesgo, precio, evidencia y decide.</p>
          <div id="casesList" class="case-list"></div>
        </div>
        <div class="card span-5">
          <h3>Validación del supervisor</h3>
          <p class="small">Caso seleccionado:</p>
          <div id="selectedCase" class="case-list">Seleccione un caso de la lista.</div>
          <form id="validateForm">
            <label>Usuario supervisor</label><input name="supervisor_user" value="supervisor.demo" required />
            <label>Decisión</label><select name="decision"><option>APROBADO</option><option>RECHAZADO</option><option>OBSERVADO</option></select>
            <label>Comentario</label><textarea name="comment">Caso validado porque tiene evidencia, acción comercial y precio autorizado.</textarea>
            <button class="primary" type="submit">Validar caso seleccionado</button>
          </form>
          <div class="status" id="validationStatus">Pendiente de seleccionar caso.</div>
        </div>
      </div>
    </section>

    <section id="dashboard">
      <div class="grid">
        <div class="card span-12">
          <h2>FEAT-002 · Dashboard gerencial con análisis nacional y regional</h2>
          <p class="note">La gerencia puede analizar impacto financiero, riesgo, cambios de precio, acciones comerciales, canal, cadena y región. Los gráficos se recalculan con los filtros.</p>
          <div class="filter-row">
            <div><label>Vista</label><select id="filterScope"><option value="TODOS">Nacional</option><option value="REGIONAL">Regional</option></select></div>
            <div><label>Región</label><select id="filterRegion"><option value="TODOS">Todas</option></select></div>
            <div><label>Canal</label><select id="filterChannel"><option value="TODOS">Todos</option></select></div>
            <div><label>Cadena</label><select id="filterChain"><option value="TODOS">Todas</option></select></div>
            <div><label>Riesgo</label><select id="filterRisk"><option value="TODOS">Todos</option><option>ALTO</option><option>MEDIO</option><option>BAJO</option></select></div>
            <div><label>Acción</label><select id="filterAction"><option value="TODOS">Todas</option><option>DESCUENTO</option><option>BANDEO</option><option>PROMOCION</option><option>RETIRO</option><option>PENDIENTE</option></select></div>
          </div>
          <button class="secondary" onclick="refreshAll()">Actualizar dashboard</button>
          <button class="ghost" id="portfolioBtnDashboard">Cargar cartera nacional demo</button>
        </div>
        <div class="span-12 grid" id="metricsGrid"></div>
        <div class="card span-6 chart"><h3>Riesgo por nivel</h3><div id="riskChart"></div></div>
        <div class="card span-6 chart"><h3>Valor financiero por región</h3><div id="regionChart"></div></div>
        <div class="card span-6 chart"><h3>Acciones comerciales</h3><div id="actionChart"></div></div>
        <div class="card span-6 chart"><h3>Análisis por canal</h3><div id="channelChart"></div></div>
        <div class="card span-6"><h3>Ranking regional</h3><div id="regionTable"></div></div>
        <div class="card span-6"><h3>Insights ejecutivos</h3><div id="insightsBox"></div></div>

        <div class="card span-12">
          <h3>Consulta detallada de casos</h3>
          <p class="note">Casos correspondientes a los filtros seleccionados.</p>
          <div id="casesDetailTable" style="overflow-x:auto"></div>
          <h3>Detalle del caso seleccionado</h3>
          <pre id="caseDetailJson">Seleccione un caso.</pre>
        </div>

        <div class="card span-12"><h3>JSON técnico del dashboard</h3><pre id="dashboardJson">Cargando...</pre></div>
      </div>
    </section>

    <section id="eventos">
      <div class="grid">
        <div class="card span-6"><h2>Eventos de dominio</h2><p class="small">Evidencian auditoría: registro, cambio de precio, clasificación de riesgo y validación.</p><div id="eventsTable"></div></div>
        <div class="card span-6"><h2>Trazabilidad documental</h2><p class="small">Conecta requerimiento, FSD, diseño, ADR, prompt, código y tests.</p><pre id="traceabilityJson">Cargando...</pre></div></div>
      </div>
    </section>
  </main>

<script>
let selectedCaseId = null;
let evidencePhotoData = '';
let evidencePhotoName = '';

const storeCatalog = {"101797 - ANDYS SAN MIGUEL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Andys", "alcance": "Demo"}, "127814 - ANDYS ACHUMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Andys", "alcance": "Demo"}, "129024 - ANDYS OBRAJES": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Andys", "alcance": "Demo"}, "166151 - SUPERMERCADO HOME CENTER ANDYS": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Andys", "alcance": "Demo"}, "104835 - DE LICOR": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "DELICOR", "alcance": "Demo"}, "147109 - DE LICOR SAN MIGUEL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "DELICOR", "alcance": "Demo"}, "153493 - DE LICOR PLAZA ABAROA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "DELICOR", "alcance": "Demo"}, "155081 - DE LICOR ACHUMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "DELICOR", "alcance": "Demo"}, "166022 - DISMAC": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "DISMAC", "alcance": "Demo"}, "147675 - FARMACIA CHAVEZ S.A.": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Chavez", "alcance": "Demo"}, "158016 - FARMACIA HIPERMAXI ACHUMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "158017 - FARMACIA HIPERMAXI OBRAJES": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "158018 - FARMACIA HIPERMAXI CALACOTO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "158019 - FARMACIA HIPERMAXI LOS PINOS": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "158020 - FARMACIA HIPERMAXI SATELITE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "158021 - FARMACIA HIPERMAXI COTA COTA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "158022 - FARMACIA HIPERMAXI COSTANERA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "158023 - FARMACIA HIPERMAXI 20 DE OCTUBRE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "139042 - FARMACIAS CATEDRAL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacias Catedral", "alcance": "Demo"}, "167406 - FARMACIAS EDISA S.R.L.": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacias Edisa", "alcance": "Demo"}, "142563 - FARMACORP S.A. CENTRAL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMACORP", "alcance": "Demo"}, "167424 - FARMACIAS FARMACOSTO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMACOSTO", "alcance": "Demo"}, "167391 - FARMAELIAS CALACOTO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "167392 - FARMAELIAS CENTRAL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "167426 - FARMAELIAS ORURO PLAZA PRINCIPAL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "167405 - FARMACIA FARMAKOS ALTO OBRAJES": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMAKOS", "alcance": "Demo"}, "108313 - FIDALGA AVAROA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "101390 - HIPERMAXI CALACOTO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "101391 - HIPERMAXI MIRAFLORES": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "107949 - HIPERMAXI SOPOCACHI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "110958 - HIPERMAXI LOS PINOS": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "123778 - HIPERMAXI SATELITE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "128329 - HIPERMAXI ACHUMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "128526 - HIPERMAXI OBRAJES": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "144404 - HIPERMAXI SA TORRES DEL POETA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "145339 - HIPERMAXI SA SUC RIO SECO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "155037 - HIPERMAXI COTA COTA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "159689 - MICRO MARKET ILLIMARKET": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Illimarket", "alcance": "Demo"}, "105610 - MICROMARKET MILENIUM": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "105612 - ALMACEN JUAN DEL SUR": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "110640 - SURCO ZEGARRA JUAN MANUEL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "142188 - CLAUDIA MARGOT QUISPE CHOQUE JUAN DEL SUR SUC. IRPAVI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "145324 - ROBERT SURCO ZEGARRA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "155080 - WILMA MIRIAM SURCO ZEGARRA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "155390 - CLAUDIA MARGOT QUISPE CHOQUE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "155438 - JUAN DEL SUR ACHUMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "155439 - JUAN DEL SUR COTA COTA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "155590 - CAMILA NICOL CHIPANA SURCO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "157371 - JHONATAN CALEB SURCO DELGADO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "101392 - KETAL ARCE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Ketal", "alcance": "Demo"}, "101393 - KETAL 15": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Ketal", "alcance": "Demo"}, "101776 - KETAL 21": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Ketal", "alcance": "Demo"}, "102445 - KETAL MIRAFLORES": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Ketal", "alcance": "Demo"}, "110650 - KETAL IRPAVI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Ketal", "alcance": "Demo"}, "120631 - KETAL SAN PEDRO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Ketal", "alcance": "Demo"}, "127310 - KETAL ACHUMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Ketal", "alcance": "Demo"}, "129467 - CENTRO DE ABASTECIMIENTO KETAL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Ketal", "alcance": "Demo"}, "166009 - SUPERMERCADO MAKRO ABASTO VITA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Makro-Abasto", "alcance": "Demo"}, "166103 - SUPERMERCADO MAKRO ABASTO FARO MURILLO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Makro-Abasto", "alcance": "Demo"}, "166104 - SUPERMERCADO MAKRO ABASTO TELEFERICO MORADO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Makro-Abasto", "alcance": "Demo"}, "166046 - JACHA MACROCENTER SRL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Makro-Abasto", "alcance": "Demo"}, "149034 - MISUPER S.R.L.": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "MISUPER", "alcance": "Demo"}, "158201 - MULTICENTER SRL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "MULTICENTER", "alcance": "Demo"}, "157377 - QUALITY FOOD FLORES & ROBLES S.R.L.": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "102242 - REPOSTERIA PIGALLE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "114099 - HELADERIA FLAVOR BURST": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "128671 - CAFE TGF": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "128893 - DEARMIDA PINTO MAMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "142301 - PASTELERIA MICHELLINE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "143300 - PULPERIA F.D.T.E.U.L.P.": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "144960 - CLIENTE EVENTUAL 734": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "144962 - CLIENTE EVENTUAL 732": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "159772 - CHOCOLATERIA CHOCOPOP": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "166025 - PIZZERIA NEWYORK": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "158115 - NEWYORK PIZZA S.R.L": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "135632 - JHOEL LLIULLY YUJRA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "167421 - RESTAURANT SILLPICHS": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "159524 - TIENDA AMIGA TORRES MALL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Tienda Amiga", "alcance": "Demo"}, "166212 - SUPERMERCADO XPRESSMARKET O&P ESTACION CENTRAL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "XPRESSMARKET", "alcance": "Demo"}, "162111 - SUPERMERCADO XPRESSMARKET O&P SAN MIGUEL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "XPRESSMARKET", "alcance": "Demo"}, "166213 - SUPERMERCADO XPRESSMARKET O&P SATELITE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "XPRESSMARKET", "alcance": "Demo"}, "166119 - SUPERMERCADO ZUMARKET": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Zumarket", "alcance": "Demo"}, "251137 - ACRICOLOR ARTE SRL": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Acricolor", "alcance": "Demo"}, "200089 - BRANDS SOCIEDAD DE RESPONSABILIDAD LIMITADA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Brands", "alcance": "Demo"}, "274662 - CAMSA INDUSTRIA Y COMERCIO S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "CAMSA", "alcance": "Demo"}, "216708 - DELICOR CENTRAL": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "DELICOR", "alcance": "Demo"}, "240522 - DELICOR VELARDE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "DELICOR", "alcance": "Demo"}, "252372 - DELICOR BANZER": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "DELICOR", "alcance": "Demo"}, "286024 - DELICOR REMANSO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "DELICOR", "alcance": "Demo"}, "235746 - DISMATEC S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "DISMAC", "alcance": "Demo"}, "255733 - FARMACIA CHAVEZ CENTRAL": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Farmacia Chavez", "alcance": "Demo"}, "202946 - FARMACIAS HIPERMAXI": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "273216 - FARMACIA DOCKWEILER": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Farmacias Dockweiler", "alcance": "Demo"}, "203238 - FARMACIA OKINAWA S.R.L.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Farmacias Okinawa", "alcance": "Demo"}, "210273 - FARMACORP": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "FARMACORP", "alcance": "Demo"}, "210738 - HAMACAS FIDALGA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Meger", "alcance": "Demo"}, "218918 - SHOPPING NORTE FIDALGA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Meger", "alcance": "Demo"}, "227769 - COTOCA FIDALGA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Meger", "alcance": "Demo"}, "236768 - LA SALLE FIDALGA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Meger", "alcance": "Demo"}, "261375 - BENI FIDALGA 5TO ANILLO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Meger", "alcance": "Demo"}, "290627 - MACRO FIDALGA LTDA.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Meger", "alcance": "Demo"}, "210003 - SUPERMERCADOS FIDALGA S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "210005 - SUPER SUR FIDALGA S.R.L.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "210736 - EKKO FIDALGA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "213882 - TROMPILLO FIDALGA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "218859 - EQUIPETROL FIDALGA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "229113 - SUPER URUBO FIDALGA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "264662 - FIDASUR S.R.L. SEVILLA LOS BOSQUES": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "264664 - FIDASUR S.R.L. BENI": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "264691 - FIDASUR S.R.L. TERRAZAS II": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "264692 - FIDASUR S.R.L. RIVIERA I": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "264693 - FIDASUR S.R.L. RIVIERA II": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "264694 - FIDASUR S.R.L. URUBO II": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "264695 - FIDASUR S.R.L. SEVILLA PINATAR": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "264696 - FIDASUR S.R.L. STRIPMALL": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "268197 - FIDASUR S.R.L. LOS JARDINES": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "268198 - MIA PLAZA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "210002 - HIPERMAXI NORTE S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "210937 - HIPERMAXI SUR S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "210938 - HIPERMAXI FLORIDA S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "215479 - HIPERMAXI LAS PALMAS S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "217550 - HIPERMAXI TRES PASOS AL FRENTE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "218310 - HIPERMAXI PAMPA DE LA ISLA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "218876 - HIPERMAXI SUPER CENTER": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "222425 - HIPERMAXI RADIAL 26": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "223109 - HIPERMAXI BENI": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "223987 - HIPERMAXI VILLA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "226472 - HIPERMAXI PIRAI": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "227177 - HIPERMAXI CANOTO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "227809 - HIPERMAXI ROCA Y CORONADO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "229668 - HIPERMAXI BLACUTT": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "230193 - HIPERMAXI PLAN 3000": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "231521 - HIPERMAXI LAS BRISAS": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "232528 - HIPERMAXI MONTERO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "233802 - HIPERMAXI EQUIPETROL": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "250091 - HIPERMAXI MUTUALISTA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "273875 - HIPERMAXI CAMBODROMO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "278752 - HIPERMAXI DOBLE VIA LA GUARDIA KM13": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "291147 - HIPERMAXI CENTRO S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "219069 - IC NORTE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Ic Norte", "alcance": "Demo"}, "246162 - MAKRO PARQUE 4TO ANILLO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Makro", "alcance": "Demo"}, "253265 - COMERCIALIZADORA MAYORISTA Y DISTRIBUIDORA K1KULJIS S.R.L.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Makro", "alcance": "Demo"}, "268496 - MAKRO MAYORISTA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Makro", "alcance": "Demo"}, "271060 - MERCAGUSTO S.R.L.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Mercagusto", "alcance": "Demo"}, "210940 - MULTI CENTER NORTE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "MULTICENTER", "alcance": "Demo"}, "213883 - MULTI CENTER SUR": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "MULTICENTER", "alcance": "Demo"}, "232421 - MULTICENTER OESTE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "MULTICENTER", "alcance": "Demo"}, "230060 - TATIANA PINTO GUTIERREZ": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "284469 - TIENDAS MAESTRO SA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "252084 - KATIA RIBERA APONTE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "266464 - SAUCEDO MOTORS S.R.L.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "270299 - UNIBIENES SEGUROS Y REASEGUROS PATRIMONIALES S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "245608 - ROHO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "ROHO", "alcance": "Demo"}, "284250 - SUPERMERCADOS MIXTURA SRL": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Super Mixtura", "alcance": "Demo"}, "243887 - TA DA REMANSO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "TA DA", "alcance": "Demo"}, "286329 - TAILOY SA BANZER STRIP": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Tailoy", "alcance": "Demo"}, "287223 - TAILOY SA GRIGOTA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Tailoy", "alcance": "Demo"}, "287224 - TAILOY SA BANZER TIENDAS NUR": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Tailoy", "alcance": "Demo"}, "223438 - SUPERMERCADO TIA 24 DE SEPTIEMBRE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Tia", "alcance": "Demo"}, "230553 - SUPERMERCADO TIA ALEMANA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Tia", "alcance": "Demo"}, "231537 - SUPERMERCADO TIA VENTURA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Tia", "alcance": "Demo"}, "261619 - TIA COTOCA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Tia", "alcance": "Demo"}, "200166 - SUPERMERCADOS TIA BENI": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Tia", "alcance": "Demo"}, "232604 - TIENDA AMIGA ER S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Tienda Amiga", "alcance": "Demo"}, "281066 - TIENDAS TRESBE S.A.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "TRESBE", "alcance": "Demo"}, "311572 - ABDIAS LOPEZ": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Abdias", "alcance": "Demo"}, "344882 - COMERCIAL CREX S.R.L": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "CREX", "alcance": "Demo"}, "353997 - DISMAC": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "DISMAC", "alcance": "Demo"}, "322271 - FARMACIA CHAVEZ(PLZ CALA CALA)": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Chavez", "alcance": "Demo"}, "322272 - FARMACIA CHAVEZ(BEIGING)": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Chavez", "alcance": "Demo"}, "322273 - FARMACIA CHAVEZ(SUECIA)": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Chavez", "alcance": "Demo"}, "322284 - FARMACIA CHAVEZ(PANAMERICANA)": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Chavez", "alcance": "Demo"}, "350678 - HIPERMAXI FARMACIA SACABA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "350680 - HIPERMAXI FARMACIA JUAN DE LA ROSA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "350681 - HIPERMAXI FARMACIA BLANCO GALINDO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "350682 - HIPERMAXI FARMACIA CIRCUNVALACION": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "350683 - HIPERMAXI FARMACIA PRADO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "350684 - HIPERMAXI FARMACIA SOFFER": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "359208 - HIPERMAXI FARMACIA PANAMERICANA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "358427 - SONIA BLANCA MERIDA NOGALES": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMACIA ZURICH", "alcance": "Demo"}, "328185 - FARMACORP BODEGA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMACORP", "alcance": "Demo"}, "357594 - FARMACIA SAN ELIAS S.R.L.": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357596 - FARMAELIAS AMERICA OESTE": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357597 - FARMAELIAS AMERICA Y TARIJA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357599 - FARMAELIAS  AMERICA ESTE": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357600 - FARMAELIAS AV.SEGUNDA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357602 - FARMAELIAS BELZU": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357604 - FARMAELIAS CALA CALA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357608 - FARMAELIAS ECOLOGICA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357609 - FARMAELIAS HIPODROMO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357612 - FARMAELIAS MELCHOR": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357617 - FARMAELIAS PRADO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357621 - FARMAELIAS RECOLETA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357622 - FARMAELIAS SIMON LOPEZ": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357623 - FARMAELIAS TARIJA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357625 - FARMAELIAS VILLAZON": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "353256 - FARMAELIAS S.R.L.": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357603 - FARMAELIAS BLANCO GALINDO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "307510 - SPM. HIPERMAXI S.A.-B. GALINDO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "307894 - SPM.HIPERMAXI S.A.-OQUENDO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "315042 - SPM.HIPERMAXI S.A.- JUAN DE LA ROSA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "319092 - HIPERMAXI - PRADO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "324070 - HIPERMAXI - SACABA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "329473 - HIPERMAXI S.A. TEMPORAL": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "358995 - HIPERMAXI PANAMERICANA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "338705 - HOMESTORE S R L": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Homestore", "alcance": "Demo"}, "302166 - SPM.IC NORTE S.A.-HIPODROMO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Ic Norte", "alcance": "Demo"}, "305717 - SPM.IC NORTE S.A.-AMERICA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Ic Norte", "alcance": "Demo"}, "351027 - MULTICERNTER UYUNI": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "MULTICENTER", "alcance": "Demo"}, "351030 - MULTICERNTER BEIGING": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "MULTICENTER", "alcance": "Demo"}, "328486 - VINOS Y PIQUEOS": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Otros", "alcance": "Demo"}, "306021 - SUPERMERCADO AMERICA SRL": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Super America", "alcance": "Demo"}, "345163 - WILLGREEN S.R.L.": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "WILLGREEN", "alcance": "Demo"}, "149261 - FARMACIA GRAN MAESTRO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMACIA GRAN MAESTRO", "alcance": "Demo"}, "357613 - FARMAELIAS PANAMERICANA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357619 - FARMAELIAS QUILLACOLLO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "357630 - FARMAELIAS CIRCUNVALACION ESTE": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "360370 - EMAPA  CENTRAL HAMIRAYA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "EMAPA", "alcance": "Demo"}, "360371 - EMAPA  BLANCO GALINDO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "EMAPA", "alcance": "Demo"}, "360372 - EMAPA  ZONA SUD SIGLO XX": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "EMAPA", "alcance": "Demo"}, "360373 - EMAPA  ZONA SUD AVENIDA 6 DE AGOSTO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "EMAPA", "alcance": "Demo"}, "360374 - EMAPA TIQUIPAYA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "EMAPA", "alcance": "Demo"}, "360375 - EMAPA  QUILLACOLLO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "EMAPA", "alcance": "Demo"}, "360382 - EMAPA  PETROLERA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "EMAPA", "alcance": "Demo"}, "360381 - EMAPA  HIPODROMO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "EMAPA", "alcance": "Demo"}, "360939 - SOFIA AL PASO AGENCIA JUAN DE LA ROSA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "360938 - SOFIA AL PASO AGENCIA VILLALOBOS": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "360937 - SOFIA AL PASO AGENCIA AV. AMÉRICA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "360942 - SOFIA AL PASO AGENCIA BLANCO GALINDO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "167480 - FARMACIAS DIVINA MISERICORDIA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Divina Misericordia", "alcance": "Demo"}, "108474 - FARMACIA JUAREZ I LINA CAROLA FLORES MACHICADO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Juarez", "alcance": "Demo"}, "167504 - SUPERMERCADO ZUMARKET MIRAFLORES": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Zumarket", "alcance": "Demo"}, "361485 - HIPERMAXI FARMACIA  BEIJING": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "167506 - FARMAELIAS S.R.L.": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "167507 - SUPERMERCADO XPRESSMARKET O&P ACHUMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "XPRESSMARKET", "alcance": "Demo"}, "362141 - SOFIA AL PASO SUCURSAL BATEON": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "168674 - FARMACIAS MOISES 2": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacias Moises", "alcance": "Demo"}, "169007 - FARMACIA JUAREZ COTA COTA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Juarez", "alcance": "Demo"}, "2001404 - SOFIA AL PASO BANZER 4TO Y 5TO ANILLO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001408 - SOFIA AL PASO ALEMANIA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001410 - SOFIA AL PASO BANZER 7MO ANILLO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001413 - SOFIA AL PASO ALEMANA 5TO ANILLO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001417 - SOFIA AL PASO RADIAL 27": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001449 - SOFIA AL PASO PROLONGACION BENI": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169277 - SOFIA LA PASO VILLA FATIMA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169278 - SOFIA AL PASO CALACOTO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169280 - SOFIA AL PASO JAIMES FREYRE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169282 - SOFIA AL PASO OBRAJES": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169283 - SOFIA AL PASO SATELITE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169285 - SOFIA AL PASO SAN PEDRO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169286 - SOFIA AL PASO MALLASA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169287 - SOFIA AL PASO SOPOCACHI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169288 - SOFIA AL PASO COTA COTA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169289 - SOFIA AL PASO LOAYZA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169290 - SOFIA AL PASO ACHUMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001446 - SOFIA AL PASO GRIGOTA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "160048 - MIGUEL ANGEL ALCON": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Micromarket 24/7", "alcance": "Demo"}, "169364 - SOFIA AL PASO IRPAVI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001447 - SOFIA AL PASO PARQUE INDUSTRIAL": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001450 - SOFIA AL PASO ARGENTINA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001451 - SOFIA AL PASO RADIAL 17 1/2": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001452 - SOFIA AL PASO SANTOS DUMONT": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169525 - FARMACIA HIPERMAXI RENACER": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "2001407 - SOFIA AL PASO MONTERO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001409 - SOFIA AL PASO URUBO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001411 - SOFIA AL PASO SEVILLA NORTE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001419 - SOFIA AL PASO EL PORTAL URUBO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001453 - SOFIA AL PASO CONAVI": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001454 - SOFIA AL PASO ROCA Y CORONADO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001455 - SOFIA AL PASO BUSCH": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001456 - SOFIA AL PASO VIRGEN DE COTOCA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2001457 - SOFIA AL PASO LA CHONTA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "322043 - GRANJA AVICOLA INTEGRAL SOFIA LTDA.": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "169861 - FARMACIA DERMAFARMA TELEFERICO ROJO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Dermafarma", "alcance": "Demo"}, "170110 - MICROMARKET YAM YAM CALLE POTOSI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Andys", "alcance": "Demo"}, "166192 - PEDIDOSYA SERVICIOS S.A.": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Pedidos Ya", "alcance": "Demo"}, "356758 - PEDIDOSYA SERVICIOS S.A. CBA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Pedidos Ya", "alcance": "Demo"}, "170010 - MICROMARKET YAM YAM SOPOCACHI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Andys", "alcance": "Demo"}, "200345 - PEDIDOSYA SERVICIOS S.A. SCZ NORTE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Pedidos Ya", "alcance": "Demo"}, "200346 - PEDIDOSYA SERVICIOS S.A. SCZ EQUIPETROL": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Pedidos Ya", "alcance": "Demo"}, "200347 - PEDIDOSYA SERVICIOS S.A. SCZ SUR": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Pedidos Ya", "alcance": "Demo"}, "170394 - MICROMARKET JUAN DE SUR LAS LOMAS ACHUMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Juan del Sur", "alcance": "Demo"}, "238174 - FARMACIA HIPERMAXI CENTENARIO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "223176 - FARMACIA HIPERMAXI ESPAÑA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "142544 - ELSA MENDOZA PATZI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Mikromarket Aquí", "alcance": "Demo"}, "170853 - MICROMARKET AQUI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Mikromarket Aquí", "alcance": "Demo"}, "170639 - HIPERMAXI IRPAVI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "171144 - SUPERMERCADO XPRESSMARKET SAN PEDRO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "XPRESSMARKET", "alcance": "Demo"}, "365014 - HIPERMAXI S.A": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "365072 - FARMACIA HIPERMAXI MELCHOR PEREZ": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "171263 - MICROMARKET ECOFAST TELEFERICO CELESTE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Micromarket Ecofast", "alcance": "Demo"}, "365145 - FARMACIA HIPERMAXI TADEO HAENKE": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "171325 - FARMACIA HIPERMAXI IRPAVI MEGACENTER": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "284297 - DELICOR ALEMANA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "DELICOR", "alcance": "Demo"}, "167399 - FARMACIA VIRGEN DE COPACABANA ALEJANDRINA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Virgen de Copacabana", "alcance": "Demo"}, "167400 - FARMACIA VIRGEN DE COPACABANA ASBUN": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Virgen de Copacabana", "alcance": "Demo"}, "167401 - FARMACIA VIRGEN DE COPACABANA CENTRAL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Virgen de Copacabana", "alcance": "Demo"}, "167402 - FARMACIA VIRGEN DE COPACABANA GENESIS": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Virgen de Copacabana", "alcance": "Demo"}, "167403 - FARMACIA VIRGEN DE COPACABANA SALVADOR DE SANTA ROZA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Virgen de Copacabana", "alcance": "Demo"}, "171465 - FARMACIA VIRGEN DE COPACABANA SAN MIGUEL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Virgen de Copacabana", "alcance": "Demo"}, "171466 - FARMACIA VIRGEN DE COPACABANA SOPOCACHI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Virgen de Copacabana", "alcance": "Demo"}, "142861 - MISUPER SRL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "MISUPER", "alcance": "Demo"}, "171806 - LEGENS SPORT BAR GRILL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "LEGENS SPORT BAR GRILL", "alcance": "Demo"}, "171827 - HOTEL RENNOVA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "HOTEL RENNOVA", "alcance": "Demo"}, "171824 - FARMACIA HIPERMAXI MONTENEGRO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "171855 - FARMAELIAS ACHUMANI": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "171922 - MIAGENCIA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Miagencia", "alcance": "Demo"}, "2006052 - TIENDA AMIGA ER S.A. SANTOS DUMONT": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Tienda Amiga", "alcance": "Demo"}, "366370 - TIENDA AMIGA ER S.A. AV.AYACUCHO": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Tienda Amiga", "alcance": "Demo"}, "172198 - JACHA MACROCENTER SRL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Makro-Abasto", "alcance": "Demo"}, "223998 - FARMACIA HIPERMAXI SANTOS DUMO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "173009 - FARMACIA  TE CUIDAMOS": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Te Cuidamos", "alcance": "Demo"}, "173158 - MINIMARKET HOPE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Minimarket Hope", "alcance": "Demo"}, "357624 - FARMAELIAS TERMINAL SACABA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "2006020 - FIDASUR VISTA VERDE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "359386 - HOGAR DE SABIDURIA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Hogar de Sabiduría", "alcance": "Demo"}, "283005 - J. SERVICE FOOD S.R.L.": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "J. SERVICE FOOD", "alcance": "Demo"}, "173418 - FARMACIAS HIPERMAXI MALL 21": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "173461 - HIPERMAXI HOGAR PLAZA 21": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Hipermaxi", "alcance": "Demo"}, "369147 - FARMAELIAS S.R.L.": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "369656 - FARMAELIAS SUC. VIEDMAN": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "173960 - FARMACIAS HIPERMAXI PINILLA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "144486 - FARMACIA  FRAY VICENTE BERNEDO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Farmacia Fray Vicente Bernedo", "alcance": "Demo"}, "173881 - EXPANDIA SOLUTIONS SRL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Nuba", "alcance": "Demo"}, "174012 - ANDYS NUBA SAN MIGUEL": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Nuba", "alcance": "Demo"}, "370023 - NUBA SRL. AV AMERICA": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Nuba", "alcance": "Demo"}, "370024 - NUBA SRL. AV SAN MARTIN": {"region": "Cochabamba", "zona": "Valle", "canal": "Moderno", "cadena": "Nuba", "alcance": "Demo"}, "2010714 - NUBA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Nuba", "alcance": "Demo"}, "2009540 - SOFIA AL PASO BENI": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "2010716 - SOFIA AL PASO BENI": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "SOFIA AL PASO", "alcance": "Demo"}, "174046 - FARMAELIAS BUSH": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "174063 - FARMAELIAS S.R.L": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "2010567 - FIDASUR S.R.L. VISTA VERDE": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "2010685 - FIDASUR S.R.L. SEVILLA TERRAZAS I": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Fidalga-Rosario", "alcance": "Demo"}, "274816 - FARMACIA HIPERMAXI SANTOS DUMONT 6TO ANILLO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "174279 - FARMAELIAS COSTANERA": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "FARMAELIAS", "alcance": "Demo"}, "2011409 - FARMACIAS ECONOMICA": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Farmacias Economica", "alcance": "Demo"}, "2010552 - ROHO TIENDA 3": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "ROHO", "alcance": "Demo"}, "2010550 - ROHO TIENDA 2": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "ROHO", "alcance": "Demo"}, "274849 - FARMACIA HIPERMAXI CENTENARIO": {"region": "Santa Cruz", "zona": "Oriente", "canal": "Moderno", "cadena": "Farmacia Hipermaxi", "alcance": "Demo"}, "174299 - SUPERMERCADO ZUMARKET SAN PEDRO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Zumarket", "alcance": "Demo"}, "174513 - SUPERMERCADO MAKRO ABASTO FEDERICO SUAZO": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "Makro-Abasto", "alcance": "Demo"}, "174499 - SUPERMERCADO XPRESSMARKET TELEFERICO CELESTE": {"region": "La Paz", "zona": "Occidente", "canal": "Moderno", "cadena": "XPRESSMARKET", "alcance": "Demo"}};

function addDays(days) { const d = new Date(); d.setDate(d.getDate() + days); return d.toISOString().slice(0, 10); }
function setStatus(id, message, kind='') { const el = document.getElementById(id); el.textContent = message; el.className = 'status ' + kind; }
function money(v) { return Number(v || 0).toFixed(2); }
function pct(n, d) { return d ? Math.round((n / d) * 100) : 0; }
function metaFor(caseOrStore) { const store = typeof caseOrStore === 'string' ? caseOrStore : caseOrStore.store; return storeCatalog[store] || { region: 'Sin región', zona: 'Sin zona', canal: 'Sin canal', cadena: 'Sin cadena', alcance: 'Sin alcance' }; }


function llenarSelector(id, opciones, seleccionado) {
  const sel = document.getElementById(id);
  sel.replaceChildren();
  opciones.forEach(valor => sel.add(new Option(valor, valor)));
  if (opciones.includes(seleccionado)) sel.value = seleccionado;
}

function actualizarSalas(preferida = '') {
  const dept = document.getElementById('departmentSelect').value;
  const cadena = document.getElementById('chainSelect').value;
  const opciones = Object.keys(storeCatalog).filter(
    s => storeCatalog[s].region === dept &&
         storeCatalog[s].cadena === cadena
  );
  llenarSelector('storeSelect', opciones, preferida);
  updateStoreContext();
}

function actualizarCadenas(preferida = '', salaPreferida = '') {
  const dept = document.getElementById('departmentSelect').value;
  const cadenas = [...new Set(
    Object.values(storeCatalog)
      .filter(m => m.region === dept)
      .map(m => m.cadena)
  )].sort();
  llenarSelector('chainSelect', cadenas, preferida);
  actualizarSalas(salaPreferida);
}

function setupStoreSelect() {
  const departamentos = [...new Set(
    Object.values(storeCatalog).map(m => m.region)
  )].sort();

  llenarSelector('departmentSelect', departamentos, 'Santa Cruz');

  document.getElementById('departmentSelect').addEventListener(
    'change', () => actualizarCadenas()
  );
  document.getElementById('chainSelect').addEventListener(
    'change', () => actualizarSalas()
  );
  document.getElementById('storeSelect').addEventListener(
    'change', updateStoreContext
  );

  actualizarCadenas('Hipermaxi', '210937 - HIPERMAXI SUR S.A.');
}
function updateStoreContext() {
  const meta = metaFor(document.getElementById('storeSelect').value);
  document.getElementById('storeContext').innerHTML = `Contexto tienda: <b>${meta.region}</b> · ${meta.zona} · ${meta.canal} · ${meta.cadena} · alcance ${meta.alcance}`;
}

document.querySelector('[name="expiration_date"]').value = addDays(26);
setupStoreSelect();

for (const btn of document.querySelectorAll('nav button')) {
  btn.addEventListener('click', () => {
    document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('section').forEach(s => s.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab).classList.add('active');
    refreshAll();
  });
}

async function api(path, options={}) {
  const response = await fetch(path, { headers: { 'Content-Type': 'application/json' }, ...options });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || JSON.stringify(data));
  return data;
}

function riskExplanation(c) {
  const rows = [
    ['Días al vencimiento', c.days_to_expiration, c.days_to_expiration <= 30 ? '+35' : c.days_to_expiration <= 45 ? '+28' : c.days_to_expiration <= 90 ? '+30' : '+0'],
    ['Valor financiero', money(c.financial_value_at_risk), c.financial_value_at_risk >= 3000 ? '+25' : c.financial_value_at_risk >= 1000 ? '+15' : '+0'],
    ['Acción comercial', c.commercial_action, c.commercial_action === 'PENDIENTE' ? '+25' : '+0'],
    ['Evidencia textual', c.evidence_note ? 'Registrada' : 'No registrada', c.evidence_note ? '+0' : '+12'],
    ['Evidencia fotográfica', c.evidence_photo_present ? 'Foto adjunta' : 'Sin foto', c.evidence_photo_present ? '+0' : 'control visual'],
    ['Cambio precio aprobado', c.price_audit.has_price_change ? (c.price_audit.price_change_approved ? 'Sí' : 'No') : 'Sin cambio', (c.price_audit.has_price_change && !c.price_audit.price_change_approved) ? '+20' : '+0'],
    ['Valor intervenido', money(c.intervened_value), c.intervened_value >= 1000 ? '+12' : '+0']
  ];
  return `<table><tr><th>Variable</th><th>Dato</th><th>Puntos</th></tr>${rows.map(r => `<tr><td>${r[0]}</td><td>${r[1]}</td><td><b>${r[2]}</b></td></tr>`).join('')}</table>`;
}

function caseCard(c) {
  const m = metaFor(c);
  return `<div class="case-item ${selectedCaseId === c.id ? 'selected' : ''}" onclick="selectCase('${c.id}')">
    <strong>${c.product_name}</strong> <span class="pill">${m.region}</span> <span class="pill">${m.canal}</span><br>
    <span class="small">${c.store} · ${m.cadena} · lote ${c.batch} · estado ${c.status}</span><br>
    Riesgo: <span class="risk-${c.risk_level}">${c.risk_level}</span> · Score ${c.risk.score} · SLA ${c.risk.sla_hours}h<br>
    Precio: ${money(c.price_audit.current_price)} → ${money(c.price_audit.new_price || c.price_audit.current_price)} · Desc. ${money(c.price_audit.discount_percent)}%<br>
    Valor en riesgo: ${money(c.financial_value_at_risk)} · Intervenido: ${money(c.intervened_value)}<br>
    Evidencia: ${c.evidence_photo_present ? '📷 Foto visible adjunta' : '📝 Solo nota textual'}
  </div>`;
}

function evidencePhotoHtml(c) {
  if (c.evidence_photo_present && c.evidence_photo_data) {
    return `<div class="evidence-box"><b>Evidencia fotográfica adjunta</b><p class="small">Archivo: ${c.evidence_photo_name || 'evidencia visual'}</p><img class="evidence-thumb" src="${c.evidence_photo_data}" alt="Evidencia fotográfica del caso" /></div>`;
  }
  return `<div class="evidence-empty">Sin foto adjunta. El caso conserva nota textual, pero para auditoría visual se recomienda adjuntar evidencia fotográfica.</div>`;
}

function selectedCaseView(c) {
  const m = metaFor(c);
  return `<div class="case-item selected">
    <strong>${c.product_name}</strong> <span class="pill">${m.region}</span> <span class="pill">${m.canal}</span> <span class="pill">${m.cadena}</span><br>
    <span class="small">${c.store} · lote ${c.batch} · estado ${c.status}</span><br>
    Riesgo: <span class="risk-${c.risk_level}">${c.risk_level}</span> · Score ${c.risk.score} · SLA ${c.risk.sla_hours}h<br>
    Precio: ${money(c.price_audit.current_price)} → ${money(c.price_audit.new_price || c.price_audit.current_price)} · Desc. ${money(c.price_audit.discount_percent)}%<br>
    Valor en riesgo: ${money(c.financial_value_at_risk)} · Intervenido: ${money(c.intervened_value)}<br>
    <b>Nota de evidencia:</b> ${c.evidence_note || 'Sin nota'}
    ${evidencePhotoHtml(c)}
    <details><summary>Ver JSON técnico completo</summary><pre>${JSON.stringify({ meta: m, case: c }, null, 2)}</pre></details>
  </div>`;
}

async function refreshCases() {
  const data = await api('/cases');
  const list = document.getElementById('casesList');
  list.innerHTML = data.cases.length ? data.cases.map(caseCard).join('') : '<p class="small">No existen casos registrados.</p>';
  if (selectedCaseId) {
    const selected = data.cases.find(c => c.id === selectedCaseId);
    document.getElementById('selectedCase').innerHTML = selected ? selectedCaseView(selected) : 'Seleccione un caso de la lista.';
  }
}

async function selectCase(id) {
  selectedCaseId = id;
  const data = await api(`/cases/${id}`);
  document.getElementById('selectedCase').innerHTML = selectedCaseView(data.case);
  setStatus('validationStatus', 'Caso seleccionado. Puede validarlo como supervisor.');
  refreshCases();
}

function filteredCases(cases) {
  const scope = document.getElementById('filterScope').value;
  const region = document.getElementById('filterRegion').value;
  const channel = document.getElementById('filterChannel').value;
  const chain = document.getElementById('filterChain').value;
  const risk = document.getElementById('filterRisk').value;
  const action = document.getElementById('filterAction').value;
  return cases.filter(c => {
    const m = metaFor(c);
    return (scope === 'TODOS' || m.alcance === 'Regional' || scope === 'REGIONAL')
      && (region === 'TODOS' || m.region === region)
      && (channel === 'TODOS' || m.canal === channel)
      && (chain === 'TODOS' || m.cadena === chain)
      && (risk === 'TODOS' || c.risk_level === risk)
      && (action === 'TODOS' || c.commercial_action === action);
  });
}

function fillFilterOptions(cases) {
  function fill(id, values) {
    const sel = document.getElementById(id);
    const current = sel.value || 'TODOS';
    sel.innerHTML = '<option value="TODOS">Todas</option>' + [...new Set(values)].sort().map(v => `<option>${v}</option>`).join('');
    if ([...sel.options].some(o => o.value === current)) sel.value = current;
  }
  fill('filterRegion', cases.map(c => metaFor(c).region));
  fill('filterChannel', cases.map(c => metaFor(c).canal));
  fill('filterChain', cases.map(c => metaFor(c).cadena));
}

function groupSum(cases, keyFn, valueFn = () => 1) {
  const out = {};
  for (const c of cases) out[keyFn(c)] = (out[keyFn(c)] || 0) + valueFn(c);
  return out;
}
function barChart(group, valueLabel='casos') {
  const entries = Object.entries(group);
  const max = Math.max(1, ...entries.map(([,v]) => Number(v)));
  if (!entries.length) return '<p class="small">Sin datos para el filtro seleccionado.</p>';
  return entries.map(([k,v]) => `<div class="bar-row"><div>${k}</div><div class="bar-bg"><div class="bar-fill" style="width:${Math.max(4, pct(v,max))}%"></div></div><div><b>${money(v)}</b> ${valueLabel}</div></div>`).join('');
}
function riskChart(cases) {
  const g = { ALTO:0, MEDIO:0, BAJO:0 };
  cases.forEach(c => g[c.risk_level]++);
  return Object.entries(g).map(([k,v]) => `<div class="bar-row"><div class="risk-${k}">${k}</div><div class="bar-bg"><div class="bar-fill ${k==='ALTO'?'danger':k==='MEDIO'?'warn':'ok'}" style="width:${Math.max(4, pct(v, Math.max(...Object.values(g),1)))}%"></div></div><div><b>${v}</b> casos</div></div>`).join('');
}
function channelDonut(cases) {
  const g = groupSum(cases, c => metaFor(c).canal);
  const total = Object.values(g).reduce((a,b) => a+b, 0);
  const entries = Object.entries(g);
  if (!entries.length) return '<p class="small">Sin datos para el filtro seleccionado.</p>';
  return `<div class="donut-wrap"><div class="donut"></div><div class="legend">${entries.map(([k,v],i) => `<div><span style="background:${['#175cd3','#12b76a','#f79009','#6941c6'][i%4]}"></span>${k}: <b>${v}</b> casos (${pct(v,total)}%)</div>`).join('')}</div></div>`;
}

async function refreshDashboard() {
  const casesData = await api('/cases');
  const allCases = casesData.cases;
  fillFilterOptions(allCases);
  const cases = filteredCases(allCases);
  const total = cases.length;
  const validated = cases.filter(c => c.validated_by).length;
  const pendingSupervisor = cases.filter(c => !c.validated_by).length;
  const high = cases.filter(c => c.risk_level === 'ALTO').length;
  const med = cases.filter(c => c.risk_level === 'MEDIO').length;
  const low = cases.filter(c => c.risk_level === 'BAJO').length;
  const valueRisk = cases.reduce((a,c) => a + Number(c.financial_value_at_risk || 0), 0);
  const qty = cases.reduce((a,c) => a + Number(c.quantity || 0), 0);
  const changes = cases.filter(c => c.price_audit.has_price_change).length;
  const unapproved = cases.filter(c => c.price_audit.has_price_change && !c.price_audit.price_change_approved).length;
  const intervened = cases.reduce((a,c) => a + Number(c.intervened_value || 0), 0);
  const avgDiscount = changes ? cases.filter(c => c.price_audit.has_price_change).reduce((a,c) => a + Number(c.price_audit.discount_percent || 0), 0) / changes : 0;
  const metrics = [
    ['Casos filtrados', total], ['Validados supervisor', validated], ['Pendientes supervisor', pendingSupervisor],
    ['Riesgo alto', high], ['Riesgo medio', med], ['Riesgo bajo', low],
    ['Valor financiero riesgo', money(valueRisk)], ['Cantidad intervenida', qty], ['Cambios de precio', changes],
    ['Cambios sin aprobación', unapproved], ['Valor intervenido', money(intervened)], ['Descuento promedio %', money(avgDiscount)]
  ];
  document.getElementById('metricsGrid').innerHTML = metrics.map(m => `<div class="metric span-3"><div class="value">${m[1]}</div><div class="label">${m[0]}</div></div>`).join('');
  document.getElementById('riskChart').innerHTML = riskChart(cases);
  document.getElementById('regionChart').innerHTML = barChart(groupSum(cases, c => metaFor(c).region, c => c.financial_value_at_risk), 'Bs');
  document.getElementById('actionChart').innerHTML = barChart(groupSum(cases, c => c.commercial_action), 'casos');
  document.getElementById('channelChart').innerHTML = channelDonut(cases);
  const regionRows = Object.entries(groupSum(cases, c => metaFor(c).region, c => c.financial_value_at_risk)).sort((a,b) => b[1]-a[1]);
  document.getElementById('regionTable').innerHTML = '<table><tr><th>Región</th><th>Valor en riesgo</th><th>Casos</th></tr>' + regionRows.map(([r,v]) => `<tr><td>${r}</td><td>${money(v)}</td><td>${cases.filter(c => metaFor(c).region===r).length}</td></tr>`).join('') + '</table>';
  const topRegion = regionRows[0]?.[0] || 'sin datos';
  document.getElementById('insightsBox').innerHTML = `
    <div class="insight"><b>Prioridad gerencial:</b> ${high} caso(s) en riesgo alto y ${unapproved} cambio(s) de precio sin aprobación.</div>
    <div class="insight"><b>Región con mayor exposición:</b> ${topRegion}.</div>
    <div class="insight"><b>Impacto financiero filtrado:</b> ${money(valueRisk)} Bs en riesgo y ${money(intervened)} Bs intervenidos por precio.</div>
    <div class="insight"><b>Lectura ejecutiva:</b> si el filtro muestra muchos pendientes supervisor o cambios sin aprobación, gerencia debe priorizar validación y control comercial.</div>`;

  const contenedor = document.getElementById('casesDetailTable');
  contenedor.replaceChildren();
  if (!cases.length) {
    contenedor.textContent = 'No existen casos con estos filtros.';
  } else {
    const tabla = document.createElement('table');
    const encabezado = document.createElement('tr');

    ['Producto','Sala','Regi?n','Riesgo','Estado','Valor en riesgo','Consulta']
      .forEach(t => {
        const th = document.createElement('th');
        th.textContent = t;
        encabezado.appendChild(th);
      });
    tabla.appendChild(encabezado);

    cases.forEach(c => {
      const fila = document.createElement('tr');

      [
        c.product_name,
        c.store,
        metaFor(c).region,
        c.risk_level,
        c.status,
        money(c.financial_value_at_risk)
      ].forEach(v => {
        const td = document.createElement('td');
        td.textContent = String(v ?? '');
        fila.appendChild(td);
      });

      const celda = document.createElement('td');
      const boton = document.createElement('button');
      boton.type = 'button';
      boton.textContent = 'Ver detalle';

      boton.addEventListener('click', () => {
        const detalle = {
          id: c.id,
          producto: c.product_name,
          lote: c.batch,
          sala: c.store,
          departamento: metaFor(c).region,
          cadena: metaFor(c).cadena,
          vencimiento: c.expiration_date,
          cantidad: c.quantity,
          precio_actual: c.current_price,
          precio_nuevo: c.new_price,
          riesgo: c.risk_level,
          valor_en_riesgo: c.financial_value_at_risk,
          estado: c.status,
          validado_por: c.validated_by || 'Pendiente',
          accion: c.commercial_action,
          auditoria_precio: c.price_audit
        };
        document.getElementById('caseDetailJson').textContent =
          JSON.stringify(detalle, null, 2);
      });

      celda.appendChild(boton);
      fila.appendChild(celda);
      tabla.appendChild(fila);
    });

    contenedor.appendChild(tabla);
  }

  const dashboardTech = await api('/dashboard');
  document.getElementById('dashboardJson').textContent = JSON.stringify({ filtros_aplicados: getFilters(), analytics_visual: { total, validated, pendingSupervisor, high, med, low, valueRisk, qty, changes, unapproved, intervened, avgDiscount }, dashboard_api: dashboardTech }, null, 2);
}
function getFilters() { return { vista: document.getElementById('filterScope').value, region: document.getElementById('filterRegion').value, canal: document.getElementById('filterChannel').value, cadena: document.getElementById('filterChain').value, riesgo: document.getElementById('filterRisk').value, accion: document.getElementById('filterAction').value }; }

async function refreshEvents() {
  const events = await api('/events');
  document.getElementById('eventsTable').innerHTML = events.events.length ? '<table><tr><th>Evento</th><th>Aggregate</th><th>Payload</th></tr>' + events.events.map(e => `<tr><td>${e.name}</td><td>${e.aggregate_id}</td><td><code>${JSON.stringify(e.payload)}</code></td></tr>`).join('') + '</table>' : '<p class="small">Sin eventos todavía.</p>';
  const trace = await api('/traceability');
  document.getElementById('traceabilityJson').textContent = JSON.stringify(trace, null, 2);
}
async function refreshAll() { try { await Promise.all([refreshCases(), refreshDashboard(), refreshEvents()]); } catch (e) { console.error(e); } }

async function registerPayload(payload) {
  const result = await api('/cases', { method: 'POST', body: JSON.stringify(payload) });
  selectedCaseId = result.case.id;
  return result.case;
}


document.getElementById('evidencePhoto').addEventListener('change', (ev) => {
  const file = ev.target.files && ev.target.files[0];
  if (!file) {
    evidencePhotoData = '';
    evidencePhotoName = '';
    document.getElementById('evidencePreviewImg').style.display = 'none';
    document.getElementById('evidencePreviewTitle').textContent = 'Sin foto adjunta todavía';
    return;
  }
  evidencePhotoName = file.name;
  const reader = new FileReader();
  reader.onload = () => {
    evidencePhotoData = String(reader.result || '');
    const img = document.getElementById('evidencePreviewImg');
    img.src = evidencePhotoData;
    img.style.display = 'block';
    document.getElementById('evidencePreviewTitle').textContent = 'Foto adjunta: ' + evidencePhotoName;
  };
  reader.readAsDataURL(file);
});

function formPayload(ev) {
  const form = new FormData(ev.target);
  const payload = Object.fromEntries(form.entries());
  payload.quantity = Number(payload.quantity);
  payload.current_price = Number(payload.current_price);
  payload.new_price = payload.new_price ? Number(payload.new_price) : null;
  payload.price_change_approved = payload.price_change_approved === 'true';
  delete payload.evidence_photo_file;
  payload.evidence_photo_name = evidencePhotoName;
  payload.evidence_photo_data = evidencePhotoData;
  return payload;
}

document.getElementById('caseForm').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  try {
    const c = await registerPayload(formPayload(ev));
    setStatus('registerStatus', 'Caso registrado correctamente. ID: ' + selectedCaseId, 'ok');
    document.getElementById('lastCaseSummary').innerHTML = caseCard(c) + evidencePhotoHtml(c) + `<h3>Variables usadas para clasificar riesgo</h3>${riskExplanation(c)}<pre>${JSON.stringify({ meta: metaFor(c), case: c }, null, 2)}</pre>`;
    await refreshAll();
  } catch (e) { setStatus('registerStatus', 'Error: ' + e.message, 'warn'); }
});

document.getElementById('validateForm').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  if (!selectedCaseId) { setStatus('validationStatus', 'Primero seleccione un caso.', 'warn'); return; }
  const payload = Object.fromEntries(new FormData(ev.target).entries());
  try {
    const result = await api(`/cases/${selectedCaseId}/validate`, { method: 'PATCH', body: JSON.stringify(payload) });
    setStatus('validationStatus', 'Caso validado: ' + result.case.status + ' por ' + result.case.validated_by, 'ok');
    document.getElementById('selectedCase').innerHTML = selectedCaseView(result.case);
    await refreshAll();
  } catch (e) { setStatus('validationStatus', 'Error: ' + e.message, 'warn'); }
});

async function resetDemo() {
  await api('/cases/reset', { method: 'DELETE' });
  selectedCaseId = null;
  setStatus('homeStatus', 'Demo reiniciada. Ahora puede registrar casos desde cero.', 'ok');
  document.getElementById('lastCaseSummary').innerHTML = '<p class="small">Demo reiniciada.</p>';
  document.getElementById('selectedCase').innerHTML = 'Seleccione un caso de la lista.';
  await refreshAll();
}
document.getElementById('resetBtn').addEventListener('click', resetDemo);

function oneExamplePayload() {
  return { store: '210937 - HIPERMAXI SUR S.A.', product_name: '0000093000-ACEITE DE OLIVA EXTRA VIRGEN 6X1L', batch: 'DEMO-ACEITE-001', expiration_date: addDays(26), quantity: 12, current_price: 150, new_price: 120, commercial_action: 'DESCUENTO', price_change_approved: true, price_change_reason: 'Descuento autorizado por supervisor', evidence_note: 'Foto clara de góndola y etiqueta de precio', created_by: 'mercaderista.demo', evidence_photo_name: 'evidencia_gondola_aceite_demo.svg', evidence_photo_data: "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='520' height='340' viewBox='0 0 520 340'%3E%3Crect width='520' height='340' fill='%23f8fafc'/%3E%3Crect x='35' y='60' width='450' height='190' rx='18' fill='%23e0f2fe' stroke='%23175cd3' stroke-width='4'/%3E%3Ctext x='55' y='105' font-family='Arial' font-size='28' font-weight='700' fill='%230b2f66'%3E0000093000-ACEITE DE OLIVA EXTRA VIRGEN 6X1L%3C/text%3E%3Ctext x='55' y='150' font-family='Arial' font-size='22' fill='%230b2f66'%3ELote DEMO-ACEITE-001 · Fecha simulada%3C/text%3E%3Ctext x='55' y='195' font-family='Arial' font-size='24' fill='%23b42318'%3EPrecio antes Bs 150.00 → ahora Bs 120.00%3C/text%3E%3Ctext x='55' y='238' font-family='Arial' font-size='20' fill='%23047857'%3EEvidencia de góndola y etiqueta registrada%3C/text%3E%3Crect x='55' y='270' width='410' height='35' rx='8' fill='%23175cd3'/%3E%3Ctext x='75' y='294' font-family='Arial' font-size='18' font-weight='700' fill='white'%3EFoto demo para validación del supervisor%3C/text%3E%3C/svg%3E" };
}
async function seedOne() {
  const c = await registerPayload(oneExamplePayload());
  setStatus('homeStatus', 'Caso ejemplo cargado correctamente. ID: ' + selectedCaseId, 'ok');
  await selectCase(c.id);
  await refreshAll();
}
document.getElementById('seedBtn').addEventListener('click', seedOne);

const portfolio = [
  oneExamplePayload(),
  ...[
  {
    "store": "128329 - HIPERMAXI ACHUMANI",
    "product_name": "0000210587-ESPONJA GLITZI X3",
    "batch": "DEMO-CARTERA-002",
    "quantity": 15,
    "current_price": 35,
    "new_price": 30,
    "commercial_action": "DESCUENTO",
    "price_change_approved": true,
    "price_change_reason": "Escenario simulado para Demo 2",
    "evidence_note": "Caso simulado; sin fotograf?a real adjunta",
    "created_by": "mercaderista.demo",
    "expiration_date": addDays(8)
  },
  {
    "store": "305717 - SPM.IC NORTE S.A.-AMERICA",
    "product_name": "0000051432-PRUDENTIAL COMFORT TOTAL M 4x20",
    "batch": "DEMO-CARTERA-003",
    "quantity": 24,
    "current_price": 28,
    "new_price": 25,
    "commercial_action": "DESCUENTO",
    "price_change_approved": true,
    "price_change_reason": "Escenario simulado para Demo 2",
    "evidence_note": "Caso simulado; sin fotograf?a real adjunta",
    "created_by": "mercaderista.demo",
    "expiration_date": addDays(20)
  },
  {
    "store": "233802 - HIPERMAXI EQUIPETROL",
    "product_name": "0000051433-PRUDENTIAL COMFORT TOTAL G 4x20",
    "batch": "DEMO-CARTERA-004",
    "quantity": 18,
    "current_price": 45,
    "new_price": 40,
    "commercial_action": "DESCUENTO",
    "price_change_approved": true,
    "price_change_reason": "Escenario simulado para Demo 2",
    "evidence_note": "Caso simulado; sin fotograf?a real adjunta",
    "created_by": "mercaderista.demo",
    "expiration_date": addDays(45)
  },
  {
    "store": "302166 - SPM.IC NORTE S.A.-HIPODROMO",
    "product_name": "0000050656-PROTECTOR CAMA PRUDENTIAL 8X10",
    "batch": "DEMO-CARTERA-005",
    "quantity": 30,
    "current_price": 60,
    "new_price": 52,
    "commercial_action": "DESCUENTO",
    "price_change_approved": true,
    "price_change_reason": "Escenario simulado para Demo 2",
    "evidence_note": "Caso simulado; sin fotograf?a real adjunta",
    "created_by": "mercaderista.demo",
    "expiration_date": addDays(12)
  },
  {
    "store": "210937 - HIPERMAXI SUR S.A.",
    "product_name": "0000051431-PROTECTOR DE CAMA PRUDENTIAL F6X20",
    "batch": "DEMO-CARTERA-006",
    "quantity": 12,
    "current_price": 75,
    "new_price": 65,
    "commercial_action": "DESCUENTO",
    "price_change_approved": true,
    "price_change_reason": "Escenario simulado para Demo 2",
    "evidence_note": "Caso simulado; sin fotograf?a real adjunta",
    "created_by": "mercaderista.demo",
    "expiration_date": addDays(60)
  }
]
];
async function seedPortfolio() {
  const existentes = (await api('/cases')).cases;
  let agregados = 0;
  for (const p of portfolio) {
    if (existentes.some(c => c.batch === p.batch)) continue;
    await registerPayload(p);
    agregados++;
  }
  setStatus('homeStatus', `Cartera demo: ${agregados} casos nuevos. Se conservaron los anteriores.`, 'ok');
  await refreshAll();
}
document.getElementById('portfolioBtn').addEventListener('click', seedPortfolio);
document.getElementById('portfolioBtnDashboard').addEventListener('click', seedPortfolio);

for (const id of ['filterScope','filterRegion','filterChannel','filterChain','filterRisk','filterAction']) document.getElementById(id).addEventListener('change', refreshDashboard);

refreshAll();
</script>
</body>
</html>
"""
