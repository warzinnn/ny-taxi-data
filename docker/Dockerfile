FROM prefecthq/prefect:2-python3.11

COPY docker-requirements.txt .
COPY prefect_block_builder.py .

RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

ENTRYPOINT ["prefect", "server", "start"]