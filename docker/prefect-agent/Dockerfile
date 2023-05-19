FROM prefecthq/prefect:2-python3.11

RUN apt update && \
    apt install -y vim

COPY docker-requirements.txt .

RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

CMD ["prefect", "agent", "start", "-q", "default"]