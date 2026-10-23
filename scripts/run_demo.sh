#!/usr/bin/env bash
set -euo pipefail
uvicorn app_deteccion.main:app --reload
