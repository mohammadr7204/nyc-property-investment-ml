# NYC Property Investment ML - Web Application Docker Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt web_requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r web_requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY web_app/ ./web_app/
COPY .env.example .env

# Create necessary directories
RUN mkdir -p data logs models/saved_models

# Set environment variables
ENV PYTHONPATH=/app/src
ENV FLASK_ENV=production
ENV DATABASE_PATH=/app/data/nyc_property_data.db

# Initialize database and ML model
RUN python scripts/setup_project.py

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Change to web app directory
WORKDIR /app/web_app

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]