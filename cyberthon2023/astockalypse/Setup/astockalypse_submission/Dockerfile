FROM python:3.9-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --default-timeout=900 --no-cache-dir -r requirements.txt

COPY app /app/astockalypse_submission
WORKDIR /app/astockalypse_submission

EXPOSE 5001
CMD ["python", "main.py"]

