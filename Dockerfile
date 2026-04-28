# syntax=docker/dockerfile:1.6
# =====================================================================
# sge-vertice — multistage image
#   Stage 1 (builder)  : compila wheels para psycopg2, Pillow, reportlab, etc.
#   Stage 2 (runtime)  : imagen final mínima, sin toolchain de compilación.
# =====================================================================

ARG PYTHON_VERSION=3.7-slim


# ---------- Stage 1: builder ----------------------------------------
FROM python:${PYTHON_VERSION} AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Toolchain + headers para construir psycopg2 (libpq), Pillow (jpeg/zlib)
# y reportlab (freetype).
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        libjpeg-dev \
        zlib1g-dev \
        libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.txt .

# Pre-construye wheels para que el stage final no requiera compiladores.
RUN pip wheel --wheel-dir /wheels -r requirements.txt


# ---------- Stage 2: runtime ----------------------------------------
FROM python:${PYTHON_VERSION} AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=rechum.settings \
    PORT=8000

# Solo librerías de runtime (sin -dev, sin gcc).
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        libjpeg62-turbo \
        zlib1g \
        libfreetype6 \
        fontconfig \
        tini \
    && rm -rf /var/lib/apt/lists/*

# Usuario no-root para ejecutar la app.
RUN groupadd --system app && \
    useradd  --system --gid app --home-dir /app --shell /sbin/nologin app

WORKDIR /app

# Instala desde los wheels prearmados (sin red, sin compiladores).
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links /wheels -r requirements.txt && \
    rm -rf /wheels

# Código fuente al final para maximizar el cache de capas.
COPY --chown=app:app . /app

# Directorios escribibles por el usuario `app` (montados como volúmenes en compose).
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R app:app /app/staticfiles /app/media && \
    chmod +x /app/docker/entrypoint.sh

USER app

EXPOSE 8000

ENTRYPOINT ["/usr/bin/tini", "--", "/app/docker/entrypoint.sh"]

CMD ["gunicorn", "rechum.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
