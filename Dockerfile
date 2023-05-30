FROM python:3.9-slim

RUN mkdir -p /app
WORKDIR /app

# Установка зависимостей
RUN pip install selenium

# Копирование исходного кода
COPY . /app
RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
