#!/usr/bin/env python3
"""
NYC Property Investment ML - Auto Web App Starter
Automatically sets up and starts the web application with all dependencies.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} found")
    return True

def check_and_install_requirements():
    """Check and install required packages"""
    print("📦 Checking Python packages...")
    
    required_packages = [
        'flask', 'pandas', 'numpy', 'scikit-learn', 'requests',
        'python-dotenv', 'geopy', 'joblib'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"📥 Installing missing packages: {', '.join(missing)}")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing, 
                         check=True, capture_output=True)
            print("✅ Packages installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            return False
    else:
        print("✅ All required packages are installed")
    
    return True

def check_file_structure():
    """Check if all necessary files exist"""
    print("📋 Checking file structure...")
    
    required_files = [
        'src/__init__.py',
        'src/analyzer.py',
        'src/data_pipeline.py', 
        'src/ml_model.py',
        'web_app/app.py',
        'web_app/templates/base.html',
        'web_app/templates/index.html',
        'web_app/static/js/main.js',
        'scripts/setup_project.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def setup_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        'web_app/static/css',
        'web_app/static/js',
        'web_app/static/images',
        'data',
        'logs',
        'models/saved_models'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def setup_environment():
    """Setup environment file"""
    print("🔧 Setting up environment...")
    
    if not Path('.env').exists():
        if Path('.env.example').exists():
            shutil.copy('.env.example', '.env')
            print("✅ Environment file created from template")
        else:
            env_content = """# Google Maps API Key (get from https://console.cloud.google.com/)
GOOGLE_MAPS_API_KEY=demo-api-key

# NYC Open Data App Token (optional but recommended)
NYC_OPEN_DATA_APP_TOKEN=your_nyc_open_data_app_token_here

# Database Configuration
DATABASE_PATH=data/nyc_property_data.db
DATABASE_URL=sqlite:///data/nyc_property_data.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/pipeline.log"""
            Path('.env').write_text(env_content)
            print("✅ Basic environment file created")
    else:
        print("✅ Environment file already exists")

def initialize_system():
    """Initialize the ML system"""
    print("🤖 Initializing ML system...")
    
    if Path('scripts/setup_project.py').exists():
        try:
            result = subprocess.run([sys.executable, 'scripts/setup_project.py'], 
                                  check=True, capture_output=True, text=True)
            print("✅ System initialized successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Setup script had issues: {e}")
            print("   The system may still work with basic functionality")
            return False
    else:
        print("⚠️  Setup script not found, skipping system initialization")
        return False

def test_system():
    """Test if the system works"""
    print("🧪 Testing system...")
    
    if Path('scripts/test_system.py').exists():
        try:
            subprocess.run([sys.executable, 'scripts/test_system.py'], 
                         check=True, capture_output=True, timeout=60)
            print("✅ System tests passed")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  Some system tests failed, but continuing...")
            return False
        except subprocess.TimeoutExpired:
            print("⚠️  System tests timed out, but continuing...")
            return False
    else:
        print("⚠️  Test script not found, skipping tests")
        return False

def start_web_app():
    """Start the web application"""
    print("\n🚀 Starting web application...")
    print("   Access at: http://localhost:5000")
    print("   Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        # Check if we're already in web_app directory
        if Path.cwd().name != 'web_app':
            if Path('web_app/app.py').exists():
                os.chdir('web_app')
            else:
                print("❌ web_app/app.py not found")
                return False
        
        # Start the Flask app
        subprocess.run([sys.executable, 'app.py'])
        
    except KeyboardInterrupt:
        print("\n⏹️  Web application stopped by user")
    except FileNotFoundError:
        print("❌ Python executable not found")
    except Exception as e:
        print(f"❌ Error starting web app: {e}")
    
    return True

def main():
    """Main setup and start function"""
    print("🏙️  NYC Property Investment ML - Auto Setup & Start")
    print("=" * 60)
    
    # Check system requirements
    if not check_python_version():
        return False
    
    # Check file structure
    if not check_file_structure():
        print("\n❌ Missing core files. Make sure you've cloned the complete repository.")
        print("   Try: git clone https://github.com/mohammadr7204/nyc-property-investment-ml.git")
        return False
    
    # Install packages
    if not check_and_install_requirements():
        return False
    
    # Setup system
    setup_directories()
    setup_environment()
    
    # Initialize the ML system
    system_ready = initialize_system()
    
    # Test system (optional)
    if system_ready:
        test_system()
    
    print("\n" + "=" * 60)
    print("🎉 Setup complete!")
    print("=" * 60)
    
    # Show configuration info
    api_key = os.getenv('GOOGLE_MAPS_API_KEY', 'demo-api-key')
    if api_key == 'demo-api-key':
        print("\n💡 Running in demo mode")
        print("   For better accuracy, add your Google API key to .env file")
        print("   Get one at: https://console.cloud.google.com/")
    else:
        print("\n🔑 Google API key configured")
    
    # Ask if user wants to start the app
    try:
        start_now = input("\n🚀 Start the web application now? (y/n): ").lower().strip()
        if start_now in ['y', 'yes', '']:
            start_web_app()
        else:
            print("\n💡 To start later, run:")
            print("   cd web_app")
            print("   python app.py")
            print("\n📚 Or try the command line interface:")
            print("   python scripts/run_analysis.py -a 'Your NYC Address'")
    except KeyboardInterrupt:
        print("\n👋 Setup complete!")
        print("\n💡 Start the web app anytime with:")
        print("   cd web_app && python app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
