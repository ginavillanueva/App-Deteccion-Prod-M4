#!/usr/bin/env bash
set -euo pipefail
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
