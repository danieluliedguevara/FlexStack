FROM python:3.9-slim

WORKDIR /app

COPY app.py .

COPY /home/dulied/Codeco/FlexStack/metrics .

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir v2xflexstack

ENTRYPOINT ["python", "app.py"]
CMD ["--station-id", "1"]
