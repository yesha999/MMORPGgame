FROM python:3.10-slim-bullseye

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY data .
COPY templates .
COPY app.py .
COPY base.py .
COPY classes.py .
COPY equipment.py .
COPY requirements.txt .
COPY skills.py .
COPY unit.py .
COPY wsgi.py .
COPY infra .
COPY .gitignore .
