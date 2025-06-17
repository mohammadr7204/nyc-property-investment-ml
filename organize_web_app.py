#!/usr/bin/env python3
"""
Web App Organization Script
Ensures all web app files are properly organized and sets up the complete web interface.
"""

import os
import shutil
from pathlib import Path
import sys

def organize_web_app_files():
    """Organize all web app files into proper structure"""
    print("🌐 Organizing Web App Files...")
    
    # Ensure web_app directory structure exists
    web_app_dirs = [
        'web_app',
        'web_app/templates', 
        'web_app/static',
        'web_app/static/css',
        'web_app/static/js',
        'web_app/static/images'
    ]
    
    for directory in web_app_dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Check if main files exist
    required_files = {
        'web_app/app.py': 'Flask application main file',
        'web_app/templates/base.html': 'Base HTML template',
        'web_app/templates/index.html': 'Main page template',
        'web_app/static/css/style.css': 'Custom CSS styles',
        'web_app/static/js/main.js': 'JavaScript functionality'
    }
    
    missing_files = []
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print(f"✅ {description}: {file_path}")
        else:
            missing_files.append((file_path, description))
            print(f"❌ Missing {description}: {file_path}")
    
    if missing_files:
        print(f"\n⚠️  {len(missing_files)} files are missing from the web app")
        print("   All required files should already be present in the repository")
    else:
        print("\n🎉 All web app files are properly organized!")
    
    return len(missing_files) == 0

def verify_web_app_functionality():
    """Verify the web app can be imported and basic functionality works"""
    print("\n🔍 Verifying Web App Functionality...")
    
    try:
        # Test that we can import the core modules
        sys.path.insert(0, str(Path('src')))
        
        from analyzer import NYCPropertyInvestmentAnalyzer
        from data_pipeline import NYCPropertyDataPipeline
        from ml_model import NYCRevenuePredictor
        
        print("✅ Core modules imported successfully")
        
        # Test analyzer initialization
        analyzer = NYCPropertyInvestmentAnalyzer('demo-api-key')
        print("✅ Analyzer initializes successfully")
        
        # Test basic functionality
        model_info = analyzer.get_model_info()
        print(f"✅ ML model ready: {model_info['model_type']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Web app verification failed: {e}")
        return False

def create_web_app_launcher():
    """Create a convenient launcher script for the web app"""
    print("\n🚀 Creating Web App Launcher...")
    
    launcher_content = '''#!/usr/bin/env python3
"""
NYC Property Investment ML - Web App Launcher
Quick launcher for the web application
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Launch the web application"""
    print("🏙️  NYC Property Investment ML - Web App Launcher")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path('web_app/app.py').exists():
        print("❌ web_app/app.py not found!")
        print("   Make sure you're running from the project root directory")
        return False
    
    # Change to web_app directory and run
    print("🚀 Starting web application...")
    print("📍 Access at: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        os.chdir('web_app')
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\\n⏹️  Web application stopped")
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
'''
    
    with open('launch_web_app.py', 'w') as f:
        f.write(launcher_content)
    
    # Make it executable on Unix systems
    try:
        os.chmod('launch_web_app.py', 0o755)
    except:
        pass  # Windows doesn't support chmod
    
    print("✅ Created launch_web_app.py")

def update_main_readme():
    """Update README with web app launch instructions"""
    print("\n📚 Updating README with web app instructions...")
    
    # The README already contains comprehensive web app instructions
    # Just verify it mentions the web app
    readme_path = Path('README.md')
    if readme_path.exists():
        readme_content = readme_path.read_text()
        if 'web app' in readme_content.lower() or 'web interface' in readme_content.lower():
            print("✅ README already contains web app instructions")
        else:
            print("⚠️  README might need web app instructions added")
    else:
        print("⚠️  README.md not found")

def main():
    """Main organization function"""
    print("🏙️  NYC Property Investment ML - Web App Organization")
    print("=" * 70)
    print("Organizing and verifying web application setup...")
    print("=" * 70)
    
    # Step 1: Organize file structure
    files_organized = organize_web_app_files()
    
    # Step 2: Verify functionality
    functionality_verified = verify_web_app_functionality()
    
    # Step 3: Create launcher script
    create_web_app_launcher()
    
    # Step 4: Update documentation
    update_main_readme()
    
    print("\n" + "=" * 70)
    print("📋 WEB APP ORGANIZATION SUMMARY")
    print("=" * 70)
    
    if files_organized and functionality_verified:
        print("🎉 WEB APP ORGANIZATION COMPLETE!")
        print("✅ All files properly organized")
        print("✅ Functionality verified")
        print("✅ Launcher script created")
        
        print("\n🚀 READY TO USE!")
        print("Choose your preferred way to start:")
        print("  1. Auto-setup:     python start_web_app.py")
        print("  2. Quick launch:   python launch_web_app.py")
        print("  3. Manual:         cd web_app && python app.py")
        print("  4. Complete setup: python complete_setup.py")
        
        print("\n📱 Once started, access at: http://localhost:5000")
        
        return True
    else:
        print("⚠️  Some issues detected during organization")
        if not files_organized:
            print("❌ File organization incomplete")
        if not functionality_verified:
            print("❌ Functionality verification failed")
        
        print("\n🔧 Try running the setup script:")
        print("   python scripts/setup_project.py")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
