FROM python:3.9-slim

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir v2xflexstack-monitoring

ENTRYPOINT ["python", "app.py"]
CMD ["--station-id", "1"]
