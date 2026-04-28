#!/usr/bin/env bash
# =====================================================================
# entrypoint.sh — sge-vertice
#
# Ejecuta los pasos previos al arranque de la app:
#   1. Espera a que PostgreSQL acepte conexiones.
#   2. Ejecuta `collectstatic` para servir estáticos vía nginx.
#   3. Lanza el comando recibido (por defecto: gunicorn).
#
# IMPORTANTE: este script NO ejecuta `manage.py migrate`.
# La base de datos se aprovisiona desde un dump SQL cargado por el
# contenedor de PostgreSQL al inicializarse (docker-entrypoint-initdb.d/).
# =====================================================================

set -euo pipefail

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
WAIT_TIMEOUT="${DB_WAIT_TIMEOUT:-60}"

echo "[entrypoint] Esperando a PostgreSQL en ${DB_HOST}:${DB_PORT} (timeout ${WAIT_TIMEOUT}s)..."

python - <<'PY'
import os, sys, time
import psycopg2

host    = os.environ.get("DB_HOST", "db")
port    = int(os.environ.get("DB_PORT", "5432"))
user    = os.environ["DB_USER"]
pwd     = os.environ["DB_PASSWORD"]
dbname  = os.environ["DB_NAME"]
timeout = int(os.environ.get("DB_WAIT_TIMEOUT", "60"))

deadline = time.time() + timeout
last_err = None
while time.time() < deadline:
    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=pwd,
            dbname=dbname, connect_timeout=3,
        )
        conn.close()
        print("[entrypoint] PostgreSQL listo.")
        sys.exit(0)
    except psycopg2.OperationalError as e:
        last_err = e
        print(f"[entrypoint] BD aún no disponible: {e}", flush=True)
        time.sleep(2)

print(f"[entrypoint] Timeout esperando a la BD: {last_err}", file=sys.stderr)
sys.exit(1)
PY

# Migraciones intencionalmente OMITIDAS — la BD se carga desde un dump SQL.
echo "[entrypoint] Migraciones omitidas (BD precargada desde dump SQL)."

echo "[entrypoint] Recolectando estáticos..."
python manage.py collectstatic --noinput --verbosity 1

echo "[entrypoint] Lanzando: $*"
exec "$@"
