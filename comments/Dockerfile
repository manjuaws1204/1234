# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY main.py .

# Install dependencies
RUN pip install fastapi uvicorn \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp

# Expose service port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
