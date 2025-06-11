#!/usr/bin/env python3
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
import numpy as np

# Add project root to Python path
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from src.analyzer import NYCPropertyInvestmentAnalyzer
except ImportError as e:
    print(f"Error importing analyzer: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Project root: {project_root}")
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

def convert_numpy_types(obj):
    """Convert NumPy types to Python native types for JSON serialization."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception: {e}")
    logger.error(traceback.format_exc())
    return render_template('500.html'), 500

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
        analyzer_instance = get_analyzer()

        # Perform analysis
        analysis = analyzer_instance.analyze_property(address)

        # Convert NumPy types to Python native types
        response_data = convert_numpy_types(analysis)

        logger.info(f"Analysis completed for {address}")
        return jsonify({
            'success': True,
            'analysis': response_data
        })

    except Exception as e:
        logger.error(f"Error analyzing property: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/batch-analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple properties"""
    try:
        data = request.get_json()
        addresses = data.get('addresses', [])

        if not addresses:
            return jsonify({
                'success': False,
                'error': 'At least one address is required'
            }), 400

        logger.info(f"Batch analyzing {len(addresses)} properties")

        analyzer_instance = get_analyzer()
        results = analyzer_instance.batch_analyze_properties(addresses)

        return jsonify({
            'success': True,
            'results': results.to_dict('records') if not results.empty else []
        })

    except Exception as e:
        logger.error(f"Error in batch analysis: {e}")
        return jsonify({
            'success': False,
            'error': f'Batch analysis failed: {str(e)}'
        }), 500

@app.route('/report/<path:address>')
def generate_report(address):
    """Generate detailed report for a property"""
    try:
        analyzer_instance = get_analyzer()
        analysis = analyzer_instance.analyze_property(address)
        report = analyzer_instance.generate_detailed_report(analysis)

        # Save report to temp file and send
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(report)
            temp_path = f.name

        return send_file(
            temp_path,
            as_attachment=True,
            download_name=f"property_analysis_{address.replace(' ', '_').replace(',', '')}.txt",
            mimetype='text/plain'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test analyzer initialization
        analyzer_instance = get_analyzer()
        model_info = analyzer_instance.get_model_info()

        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'model_type': model_info.get('model_type', 'Unknown'),
            'api_mode': 'Real API' if os.environ.get('GOOGLE_MAPS_API_KEY', 'demo-api-key') != 'demo-api-key' else 'Demo Mode',
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/examples')
def get_examples():
    """Get example addresses for testing"""
    examples = [
        {
            'address': '350 Central Park West, New York, NY',
            'description': 'Upper West Side Luxury Building'
        },
        {
            'address': '1 Wall Street, New York, NY',
            'description': 'Financial District Historic Building'
        },
        {
            'address': '123 West 86th Street, New York, NY',
            'description': 'Upper West Side Residential'
        },
        {
            'address': '456 East 74th Street, New York, NY',
            'description': 'Upper East Side Apartment'
        }
    ]

    return jsonify({'examples': examples})

if __name__ == '__main__':
    print("🏙️  NYC Property Investment ML - Web Interface")
    print("=" * 50)
    print("🚀 Starting Flask application...")
    print("📍 Access the app at: http://localhost:8080")
    print("🔧 API endpoints:")
    print("   POST /analyze - Single property analysis")
    print("   POST /batch-analyze - Multiple property analysis")
    print("   GET /health - System health check")
    print("   GET /api/examples - Example addresses")
    print("=" * 50)

    # Run the app
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True,
        use_reloader=True
    )
