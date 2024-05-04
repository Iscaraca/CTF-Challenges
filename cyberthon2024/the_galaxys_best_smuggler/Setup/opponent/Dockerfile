FROM python:3.11.4-slim as python-base

COPY . /app/
WORKDIR /app

RUN pip install requests

CMD ["python3", "main.py"]