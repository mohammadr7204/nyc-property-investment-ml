@echo off
echo ================================================================
echo   NYC Property Investment ML - Web App Setup (Windows)
echo ================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

:: Create virtual environment
echo 🔧 Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ℹ️  Virtual environment already exists
)

:: Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

:: Install requirements
echo 📦 Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt
if exist "web_requirements.txt" (
    pip install -r web_requirements.txt
)

:: Create directories
echo 📁 Creating directories...
if not exist "web_app" mkdir web_app
if not exist "web_app\templates" mkdir web_app\templates
if not exist "web_app\static" mkdir web_app\static
if not exist "web_app\static\css" mkdir web_app\static\css
if not exist "web_app\static\js" mkdir web_app\static\js
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "models\saved_models" mkdir models\saved_models

echo ✅ Directories created
echo.

:: Setup environment file
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo ✅ Environment file created from template
    ) else (
        echo GOOGLE_MAPS_API_KEY=demo-api-key > .env
        echo DATABASE_PATH=data/nyc_property_data.db >> .env
        echo LOG_LEVEL=INFO >> .env
        echo ✅ Basic environment file created
    )
) else (
    echo ℹ️  Environment file already exists
)

echo.
echo 💡 IMPORTANT: Edit .env file to add your Google API key for better accuracy
echo.

:: Initialize database
echo 🗄️  Initializing database and ML model...
python scripts\setup_project.py
if errorlevel 1 (
    echo ⚠️  Database initialization had issues, but continuing...
) else (
    echo ✅ Database initialized successfully
)

echo.
echo ================================================================
echo   🎉 Setup Complete!
echo ================================================================
echo.
echo 📝 Next steps:
echo   1. Copy web app files to web_app/ directory:
echo      - app.py
echo      - templates/ folder
echo      - static/ folder
echo.
echo   2. Start the web server:
echo      cd web_app
echo      python app.py
echo.
echo   3. Open browser to: http://localhost:5000
echo.
echo ⚠️  Remember to add your Google API key to .env for best results!
echo.
pause