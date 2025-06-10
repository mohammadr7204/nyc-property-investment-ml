#!/usr/bin/env python3
"""
Project setup script - Run this first!
Initializes database, checks dependencies, and sets up the project structure.
"""

import os
import sqlite3
import logging
from pathlib import Path
import sys

def setup_logging():
    """Setup logging configuration"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/setup.log'),
            logging.StreamHandler()
        ]
    )

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'pandas', 'numpy', 'scikit-learn', 'requests', 
        'matplotlib', 'geopy', 'joblib'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            logging.info(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            logging.error(f"❌ {package} is missing")
    
    if missing_packages:
        logging.error("Install missing packages with: pip install -r requirements.txt")
        return False
    
    return True

def setup_database():
    """Initialize the SQLite database"""
    db_path = Path('data/nyc_property_data.db')
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    
    # Create tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT UNIQUE,
            latitude REAL,
            longitude REAL,
            property_type TEXT,
            bedrooms INTEGER,
            bathrooms REAL,
            sqft INTEGER,
            year_built INTEGER,
            last_sale_price REAL,
            last_sale_date TEXT,
            zestimate REAL,
            rent_estimate REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS location_features (
            property_id INTEGER,
            crime_score REAL,
            walkability_score REAL,
            transit_score REAL,
            amenity_score REAL,
            distance_to_subway REAL,
            distance_to_manhattan REAL,
            neighborhood TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES properties (id)
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rental_comps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER,
            comp_address TEXT,
            comp_latitude REAL,
            comp_longitude REAL,
            monthly_rent REAL,
            bedrooms INTEGER,
            bathrooms REAL,
            sqft INTEGER,
            distance_miles REAL,
            listing_source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES properties (id)
        )
    """)
    
    conn.commit()
    conn.close()
    
    logging.info("✅ Database initialized successfully")

def check_api_keys():
    """Check if API keys are configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        google_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not google_key or google_key == 'your_google_maps_api_key_here':
            logging.warning("⚠️  Google Maps API key not configured (using demo mode)")
            logging.info("Get your key at: https://console.cloud.google.com/")
            return False
        
        logging.info("✅ API keys configured")
        return True
    except ImportError:
        logging.info("python-dotenv not installed, skipping API key check")
        return False

def create_directory_structure():
    """Create necessary directories"""
    dirs_to_create = [
        'data/raw', 'data/processed', 'models/saved_models',
        'logs', 'notebooks', 'tests', 'docs'
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        # Add .gitkeep files to preserve empty directories
        gitkeep_path = Path(dir_path) / '.gitkeep'
        if not gitkeep_path.exists():
            gitkeep_path.write_text('# Keep this directory in git\n')
    
    logging.info("✅ Directory structure created")

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    env_path = Path('.env')
    env_example_path = Path('.env.example')
    
    if not env_path.exists() and env_example_path.exists():
        env_path.write_text(env_example_path.read_text())
        logging.info("✅ Created .env file from .env.example")
        logging.info("📝 Edit .env file to add your API keys")
    elif not env_path.exists():
        # Create basic .env file
        env_content = """
# Google Maps API Key (get from https://console.cloud.google.com/)
GOOGLE_MAPS_API_KEY=demo-api-key

# Database Configuration
DATABASE_PATH=data/nyc_property_data.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/pipeline.log
        """.strip()
        
        env_path.write_text(env_content)
        logging.info("✅ Created basic .env file")

def main():
    """Main setup function"""
    setup_logging()
    logging.info("🚀 Setting up NYC Property Investment System...")
    
    try:
        # Check Python version
        if sys.version_info < (3, 8):
            logging.error("❌ Python 3.8+ required")
            return False
        
        # Check dependencies
        if not check_dependencies():
            logging.error("❌ Missing dependencies. Please install requirements.txt")
            return False
        
        # Create directory structure
        create_directory_structure()
        
        # Create .env file if needed
        create_env_file()
        
        # Setup database
        setup_database()
        
        # Check API keys
        api_configured = check_api_keys()
        
        logging.info("✅ Project setup complete!")
        
        print("\n" + "="*60)
        print("🎉 NYC Property Investment ML - Setup Complete!")
        print("="*60)
        
        if not api_configured:
            print("\n📝 Next steps:")
            print("1. Get Google Maps API key (optional for demo)")
            print("2. Update .env file with your API key")
            print("3. Run: python scripts/test_system.py")
        else:
            print("\n✅ Ready to use! Run: python scripts/test_system.py")
        
        print("\n📚 Quick commands:")
        print("  python scripts/test_system.py        # Test the system")
        print("  python scripts/run_analysis.py -a 'address'  # Analyze property")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
