#!/usr/bin/env python3
"""
NYC Property Investment ML - Web App File Organization Script
Automatically organizes all the web application files into the correct structure.
"""

import os
import shutil
from pathlib import Path

def create_file(file_path, content):
    """Create a file with given content"""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {file_path}")

def organize_web_app():
    """Organize all web application files"""
    
    print("🏙️  NYC Property Investment ML - Web App File Organization")
    print("=" * 60)
    print()
    
    # Create directory structure
    directories = [
        "web_app",
        "web_app/templates", 
        "web_app/static",
        "web_app/static/css",
        "web_app/static/js",
        "web_app/static/images",
        "data",
        "logs", 
        "models/saved_models"
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Directories created")
    print()
    
    # Flask Application (app.py)
    app_py_content = '''#!/usr/bin/env python3
"""
NYC Property Investment ML - Web Application
A Flask web interface for the property investment analysis system.
"""

import os
import sys
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import traceback
import json

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

try:
    from analyzer import NYCPropertyInvestmentAnalyzer
except ImportError as e:
    print(f"Error importing analyzer: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(project_root / '.env')
except ImportError:
    print("python-dotenv not available, using system environment variables")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global analyzer instance (initialized on first use)
analyzer = None

def get_analyzer():
    """Get or create analyzer instance"""
    global analyzer
    if analyzer is None:
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY', 'demo-api-key')
        logger.info(f"Initializing analyzer with API key: {'Real key' if api_key != 'demo-api-key' else 'Demo mode'}")
        try:
            analyzer = NYCPropertyInvestmentAnalyzer(api_key)
            logger.info("Analyzer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize analyzer: {e}")
            raise
    return analyzer

@app.route('/')
def index():
    """Main page with property analysis form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_property():
    """Analyze a single property"""
    try:
        data = request.get_json()
        address = data.get('address', '').strip()
        
        if not address:
            return jsonify({
                'success': False,
                'error': 'Address is required'
            }), 400
        
        logger.info(f"Analyzing property: {address}")
        
        # Get analyzer
        analyzer = get_analyzer()
        
        # Perform analysis
        analysis = analyzer.analyze_property(address)
        
        # Format response for frontend
        response_data = {
            'success': True,
            'analysis': {
                'address': analysis['property_details']['address'],
                'property_details': analysis['property_details'],
                'location_analysis': analysis['location_analysis'],
                'revenue_prediction': analysis['revenue_prediction'],
                'financial_metrics': analysis['financial_metrics'],
                'risk_assessment': analysis['risk_assessment'],
                'investment_recommendation': analysis['investment_recommendation'],
                'data_quality': analysis.get('data_quality', {}),
                'rental_comparables': analysis.get('rental_comparables', [])
            }
        }
        
        logger.info(f"Analysis completed for {address}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error analyzing property: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test analyzer initialization
        analyzer = get_analyzer()
        model_info = analyzer.get_model_info()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'model_type': model_info.get('model_type', 'Unknown'),
            'api_mode': 'Real API' if os.environ.get('GOOGLE_MAPS_API_KEY', 'demo-api-key') != 'demo-api-key' else 'Demo Mode'
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    print("🏙️  NYC Property Investment ML - Web Interface")
    print("=" * 50)
    print("🚀 Starting Flask application...")
    print("📍 Access the app at: http://localhost:5000")
    print("=" * 50)
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
'''
    
    create_file("web_app/app.py", app_py_content)
    
    # Base HTML Template
    base_html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}NYC Property Investment ML{% endblock %}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <i class="fas fa-building me-2"></i>
                NYC Property Investment ML
            </a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('index') }}">
                            <i class="fas fa-home me-1"></i>
                            Analyze Property
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('health_check') }}" target="_blank">
                            <i class="fas fa-heartbeat me-1"></i>
                            System Status
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>

    <!-- Loading Modal -->
    <div class="modal fade" id="loadingModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-body text-center py-4">
                    <div class="spinner-border text-primary mb-3" role="status" style="width: 3rem; height: 3rem;">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <h5 class="mb-2">Analyzing Property</h5>
                    <p class="mb-0 text-muted">
                        <span id="loadingText">Collecting real NYC data and running ML analysis...</span>
                    </p>
                    <div class="progress mt-3" style="height: 6px;">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JavaScript -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    
    {% block scripts %}{% endblock %}
</body>
</html>'''
    
    create_file("web_app/templates/base.html", base_html_content)
    
    # Main Page Template (simplified)
    index_html_content = '''{% extends "base.html" %}

{% block content %}
<!-- Hero Section -->
<section class="hero-section bg-gradient text-white py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-8 mx-auto text-center">
                <h1 class="display-4 fw-bold mb-3">
                    <i class="fas fa-chart-line me-3"></i>
                    NYC Property Investment Analysis
                </h1>
                <p class="lead mb-4">
                    Get AI-powered investment insights for NYC real estate using real data and machine learning.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- Analysis Form Section -->
<section class="analysis-section py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="analysis-card card shadow-lg">
                    <div class="card-header bg-primary text-white text-center">
                        <h3 class="mb-0">
                            <i class="fas fa-search me-2"></i>
                            Analyze NYC Property
                        </h3>
                        <p class="mb-0">Enter a NYC address to get comprehensive investment analysis</p>
                    </div>
                    <div class="card-body p-4">
                        <form id="analysisForm">
                            <div class="input-group input-group-lg mb-3">
                                <span class="input-group-text">
                                    <i class="fas fa-map-marker-alt"></i>
                                </span>
                                <input 
                                    type="text" 
                                    class="form-control" 
                                    id="addressInput" 
                                    placeholder="e.g., 123 West 86th Street, New York, NY"
                                    required
                                >
                                <button class="btn btn-primary" type="submit" id="analyzeBtn">
                                    <i class="fas fa-chart-line me-2"></i>
                                    Analyze Property
                                </button>
                            </div>
                        </form>

                        <!-- Example Addresses -->
                        <div class="example-addresses mt-4 p-3 bg-light rounded">
                            <h6 class="mb-3">
                                <i class="fas fa-lightbulb me-2"></i>
                                Try these example addresses:
                            </h6>
                            <div class="row g-2">
                                <div class="col-md-6">
                                    <button class="btn btn-outline-secondary btn-sm w-100 example-btn" 
                                            data-address="350 Central Park West, New York, NY">
                                        350 Central Park West (UWS)
                                    </button>
                                </div>
                                <div class="col-md-6">
                                    <button class="btn btn-outline-secondary btn-sm w-100 example-btn" 
                                            data-address="1 Wall Street, New York, NY">
                                        1 Wall Street (Financial District)
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Results Container (Hidden by default) -->
<div id="resultsContainer" style="display: none;">
    <section class="results-section py-5 bg-light">
        <div class="container">
            <h2 class="fw-bold mb-4">
                <i class="fas fa-chart-line me-2"></i>
                Investment Analysis Results
            </h2>
            
            <!-- Analysis Results Content will be dynamically inserted here -->
            <div id="resultsContent"></div>
        </div>
    </section>
</div>
{% endblock %}

{% block scripts %}
<script>
// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    initializeAnalysisForm();
    initializeExampleButtons();
});

function initializeAnalysisForm() {
    const form = document.getElementById('analysisForm');
    const addressInput = document.getElementById('addressInput');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const address = addressInput.value.trim();
        
        if (!address) {
            alert('Please enter a property address');
            return;
        }
        
        analyzeProperty(address);
    });
}

function initializeExampleButtons() {
    const exampleBtns = document.querySelectorAll('.example-btn');
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const address = this.dataset.address;
            document.getElementById('addressInput').value = address;
            analyzeProperty(address);
        });
    });
}

async function analyzeProperty(address) {
    try {
        // Show loading modal
        showLoadingModal();
        
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: address })
        });
        
        const data = await response.json();
        
        if (data.success) {
            hideLoadingModal();
            displayResults(data.analysis);
        } else {
            hideLoadingModal();
            alert(data.error || 'Analysis failed');
        }
        
    } catch (error) {
        hideLoadingModal();
        console.error('Error:', error);
        alert('Connection error. Please try again.');
    }
}

function displayResults(analysis) {
    document.getElementById('resultsContainer').style.display = 'block';
    document.getElementById('resultsContainer').scrollIntoView({ behavior: 'smooth' });
    
    const resultsHTML = generateResultsHTML(analysis);
    document.getElementById('resultsContent').innerHTML = resultsHTML;
}

function generateResultsHTML(analysis) {
    const prop = analysis.property_details;
    const fin = analysis.financial_metrics;
    const rec = analysis.investment_recommendation;
    const rev = analysis.revenue_prediction;
    
    return `
        <div class="row g-4">
            <div class="col-lg-4">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Property Overview</h5>
                    </div>
                    <div class="card-body">
                        <h6>${prop.address}</h6>
                        <p><strong>Type:</strong> ${prop.property_type}</p>
                        <p><strong>Bedrooms:</strong> ${prop.bedrooms}</p>
                        <p><strong>Square Feet:</strong> ${prop.sqft.toLocaleString()}</p>
                        <p><strong>Year Built:</strong> ${prop.year_built}</p>
                    </div>
                </div>
            </div>
            
            <div class="col-lg-4">
                <div class="card h-100">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">Financial Analysis</h5>
                    </div>
                    <div class="card-body">
                        <div class="text-center mb-3">
                            <h3 class="text-primary">$${Math.round(rev.predicted_monthly_rent).toLocaleString()}</h3>
                            <small class="text-muted">Monthly Rent Prediction</small>
                        </div>
                        <p><strong>Gross Yield:</strong> ${fin.gross_rental_yield}%</p>
                        <p><strong>Net Yield:</strong> ${fin.net_rental_yield}%</p>
                        <p><strong>Cash Flow:</strong> $${Math.round(fin.monthly_cash_flow).toLocaleString()}/month</p>
                    </div>
                </div>
            </div>
            
            <div class="col-lg-4">
                <div class="card h-100">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0">Recommendation</h5>
                    </div>
                    <div class="card-body text-center">
                        <div class="mb-3">
                            <span class="badge bg-primary fs-6 p-2">${rec.recommendation}</span>
                        </div>
                        <p><strong>Confidence:</strong> ${rec.confidence}</p>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function showLoadingModal() {
    const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
    modal.show();
}

function hideLoadingModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
    if (modal) {
        modal.hide();
    }
}
</script>
{% endblock %}'''
    
    create_file("web_app/templates/index.html", index_html_content)
    
    # Basic CSS
    css_content = '''/* NYC Property Investment ML - Custom Styles */
:root {
    --primary-color: #0d6efd;
    --success-color: #198754;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #0dcaf0;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.analysis-card {
    border: none;
    border-radius: 1rem;
}

.input-group-lg .form-control,
.input-group-lg .btn {
    border-radius: 0.75rem;
}

.example-btn {
    transition: all 0.3s ease;
}

.example-btn:hover {
    transform: translateY(-2px);
}

.card {
    border-radius: 0.75rem;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.progress {
    border-radius: 1rem;
}

@media (max-width: 768px) {
    .hero-section {
        padding: 2rem 0;
    }
    
    .analysis-card .card-body {
        padding: 2rem 1rem;
    }
}'''
    
    create_file("web_app/static/css/style.css", css_content)
    
    # Basic JavaScript
    js_content = '''// NYC Property Investment ML - Main JavaScript Functions

function showToast(message, type = 'info') {
    // Simple alert for now - can be enhanced with toast notifications
    alert(message);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

// Global utilities
window.PropertyAnalysisUtils = {
    showToast,
    formatCurrency,
    formatNumber
};'''
    
    create_file("web_app/static/js/main.js", js_content)
    
    # Web requirements
    web_req_content = '''# NYC Property Investment ML - Web App Requirements
Flask>=2.3.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
requests>=2.31.0
python-dotenv>=1.0.0
geopy>=2.3.0
joblib>=1.3.0'''
    
    create_file("web_requirements.txt", web_req_content)
    
    print()
    print("🎉 Web application files created successfully!")
    print()
    print("📝 Next steps:")
    print("   1. Install requirements: pip install -r web_requirements.txt")
    print("   2. Copy your existing src/ folder to the project root")
    print("   3. Start the app: cd web_app && python app.py")
    print("   4. Open browser to: http://localhost:5000")
    print()
    print("💡 Don't forget to add your Google API key to .env for better accuracy!")

if __name__ == "__main__":
    organize_web_app()