FROM python:3.12-slim

WORKDIR /app

COPY scripts/ scripts/
COPY *.csv ./

RUN pip install --no-cache-dir pandas

CMD ["python", "scripts/normalize_all.py"]
