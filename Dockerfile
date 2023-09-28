FROM python:3.11-slim
WORKDIR /lenta_app
COPY ./requirements.txt .
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY backend/ .
CMD ["gunicorn", "backend.asgi.application", "--bind", "0:8000" ]
