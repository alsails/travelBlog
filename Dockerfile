FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN apt-get update && apt-get install -y default-mysql-client
RUN pip install -r requirements.txt

# Копируем только необходимые файлы в контейнер
COPY .. .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "localhost:8000"]
