#!/bin/bash

# NYC Property Investment ML - Web App Setup Script (Unix/Linux/Mac)

set -e  # Exit on any error

echo "================================================================"
echo "   NYC Property Investment ML - Web App Setup (Unix/Linux/Mac)"
echo "================================================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Python 3.8+ is installed
echo "🔍 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    print_error "Python is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    print_error "Python 3.8+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

print_status "Python $PYTHON_VERSION found"
echo

# Create virtual environment
echo "🔧 Setting up virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    print_status "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "Core requirements installed"
else
    print_warning "requirements.txt not found, skipping core requirements"
fi

if [ -f "web_requirements.txt" ]; then
    pip install -r web_requirements.txt
    print_status "Web app requirements installed"
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p web_app/templates
mkdir -p web_app/static/css
mkdir -p web_app/static/js
mkdir -p web_app/static/images
mkdir -p data
mkdir -p logs
mkdir -p models/saved_models

print_status "Directories created"
echo

# Setup environment file
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_status "Environment file created from template"
    else
        cat > .env << EOF
GOOGLE_MAPS_API_KEY=demo-api-key
DATABASE_PATH=data/nyc_property_data.db
LOG_LEVEL=INFO
EOF
        print_status "Basic environment file created"
    fi
else
    print_info "Environment file already exists"
fi

echo
print_warning "IMPORTANT: Edit .env file to add your Google API key for better accuracy"
echo

# Initialize database
echo "🗄️  Initializing database and ML model..."
if [ -f "scripts/setup_project.py" ]; then
    if $PYTHON_CMD scripts/setup_project.py; then
        print_status "Database initialized successfully"
    else
        print_warning "Database initialization had issues, but continuing..."
    fi
else
    print_warning "setup_project.py not found, skipping database initialization"
fi

echo
echo "================================================================"
echo "   🎉 Setup Complete!"
echo "================================================================"
echo
echo "📝 Next steps:"
echo "   1. Copy web app files to web_app/ directory:"
echo "      - app.py"
echo "      - templates/ folder"
echo "      - static/ folder"
echo
echo "   2. Start the web server:"
echo "      cd web_app"
echo "      python app.py"
echo
echo "   3. Open browser to: http://localhost:5000"
echo
print_warning "Remember to add your Google API key to .env for best results!"
echo

# Ask if user wants to start the app now
read -p "🚀 Would you like to start the web app now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "web_app/app.py" ]; then
        echo "🌐 Starting web application..."
        cd web_app
        $PYTHON_CMD app.py
    else
        print_error "web_app/app.py not found!"
        echo "Please copy the app.py file to the web_app/ directory first."
        exit 1
    fi
fi