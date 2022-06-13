FROM python:3.10-slim-bullseye

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
