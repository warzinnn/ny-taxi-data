FROM prefecthq/prefect:2-python3.11

RUN apt update && \
    apt install -y vim

CMD ["prefect", "agent", "start", "-q", "default"]