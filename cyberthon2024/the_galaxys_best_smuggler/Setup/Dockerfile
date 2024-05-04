FROM docker:dind

COPY . /app/
WORKDIR /app

RUN chmod +x run-compose.sh

RUN apk add --no-cache python3 py3-pip
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip3 install flask
RUN pip3 install gunicorn
RUN pip3 install gunicorn[gevent]

#CMD ["./run-compose.sh", "instance", "8000", "8010"]

CMD ["gunicorn", "-k", "gevent", "--bind", "0.0.0.0:80", "app:app"]