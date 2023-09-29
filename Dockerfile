FROM python:3.11.4-slim
WORKDIR /lenta_app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY backend/ .
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]
