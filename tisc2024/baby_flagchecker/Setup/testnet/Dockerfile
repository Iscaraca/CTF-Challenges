FROM python:3.10.12

# Update Python3
RUN python3 -m pip install --upgrade pip && python3 -m pip install --upgrade setuptools && python3 -m pip install --upgrade wheel

# Install foundry
RUN curl -L https://foundry.paradigm.xyz | bash \
    && bash -c "source /root/.bashrc && foundryup" \
    && chmod 755 -R /root

ENTRYPOINT ["/root/.foundry/bin/anvil", "--host", "0.0.0.0"]
