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

def setup_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        'web_app',
        'web_app/templates', 
        'web_app/static/css',
        'web_app/static/js',
        'data',
        'logs',
        'models/saved_models'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def create_web_app_files():
    """Create the web application files"""
    print("🔧 Creating web application files...")
    
    # Run the organize_web_app.py script if it exists
    if Path('organize_web_app.py').exists():
        try:
            subprocess.run([sys.executable, 'organize_web_app.py'], 
                         check=True, capture_output=True)
            print("✅ Web app files organized")
        except subprocess.CalledProcessError:
            print("⚠️  organize_web_app.py failed, creating files manually...")
            create_basic_web_files()
    else:
        create_basic_web_files()

def create_basic_web_files():
    """Create basic web files if organize script not available"""
    
    # Basic Flask app
    app_py = """from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from analyzer import NYCPropertyInvestmentAnalyzer
except ImportError:
    print("Error: Could not import analyzer. Make sure src/ directory exists.")
    sys.exit(1)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    address = data.get('address', '').strip()
    
    if not address:
        return jsonify({'success': False, 'error': 'Address required'}), 400
    
    try:
        analyzer = NYCPropertyInvestmentAnalyzer('demo-api-key')
        analysis = analyzer.analyze_property(address)
        
        return jsonify({
            'success': True,
            'analysis': {
                'property_details': analysis['property_details'],
                'revenue_prediction': analysis['revenue_prediction'],
                'financial_metrics': analysis['financial_metrics'],
                'investment_recommendation': analysis['investment_recommendation']
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🏙️  NYC Property Investment ML - Web Interface")
    print("🚀 Starting at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
"""
    
    # Basic HTML template
    index_html = """<!DOCTYPE html>
<html>
<head>
    <title>NYC Property Investment ML</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center mb-4">🏙️ NYC Property Investment Analysis</h1>
        
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-body">
                        <form id="analysisForm">
                            <div class="mb-3">
                                <label class="form-label">Property Address</label>
                                <input type="text" class="form-control" id="addressInput" 
                                       placeholder="123 West 86th Street, New York, NY">
                            </div>
                            <button type="submit" class="btn btn-primary">Analyze Property</button>
                        </form>
                    </div>
                </div>
                
                <div id="results" class="mt-4" style="display:none;">
                    <div class="card">
                        <div class="card-body">
                            <h5>Analysis Results</h5>
                            <div id="resultsContent"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('analysisForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const address = document.getElementById('addressInput').value;
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({address: address})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    const analysis = data.analysis;
                    document.getElementById('resultsContent').innerHTML = `
                        <p><strong>Address:</strong> ${analysis.property_details.address}</p>
                        <p><strong>Predicted Rent:</strong> $${analysis.revenue_prediction.predicted_monthly_rent.toLocaleString()}/month</p>
                        <p><strong>Gross Yield:</strong> ${analysis.financial_metrics.gross_rental_yield}%</p>
                        <p><strong>Recommendation:</strong> ${analysis.investment_recommendation.recommendation}</p>
                    `;
                    document.getElementById('results').style.display = 'block';
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                alert('Connection error: ' + error.message);
            }
        });
    </script>
</body>
</html>"""
    
    # Write files
    Path('web_app/app.py').write_text(app_py)
    Path('web_app/templates/index.html').write_text(index_html)
    
    print("✅ Basic web files created")

def setup_environment():
    """Setup environment file"""
    print("🔧 Setting up environment...")
    
    if not Path('.env').exists():
        if Path('.env.example').exists():
            shutil.copy('.env.example', '.env')
            print("✅ Environment file created from template")
        else:
            env_content = """GOOGLE_MAPS_API_KEY=demo-api-key
DATABASE_PATH=data/nyc_property_data.db
LOG_LEVEL=INFO"""
            Path('.env').write_text(env_content)
            print("✅ Basic environment file created")
    else:
        print("✅ Environment file already exists")

def initialize_system():
    """Initialize the ML system"""
    print("🤖 Initializing ML system...")
    
    if Path('scripts/setup_project.py').exists():
        try:
            subprocess.run([sys.executable, 'scripts/setup_project.py'], 
                         check=True, capture_output=True)
            print("✅ System initialized")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Setup script failed: {e}")
            print("   The system may still work with basic functionality")
    else:
        print("⚠️  Setup script not found, skipping system initialization")

def start_web_app():
    """Start the web application"""
    print("\n🚀 Starting web application...")
    print("   Access at: http://localhost:5000")
    print("   Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        os.chdir('web_app')
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n⏹️  Web application stopped")
    except FileNotFoundError:
        print("❌ Web application files not found")
        print("   Make sure web_app/app.py exists")

def main():
    """Main setup and start function"""
    print("🏙️  NYC Property Investment ML - Auto Setup & Start")
    print("=" * 60)
    
    # Check requirements
    if not check_python_version():
        return False
    
    if not check_and_install_requirements():
        return False
    
    # Setup system
    setup_directories()
    setup_environment()
    create_web_app_files()
    initialize_system()
    
    print("\n" + "=" * 60)
    print("🎉 Setup complete!")
    print("=" * 60)
    
    # Ask if user wants to start the app
    try:
        start_now = input("\n🚀 Start the web application now? (y/n): ").lower().strip()
        if start_now in ['y', 'yes']:
            start_web_app()
        else:
            print("\n💡 To start later, run:")
            print("   cd web_app")
            print("   python app.py")
    except KeyboardInterrupt:
        print("\n👋 Setup complete! Start the app anytime with: cd web_app && python app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)