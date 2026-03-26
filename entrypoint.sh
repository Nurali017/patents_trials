#!/bin/sh
set -e

echo "Waiting for PostgreSQL at ${SQL_HOST}:${SQL_PORT}..."
while ! nc -z "$SQL_HOST" "$SQL_PORT" 2>/dev/null; do
  sleep 1
done
echo "PostgreSQL is available"

echo "Using media backend: ${MEDIA_BACKEND:-filesystem}"
if [ "${MEDIA_BACKEND:-filesystem}" = "filesystem" ]; then
  echo "Checking media directory permissions..."
  mkdir -p /usr/src/app/media/documents
  if [ ! -w /usr/src/app/media ] || [ ! -w /usr/src/app/media/documents ]; then
    echo "ERROR: media directory is not writable for $(id -u):$(id -g)"
    ls -ld /usr/src/app/media /usr/src/app/media/documents 2>/dev/null || true
    exit 1
  fi
else
  : "${MINIO_ENDPOINT:?MINIO_ENDPOINT is required when MEDIA_BACKEND=minio}"
  : "${MINIO_BUCKET:?MINIO_BUCKET is required when MEDIA_BACKEND=minio}"
  : "${MINIO_ACCESS_KEY:?MINIO_ACCESS_KEY is required when MEDIA_BACKEND=minio}"
  : "${MINIO_SECRET_KEY:?MINIO_SECRET_KEY is required when MEDIA_BACKEND=minio}"
  mkdir -p "${LEGACY_MEDIA_ROOT:-/usr/src/app/legacy-media}"
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn on port 8001..."
exec gunicorn trials.wsgi:application \
    --bind 0.0.0.0:8001 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile -
