FROM python:3.11.4-slim as python-base

COPY . /app/
WORKDIR /app

RUN pip install flask==1.1.4
RUN pip install gunicorn==19.9.0
RUN pip install gunicorn[gevent]
RUN pip install --force markupsafe==2.0.1


CMD ["gunicorn", "--keep-alive", "10", "-k", "gevent", "--bind", "0.0.0.0:6767", "-w", "1", "--worker-connections", "50", "server:app"]