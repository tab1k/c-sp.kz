#!/bin/bash
set -e

echo "Ожидание PostgreSQL..."
until pg_isready -h postgres -p 5432; do
  sleep 1
done

echo "PostgreSQL доступен, выполняем миграции..."
python src/manage.py migrate
python src/manage.py collectstatic --noinput

echo "Запускаем Gunicorn-сервер..."
exec gunicorn src.website.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --threads 2 \
  --timeout 120
