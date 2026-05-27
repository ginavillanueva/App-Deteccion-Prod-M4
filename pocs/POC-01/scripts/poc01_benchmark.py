#!/usr/bin/env python3
"""
POC-01 App Detección Prod — versión defensa final / nivel doctorado
Valida registro transaccional de producto próximo a vencer + cambio de precio + actualización inmediata de dashboard + Outbox.
Ejecutar: python scripts/poc01_benchmark.py
"""
from pathlib import Path
import sqlite3, time, random, statistics, csv, json

BASE = Path(__file__).resolve().parents[1]
EVID = BASE / "evidencia"
EVID.mkdir(exist_ok=True)
DB = EVID / "poc01_app_deteccion_prod.sqlite"
N = 1000
random.seed(42)

if DB.exists():
    DB.unlink()

conn = sqlite3.connect(DB)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA synchronous=NORMAL;")
conn.executescript("""
CREATE TABLE product_case (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sku TEXT NOT NULL,
  store_id TEXT NOT NULL,
  lot_code TEXT NOT NULL,
  expiration_days INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  previous_price REAL NOT NULL,
  new_price REAL NOT NULL,
  price_delta_pct REAL NOT NULL,
  status TEXT NOT NULL,
  risk_level TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE dashboard_operational_snapshot (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  open_cases INTEGER NOT NULL,
  critical_cases INTEGER NOT NULL,
  units_at_risk INTEGER NOT NULL,
  financial_value_at_risk REAL NOT NULL,
  price_changed_cases INTEGER NOT NULL,
  total_price_delta_value REAL NOT NULL,
  last_updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE outbox_event (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  aggregate_type TEXT NOT NULL,
  aggregate_id INTEGER NOT NULL,
  event_type TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL DEFAULT 'PENDING',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO dashboard_operational_snapshot
(id, open_cases, critical_cases, units_at_risk, financial_value_at_risk, price_changed_cases, total_price_delta_value)
VALUES (1,0,0,0,0.0,0,0.0);
""")
conn.commit()

latencies_ms = []
errors = 0
start = time.perf_counter()

for i in range(N):
    sku = f"SKU-{random.randint(1000,9999)}"
    store_id = f"SALA-{random.randint(1,25):02d}"
    lot_code = f"LOT-{random.randint(10000,99999)}"
    expiration_days = random.choice([7, 15, 30, 45, 60, 75, 89])
    quantity = random.randint(1, 80)
    previous_price = round(random.uniform(8, 180), 2)
    discount_pct = random.choice([0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
    new_price = round(previous_price * (1 - discount_pct), 2)
    price_delta_pct = round(((new_price - previous_price) / previous_price) * 100, 2)
    risk = "CRITICO" if expiration_days <= 30 else "MEDIO" if expiration_days <= 60 else "BAJO"
    status = "REGISTRADO"
    t0 = time.perf_counter()
    try:
        with conn:
            cur = conn.execute("""
                INSERT INTO product_case
                (sku, store_id, lot_code, expiration_days, quantity, previous_price, new_price, price_delta_pct, status, risk_level)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (sku, store_id, lot_code, expiration_days, quantity, previous_price, new_price, price_delta_pct, status, risk))
            case_id = cur.lastrowid
            financial_value = quantity * previous_price
            delta_value = quantity * (previous_price - new_price)
            conn.execute("""
                UPDATE dashboard_operational_snapshot
                SET open_cases = open_cases + 1,
                    critical_cases = critical_cases + ?,
                    units_at_risk = units_at_risk + ?,
                    financial_value_at_risk = financial_value_at_risk + ?,
                    price_changed_cases = price_changed_cases + 1,
                    total_price_delta_value = total_price_delta_value + ?,
                    last_updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (1 if risk == "CRITICO" else 0, quantity, financial_value, delta_value))
            payload = {
                "caseId": case_id,
                "sku": sku,
                "storeId": store_id,
                "previousPrice": previous_price,
                "newPrice": new_price,
                "priceDeltaPct": price_delta_pct,
                "quantity": quantity,
                "riskLevel": risk
            }
            conn.execute("""
                INSERT INTO outbox_event
                (aggregate_type, aggregate_id, event_type, payload_json, idempotency_key)
                VALUES (?,?,?,?,?)
            """, ("ProductCase", case_id, "ProductNearExpiryRegistered.v1", json.dumps(payload, ensure_ascii=False), f"ProductCase:{case_id}:registered:v1"))
            conn.execute("""
                INSERT INTO outbox_event
                (aggregate_type, aggregate_id, event_type, payload_json, idempotency_key)
                VALUES (?,?,?,?,?)
            """, ("ProductCase", case_id, "PriceChanged.v1", json.dumps(payload, ensure_ascii=False), f"ProductCase:{case_id}:price_changed:v1"))
    except Exception:
        errors += 1
    finally:
        latencies_ms.append((time.perf_counter() - t0) * 1000)

elapsed = time.perf_counter() - start

def percentile(values, pct):
    values = sorted(values)
    k = (len(values)-1) * (pct/100)
    f = int(k)
    c = min(f+1, len(values)-1)
    if f == c:
        return values[int(k)]
    return values[f] * (c-k) + values[c] * (k-f)

row = conn.execute("SELECT * FROM dashboard_operational_snapshot WHERE id=1").fetchone()
case_count = conn.execute("SELECT COUNT(*) FROM product_case").fetchone()[0]
outbox_count = conn.execute("SELECT COUNT(*) FROM outbox_event").fetchone()[0]
price_events = conn.execute("SELECT COUNT(*) FROM outbox_event WHERE event_type='PriceChanged.v1'").fetchone()[0]

metrics = {
    "poc_id": "POC-01",
    "records_attempted": N,
    "records_inserted": case_count,
    "errors": errors,
    "throughput_records_per_second": round(N/elapsed, 2),
    "latency_avg_ms": round(statistics.mean(latencies_ms), 3),
    "latency_p50_ms": round(percentile(latencies_ms, 50), 3),
    "latency_p95_ms": round(percentile(latencies_ms, 95), 3),
    "latency_p99_ms": round(percentile(latencies_ms, 99), 3),
    "outbox_events_total": outbox_count,
    "price_changed_events_total": price_events,
    "dashboard_open_cases": row[1],
    "dashboard_critical_cases": row[2],
    "dashboard_units_at_risk": row[3],
    "dashboard_financial_value_at_risk": round(row[4], 2),
    "dashboard_price_changed_cases": row[5],
    "dashboard_total_price_delta_value": round(row[6], 2),
    "dashboard_consistency_ok": bool(row[1] == case_count and row[5] == price_events == case_count),
    "db_path": str(DB)
}

(EVID / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
with (EVID / "latencies.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["operation", "latency_ms"])
    for idx, latency in enumerate(latencies_ms, 1):
        writer.writerow([idx, round(latency, 4)])

with (EVID / "dashboard_snapshot.json").open("w", encoding="utf-8") as f:
    json.dump({
        "open_cases": row[1],
        "critical_cases": row[2],
        "units_at_risk": row[3],
        "financial_value_at_risk": round(row[4], 2),
        "price_changed_cases": row[5],
        "total_price_delta_value": round(row[6], 2),
        "last_updated_at": row[7]
    }, f, indent=2, ensure_ascii=False)

print(json.dumps(metrics, indent=2, ensure_ascii=False))
