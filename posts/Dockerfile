FROM python:3.11-slim
WORKDIR /app
COPY main.py .
RUN pip install fastapi uvicorn opentelemetry-sdk opentelemetry-exporter-otlp
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
