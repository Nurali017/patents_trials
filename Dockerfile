FROM python:3.9

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Python зависимостей
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Копирование проекта
COPY . /usr/src/app/

# Создание символической ссылки на utils из patents-backend
# Это будет сделано через volume в docker-compose

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
