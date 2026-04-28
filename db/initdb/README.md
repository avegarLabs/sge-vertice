# `db/initdb` — dumps SQL para inicialización de PostgreSQL

Coloca aquí el archivo de respaldo (`*.sql` o `*.sql.gz`) que el
contenedor `db` debe ejecutar **automáticamente en su primer arranque**.

## Convenciones del contenedor `postgres`

- Solo se ejecutan los archivos cuando el volumen `pgdata` está **vacío**
  (instalación limpia). Si el volumen ya tiene datos, los dumps se
  ignoran.
- Se procesan en **orden alfabético** los archivos con extensiones:
  - `*.sql`
  - `*.sql.gz`
  - `*.sql.xz`
  - `*.sh`
- Los `*.sh` se ejecutan como root y reciben `PGUSER` / `PGDATABASE`
  vía variables de entorno.

## Disposición recomendada

```
db/initdb/
├── 01-schema.sql       # Esquema (CREATE DATABASE / TABLE / etc.)
└── 02-data.sql         # Datos
```

O bien un único dump completo (lo más común con `pg_dump`):

```
db/initdb/
└── 00-rechum-dump.sql
```

> **Importante**: el dump debe ser compatible con la versión de PostgreSQL
> definida en `POSTGRES_VERSION` (ver `.env`). Si el dump fue generado con
> `pg_dump` desde una versión 13, ajusta `POSTGRES_VERSION=13` antes del
> primer arranque, o vuelve a generar el dump con la versión destino.

## Recargar el dump tras cambios

Recordá: los dumps solo se ejecutan si el volumen `pgdata` está vacío.
Para forzar una recarga:

```bash
docker compose down -v          # ¡BORRA TODOS los datos persistentes!
docker compose up -d
```

## ¿Versionar los dumps?

**No recomendable** si el dump:

- Pesa más de unos pocos MB (Git no es óptimo para binarios grandes;
  considera Git LFS o una ubicación externa).
- Contiene datos personales / sensibles (PII).

Por defecto este repo **ignora** los archivos `*.sql*` dentro de
`db/initdb/` (ver `.gitignore`). Si quieres versionar un dump pequeño y
no sensible, agrégalo explícitamente con `git add -f`.
