FROM python:3.10.12

# Update Python3
RUN python3 -m pip install --upgrade pip && python3 -m pip install --upgrade setuptools && python3 -m pip install --upgrade wheel

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./app /app
WORKDIR /app

# Use gunicorn to run the Flask application
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "main:app"]