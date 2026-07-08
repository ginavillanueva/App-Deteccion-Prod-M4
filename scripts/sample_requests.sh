#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE:-http://127.0.0.1:8000}"

curl -s "$BASE/health" | python -m json.tool

curl -s -X POST "$BASE/cases"   -H "Content-Type: application/json"   -d '{
    "store": "Hipermaxi Sur",
    "product_name": "Yogurt Natural 1L",
    "batch": "L-2026-07",
    "expiration_date": "2026-07-20",
    "quantity": 25,
    "current_price": 18.5,
    "new_price": 14.5,
    "commercial_action": "DESCUENTO",
    "price_change_approved": true,
    "price_change_reason": "Descuento autorizado por supervisor",
    "evidence_note": "Foto clara de gondola y etiqueta de precio",
    "created_by": "mercaderista.demo"
  }' | python -m json.tool

curl -s "$BASE/dashboard" | python -m json.tool
curl -s "$BASE/traceability" | python -m json.tool
