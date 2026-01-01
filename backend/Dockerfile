# backend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir debugpy # For debugging

# Copy app code (both app/ and classes/)
COPY app/ ./app
# COPY classes/ ./classes

# Make classes importable
ENV PYTHONPATH=/app

# Expose FastAPI ports
EXPOSE 8000 5678