FROM python:3.10.12

# Update Python3
RUN python3 -m pip install --upgrade pip && python3 -m pip install --upgrade setuptools && python3 -m pip install --upgrade wheel

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Install foundry and huff
RUN curl -L https://foundry.paradigm.xyz | bash \
    && bash -c "source /root/.bashrc && foundryup" \
    && chmod 755 -R /root
RUN curl -L get.huff.sh | bash \
    && bash -c "source /root/.bashrc && huffup" \
    && chmod 755 -R /root
RUN apt-get -y update && apt-get -y upgrade \
    && apt-get install -y npm \
    && apt-get install -y yarn \
    && apt-get install -y bsdmainutils

ENV PATH="$PATH:/root/.foundry/bin"
ENV PATH="$PATH:/root/.huff/bin"


COPY ./contracts /contracts
COPY ./app /app

WORKDIR /app
ENTRYPOINT ["/bin/bash", "/app/deploy.sh"]
# ENTRYPOINT ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:5000"]