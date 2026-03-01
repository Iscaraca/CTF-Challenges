FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN mv flag.txt /flag.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]