# Используем официальный образ Python 3.10 на основе Slim
FROM python:3.10-slim

# Установка переменной окружения для отключения буферизации вывода Python (полезно для логов)
ENV PYTHONUNBUFFERED 1

# Установка системных зависимостей для PostgreSQL и компиляции
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование requirements.txt в контейнер
COPY requirements.txt /app/requirements.txt

# Установка зависимостей из requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Установим gunicorn, если он не указан в requirements.txt
RUN pip install --no-cache-dir gunicorn

# Копирование проекта в контейнер
COPY ./src /app

# Сбор статических файлов (если нужно для проекта)
RUN python manage.py collectstatic --noinput

# Экспорт порта для сервера
EXPOSE 8000

# Команда для запуска приложения через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "website.wsgi:application"]
