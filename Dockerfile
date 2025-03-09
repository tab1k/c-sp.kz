# Используем официальный образ Python
FROM python:3.10

# Отключаем кеширование bytecode и включаем немедленный вывод
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создаём рабочую директорию
WORKDIR /app  

# Обновляем `apt` и устанавливаем PostgreSQL-клиент
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY src /app

# Копируем и даём права на выполнение `docker-entrypoint.sh`
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Определяем точку входа
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Открываем порт для приложения
EXPOSE 8000
