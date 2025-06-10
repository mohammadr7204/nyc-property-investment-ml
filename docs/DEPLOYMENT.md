# Deployment Guide

This guide covers different deployment options for the NYC Property Investment ML system.

## 🚀 Deployment Options

### 1. Local Development

For development and testing:

```bash
# Clone repository
git clone https://github.com/mohammadr7204/nyc-property-investment-ml.git
cd nyc-property-investment-ml

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Initialize project
python scripts/setup_project.py

# Test system
python scripts/test_system.py
```

### 2. Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs models/saved_models

# Set environment variables
ENV PYTHONPATH=/app/src
ENV DATABASE_PATH=/app/data/nyc_property_data.db

# Initialize database
RUN python scripts/setup_project.py

# Expose port (if running web interface)
EXPOSE 8000

# Default command
CMD ["python", "scripts/test_system.py"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  nyc-property-ml:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}
      - DATABASE_PATH=/app/data/nyc_property_data.db
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./models:/app/models
    command: python scripts/run_analysis.py -a "123 West 86th Street, New York, NY"
```

Build and run:

```bash
# Build image
docker build -t nyc-property-ml .

# Run with docker-compose
docker-compose up

# Or run directly
docker run -e GOOGLE_MAPS_API_KEY=your_key nyc-property-ml
```

### 3. Cloud Deployment (AWS)

#### AWS Lambda

Create `lambda_handler.py`:

```python
import json
import sys
import os
sys.path.append('/opt/python')
sys.path.append('./src')

from analyzer import NYCPropertyInvestmentAnalyzer

def lambda_handler(event, context):
    try:
        # Get API key from environment
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY', 'demo-api-key')
        
        # Initialize analyzer
        analyzer = NYCPropertyInvestmentAnalyzer(api_key)
        
        # Get address from event
        address = event.get('address')
        if not address:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Address is required'})
            }
        
        # Analyze property
        analysis = analyzer.analyze_property(address)
        
        # Return results
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'address': address,
                'predicted_rent': analysis['revenue_prediction']['predicted_monthly_rent'],
                'gross_yield': analysis['financial_metrics']['gross_rental_yield'],
                'recommendation': analysis['investment_recommendation']['recommendation'],
                'risk_level': analysis['risk_assessment']['overall_risk']
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

Deploy with AWS SAM:

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  NYCPropertyAnalyzer:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: .
      Handler: lambda_handler.lambda_handler
      Runtime: python3.9
      Timeout: 60
      MemorySize: 1024
      Environment:
        Variables:
          GOOGLE_MAPS_API_KEY: !Ref GoogleMapsApiKey
      Events:
        AnalyzeProperty:
          Type: Api
          Properties:
            Path: /analyze
            Method: post

Parameters:
  GoogleMapsApiKey:
    Type: String
    NoEcho: true
```

#### AWS EC2

```bash
# Launch EC2 instance (Ubuntu 20.04)
# SSH into instance

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9
sudo apt install python3.9 python3.9-venv python3.9-dev -y

# Clone repository
git clone https://github.com/mohammadr7204/nyc-property-investment-ml.git
cd nyc-property-investment-ml

# Setup environment
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Setup as service
sudo cp deployment/nyc-property-ml.service /etc/systemd/system/
sudo systemctl enable nyc-property-ml
sudo systemctl start nyc-property-ml
```

### 4. Web Application Deployment

#### Flask Web App

Create `app.py`:

```python
from flask import Flask, request, jsonify, render_template
import sys
sys.path.append('src')

from analyzer import NYCPropertyInvestmentAnalyzer
import os

app = Flask(__name__)
api_key = os.environ.get('GOOGLE_MAPS_API_KEY', 'demo-api-key')
analyzer = NYCPropertyInvestmentAnalyzer(api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_property():
    data = request.get_json()
    address = data.get('address')
    
    if not address:
        return jsonify({'error': 'Address is required'}), 400
    
    try:
        analysis = analyzer.analyze_property(address)
        return jsonify({
            'success': True,
            'analysis': {
                'predicted_rent': analysis['revenue_prediction']['predicted_monthly_rent'],
                'gross_yield': analysis['financial_metrics']['gross_rental_yield'],
                'recommendation': analysis['investment_recommendation']['recommendation'],
                'risk_level': analysis['risk_assessment']['overall_risk'],
                'location_scores': analysis['location_analysis']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

#### Deploy to Heroku

Create `Procfile`:

```
web: gunicorn app:app
```

Create `runtime.txt`:

```
python-3.9.18
```

Deploy:

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create nyc-property-ml-app

# Set environment variables
heroku config:set GOOGLE_MAPS_API_KEY=your_api_key

# Deploy
git push heroku main

# Open app
heroku open
```

### 5. API Service Deployment

#### FastAPI Service

Create `main.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
sys.path.append('src')

from analyzer import NYCPropertyInvestmentAnalyzer
import os

app = FastAPI(title="NYC Property Investment API", version="1.0.0")
api_key = os.environ.get('GOOGLE_MAPS_API_KEY', 'demo-api-key')
analyzer = NYCPropertyInvestmentAnalyzer(api_key)

class PropertyRequest(BaseModel):
    address: str

class BatchRequest(BaseModel):
    addresses: list[str]

@app.get("/")
def root():
    return {"message": "NYC Property Investment ML API"}

@app.post("/analyze")
def analyze_property(request: PropertyRequest):
    try:
        analysis = analyzer.analyze_property(request.address)
        return {
            "address": request.address,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-analyze")
def batch_analyze(request: BatchRequest):
    try:
        results = analyzer.batch_analyze_properties(request.addresses)
        return {
            "results": results.to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run with:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔧 Environment Configuration

### Production Environment Variables

```bash
# Required
GOOGLE_MAPS_API_KEY=your_production_api_key

# Database
DATABASE_URL=postgresql://user:pass@host:port/db  # For PostgreSQL
DATABASE_PATH=/app/data/nyc_property_data.db      # For SQLite

# Logging
LOG_LEVEL=WARNING
LOG_FILE=/app/logs/production.log

# Security
SECRET_KEY=your_secret_key_for_sessions
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com

# Performance
WORKERS=4
MAX_REQUESTS=1000
TIMEOUT=30
```

### Security Considerations

1. **API Key Management**:
   - Use environment variables
   - Rotate keys regularly
   - Implement rate limiting

2. **Database Security**:
   - Use PostgreSQL for production
   - Enable SSL connections
   - Regular backups

3. **Application Security**:
   - Input validation
   - SQL injection prevention
   - HTTPS encryption

## 📊 Monitoring and Logging

### Application Monitoring

```python
# monitoring.py
import logging
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logging.info(f"{func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"{func.__name__} failed after {duration:.2f}s: {e}")
            raise
    return wrapper
```

### Health Checks

```python
# health.py
@app.get("/health")
def health_check():
    try:
        # Test database connection
        analyzer.get_model_info()
        return {"status": "healthy", "timestamp": time.time()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

## 🔄 CI/CD Pipeline

### GitHub Actions Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to AWS
      run: |
        # Deploy to AWS Lambda
        aws lambda update-function-code \
          --function-name nyc-property-analyzer \
          --zip-file fileb://deployment.zip
```

### Automated Testing

```bash
# deployment/test_deployment.sh
#!/bin/bash

echo "Testing deployment..."

# Test API endpoint
response=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"address":"123 West 86th Street, New York, NY"}' \
  $API_URL/analyze)

if echo $response | grep -q "predicted_rent"; then
  echo "✅ API test passed"
else
  echo "❌ API test failed"
  exit 1
fi
```

## 📈 Scaling Considerations

### Performance Optimization

1. **Caching Strategy**:
   - Redis for API responses
   - Database query caching
   - Model prediction caching

2. **Database Optimization**:
   - Connection pooling
   - Query optimization
   - Read replicas

3. **Load Balancing**:
   - Multiple application instances
   - Database load balancing
   - CDN for static assets

### Cost Optimization

1. **API Usage**:
   - Cache API responses
   - Batch API calls
   - Use free tiers efficiently

2. **Infrastructure**:
   - Auto-scaling groups
   - Spot instances for non-critical workloads
   - Reserved instances for consistent workloads

For specific deployment questions, please refer to the cloud provider documentation or open an issue in the repository.
