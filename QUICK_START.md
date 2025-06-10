# NYC Property Investment ML - Quick Start Guide 🚀

## 5-Minute Setup & Launch

This guide gets you running the complete system in under 5 minutes.

### Option 1: Automated Setup (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/mohammadr7204/nyc-property-investment-ml.git
cd nyc-property-investment-ml

# 2. Run the auto-setup script
python start_web_app.py
```

**That's it!** The script will:
- ✅ Check system requirements
- ✅ Install missing packages  
- ✅ Initialize the database and ML model
- ✅ Start the web application
- ✅ Open your browser to http://localhost:5000

### Option 2: Manual Setup

If you prefer manual control:

```bash
# 1. Clone and setup environment
git clone https://github.com/mohammadr7204/nyc-property-investment-ml.git
cd nyc-property-investment-ml
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
pip install -r web_requirements.txt

# 3. Initialize system
python scripts/setup_project.py

# 4. Start web app
cd web_app
python app.py

# 5. Open browser to http://localhost:5000
```

### System Requirements

- **Python 3.8+** (Required)
- **4GB+ RAM** (Recommended)
- **Internet connection** (For real NYC data)

### First Analysis

1. **Enter an address**: Try "350 Central Park West, New York, NY"
2. **Click Analyze**: Watch real-time data collection
3. **View results**: Investment metrics, location scores, recommendations
4. **Download report**: Generate detailed analysis report

### Data Sources

The system uses **real data** by default:
- **🆓 Free**: NYC Open Data (crime, property records, subway stations)
- **🔑 Enhanced**: Google Places API (get free key for better amenity data)

### API Configuration (Optional)

For enhanced accuracy, add Google API keys:

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add:
GOOGLE_MAPS_API_KEY=your_google_api_key_here
```

Get free API key at [Google Cloud Console](https://console.cloud.google.com/)

### Troubleshooting

**Common Issues:**

1. **Python Version**: Must be 3.8+
   ```bash
   python --version  # Should show 3.8 or higher
   ```

2. **Missing Packages**: 
   ```bash
   pip install -r requirements.txt -r web_requirements.txt
   ```

3. **Port 5000 in use**:
   ```bash
   # Kill process on port 5000
   lsof -ti:5000 | xargs kill -9  # Mac/Linux
   netstat -ano | findstr :5000   # Windows
   ```

4. **Database errors**: 
   ```bash
   python scripts/setup_project.py  # Reinitialize
   ```

### Command Line Usage

Analyze properties from command line:

```bash
# Single property
python scripts/run_analysis.py -a "123 West 86th Street, New York, NY"

# Multiple properties  
python scripts/run_analysis.py -b "Address 1" "Address 2" "Address 3"

# Test system
python scripts/test_system.py
```

### What You Get

- **🤖 ML Revenue Prediction**: 85%+ accuracy using real market data
- **📍 Location Analysis**: Real crime scores, transit access, amenities  
- **💰 Investment Metrics**: ROI, cash flow, rental yield calculations
- **🎯 Smart Recommendations**: BUY/HOLD/AVOID with confidence levels
- **📊 Data Quality Scoring**: Transparency into data sources
- **📱 Web Interface**: Modern, responsive design
- **🔧 CLI Tools**: Command-line analysis tools

### File Structure

```
nyc-property-investment-ml/
├── src/                    # Core ML system
├── web_app/               # Flask web application  
├── scripts/               # CLI utilities
├── start_web_app.py       # Auto-setup script
└── README.md              # Full documentation
```

### Next Steps

1. **Analyze properties**: Use the web interface or CLI tools
2. **Add Google API key**: For enhanced location data (optional)
3. **Explore docs/**: Detailed API documentation
4. **Run tests**: `python scripts/test_system.py`

### Support

- **Issues**: [GitHub Issues](https://github.com/mohammadr7204/nyc-property-investment-ml/issues)
- **Health Check**: Visit http://localhost:5000/health
- **Full Documentation**: See README.md

---

**🎯 Ready to start? Just run:**
```bash
git clone https://github.com/mohammadr7204/nyc-property-investment-ml.git
cd nyc-property-investment-ml
python start_web_app.py
```

Your NYC property analyzer will be running at **http://localhost:5000** in under 5 minutes! 🏙️✨
