FROM python:3.9-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/astockalypse_app
WORKDIR /app/astockalypse_app

EXPOSE 5000
CMD ["python", "main.py"]
