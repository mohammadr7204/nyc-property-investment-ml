#!/usr/bin/env python3
"""
Complete Setup and Launch Script for NYC Property Investment ML
Handles everything needed to get the system running from a fresh clone.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import time
import platform

def print_banner():
    """Print welcome banner"""
    print("🏙️" + "="*70 + "🏙️")
    print("   NYC Property Investment ML - Complete Setup & Launch")
    print("   AI-Powered Real Estate Analysis with Real NYC Data")
    print("🏙️" + "="*70 + "🏙️")
    print()

def check_python():
    """Check Python version"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {sys.version}")
        print("   Please install Python 3.8 or newer from https://python.org")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def install_requirements():
    """Install all required packages"""
    print("\n📦 Installing required packages...")
    
    # Core requirements
    req_files = ['requirements.txt', 'web_requirements.txt']
    
    for req_file in req_files:
        if Path(req_file).exists():
            print(f"   Installing from {req_file}...")
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', req_file
                ], check=True, capture_output=True)
                print(f"   ✅ {req_file} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"   ⚠️ Error installing {req_file}: {e}")
                print("   Continuing with individual package installation...")
                
                # Try individual packages
                essential_packages = [
                    'flask', 'pandas', 'numpy', 'scikit-learn', 
                    'requests', 'python-dotenv', 'geopy', 'joblib'
                ]
                
                for package in essential_packages:
                    try:
                        subprocess.run([
                            sys.executable, '-m', 'pip', 'install', package
                        ], check=True, capture_output=True)
                        print(f"     ✅ {package}")
                    except:
                        print(f"     ⚠️ Failed to install {package}")
        else:
            print(f"   ⚠️ {req_file} not found, skipping")
    
    print("✅ Package installation complete")

def setup_environment():
    """Setup environment configuration"""
    print("\n🔧 Setting up environment...")
    
    # Create .env from example if it doesn't exist
    if not Path('.env').exists():
        if Path('.env.example').exists():
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from template")
        else:
            # Create basic .env file
            env_content = """# Google Maps API Key (optional - enhances accuracy)
GOOGLE_MAPS_API_KEY=demo-api-key

# NYC Open Data App Token (optional - higher rate limits)
NYC_OPEN_DATA_APP_TOKEN=your_nyc_open_data_app_token_here

# Database Configuration
DATABASE_PATH=data/nyc_property_data.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/pipeline.log

# NYC Geographic Boundaries
NYC_LAT_MIN=40.4774
NYC_LAT_MAX=40.9176
NYC_LNG_MIN=-74.2591
NYC_LNG_MAX=-73.7004
"""
            Path('.env').write_text(env_content)
            print("✅ Created basic .env file")
    else:
        print("✅ Environment file already exists")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directory structure...")
    
    directories = [
        'data', 'logs', 'models/saved_models',
        'web_app/static/css', 'web_app/static/js', 'web_app/static/images',
        'tests', 'notebooks'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")

def initialize_system():
    """Initialize the ML system"""
    print("\n🤖 Initializing ML system...")
    
    try:
        # Try to run setup script
        if Path('scripts/setup_project.py').exists():
            subprocess.run([sys.executable, 'scripts/setup_project.py'], 
                         check=True, capture_output=True, text=True)
            print("✅ Database and ML model initialized")
        else:
            print("⚠️ Setup script not found, manual initialization required")
            
    except subprocess.CalledProcessError as e:
        print("⚠️ Setup had some issues, but system should still work")
        print("   You can run setup manually later: python scripts/setup_project.py")

def test_system():
    """Test if the system works"""
    print("\n🧪 Testing system...")
    
    try:
        # Quick system test
        if Path('scripts/test_system.py').exists():
            result = subprocess.run([sys.executable, 'scripts/test_system.py'], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print("✅ System tests passed")
            else:
                print("⚠️ Some tests failed, but basic functionality should work")
        else:
            print("⚠️ Test script not found")
            
        # Test imports
        print("   Testing core imports...")
        test_imports = [
            "import sys; sys.path.append('src')",
            "from analyzer import NYCPropertyInvestmentAnalyzer",
            "from data_pipeline import NYCPropertyDataPipeline", 
            "from ml_model import NYCRevenuePredictor",
            "print('✅ All core modules imported successfully')"
        ]
        
        subprocess.run([
            sys.executable, '-c', '; '.join(test_imports)
        ], check=True, capture_output=True)
        print("✅ Core system functional")
        
    except Exception as e:
        print(f"⚠️ System test encountered issues: {e}")
        print("   System may still work, continuing...")

def show_configuration_info():
    """Show configuration and usage information"""
    print("\n" + "="*70)
    print("📋 SETUP COMPLETE - CONFIGURATION INFO")
    print("="*70)
    
    # Check API configuration
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        google_key = os.getenv('GOOGLE_MAPS_API_KEY', 'demo-api-key')
        nyc_token = os.getenv('NYC_OPEN_DATA_APP_TOKEN', '')
        
        print("\n🔑 API Configuration:")
        if google_key == 'demo-api-key':
            print("   Google API: 🟡 Demo mode (still uses real NYC data)")
            print("   → Add real key to .env for enhanced accuracy")
        else:
            print("   Google API: 🟢 Configured")
            
        if nyc_token and nyc_token != 'your_nyc_open_data_app_token_here':
            print("   NYC Open Data: 🟢 Token configured")
        else:
            print("   NYC Open Data: 🟡 Using public access (may have rate limits)")
            
    except ImportError:
        print("   ⚠️ Could not check API configuration")

def show_usage_options():
    """Show usage options"""
    print("\n🚀 READY TO USE! Choose your interface:")
    print("\n1. 🌐 Web Interface (Recommended):")
    print("   python start_web_app.py")
    print("   → Then visit: http://localhost:5000")
    
    print("\n2. 🖥️ Command Line:")
    print("   python scripts/run_analysis.py -a '350 Central Park West, New York, NY'")
    
    print("\n3. 🐍 Python API:")
    print("   from src.analyzer import NYCPropertyInvestmentAnalyzer")
    print("   analyzer = NYCPropertyInvestmentAnalyzer('demo-api-key')")
    print("   result = analyzer.analyze_property('Your Address')")
    
    print("\n4. 🔧 Diagnostic Tools:")
    print("   python scripts/diagnose_data_issues.py")
    print("   python scripts/demo_real_data.py")

def start_web_app():
    """Start the web application"""
    print("\n🌐 Starting web application...")
    print("   The app will open at: http://localhost:5000")
    print("   Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Change to web_app directory if it exists
        if Path('web_app/app.py').exists():
            os.chdir('web_app')
            subprocess.run([sys.executable, 'app.py'])
        else:
            print("❌ Web app not found. Try command line interface instead:")
            print("   python scripts/run_analysis.py -a 'Your Address'")
            
    except KeyboardInterrupt:
        print("\n⏹️ Web application stopped")
    except Exception as e:
        print(f"\n❌ Error starting web app: {e}")
        print("   Try the command line interface:")
        print("   python scripts/run_analysis.py -a 'Your Address'")

def main():
    """Main setup function"""
    print_banner()
    
    # Step 1: Check Python
    if not check_python():
        return False
    
    # Step 2: Install packages
    install_requirements()
    
    # Step 3: Setup environment
    setup_environment()
    
    # Step 4: Create directories
    create_directories()
    
    # Step 5: Initialize system
    initialize_system()
    
    # Step 6: Test system
    test_system()
    
    # Step 7: Show configuration
    show_configuration_info()
    
    # Step 8: Show usage options
    show_usage_options()
    
    # Step 9: Ask about starting web app
    print("\n" + "="*70)
    print("🎉 SETUP COMPLETE!")
    print("="*70)
    
    try:
        response = input("\n🚀 Start the web application now? (y/n): ").lower().strip()
        if response in ['y', 'yes', '']:
            start_web_app()
        else:
            print("\n💡 Start anytime with: python start_web_app.py")
            print("📚 Or try CLI: python scripts/run_analysis.py -a 'Your Address'")
    except KeyboardInterrupt:
        print("\n👋 Setup complete! Use any of the interfaces shown above.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)