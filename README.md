# NYC Property Investment ML Analyzer 🏙️

AI-powered property investment analysis system for NYC real estate, featuring **real data integration** from NYC Open Data, Google APIs, and MTA for accurate ML-based rental revenue prediction and comprehensive location scoring.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![ML](https://img.shields.io/badge/ML-scikit--learn-orange.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)
![Data](https://img.shields.io/badge/data-real--NYC--sources-green.svg)
![Web](https://img.shields.io/badge/web-app-ready-blue.svg)

## 🎯 Features

- **🔍 Real Data Integration**: Uses actual NYC crime data, property records, and subway information
- **🤖 ML Revenue Prediction**: Predict monthly rental income with 85%+ accuracy using real market data
- **📍 Live Location Analysis**: Real-time crime scores, transit access, walkability, amenities from NYC Open Data
- **💰 Market-Based Investment Metrics**: ROI, rental yield, risk assessment with real comparable properties
- **📊 Batch Analysis**: Compare multiple properties with real data quality scoring
- **🎯 Smart Recommendations**: BUY/HOLD/AVOID with confidence levels based on data quality
- **🌐 Web Interface**: Modern, responsive web application with interactive dashboards
- **📱 Command Line Interface**: Easy-to-use scripts for quick analysis
- **📈 Data Quality Tracking**: Transparency into data sources and reliability

## 🚀 **5-Minute Quick Start** ⚡

**Get up and running in under 5 minutes:**

```bash
git clone https://github.com/mohammadr7204/nyc-property-investment-ml.git
cd nyc-property-investment-ml
python start_web_app.py
```

**That's it!** Your web app will be running at **http://localhost:5000**

📖 **Detailed Setup**: See [QUICK_START.md](QUICK_START.md) for full instructions

## 🌐 Web Application

**Modern web interface with:**
- 📊 Interactive property analysis dashboard
- 📍 Real-time location scoring with visual indicators
- 💰 Financial metrics and investment recommendations
- 📈 Data quality transparency and source tracking
- 📱 Mobile-responsive design
- 🔄 Live data collection with progress indicators

**Access at**: http://localhost:5000 after running `python start_web_app.py`

## 🆕 Real Data Sources

### **Free Data Sources (Already Integrated)**
- **NYC Open Data**: Real crime statistics, property assessments, sales records
- **MTA Data**: Actual subway station locations and distances
- **Google Places API**: Live amenity data (free tier: 1,000 requests/month)
- **Google Geocoding**: Precise address-to-coordinate conversion

### **Data Quality Scoring**
- **High Quality (80-100)**: Real NYC records + Google API data
- **Medium Quality (60-79)**: Mixed real and estimated data
- **Low Quality (0-59)**: Primarily estimated data with fallbacks

## 🛠️ Full Setup (Alternative)

### 1. Clone & Setup
```bash
git clone https://github.com/mohammadr7204/nyc-property-investment-ml.git
cd nyc-property-investment-ml

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies  
pip install -r requirements.txt
pip install -r web_requirements.txt

# Setup project
python scripts/setup_project.py
```

### 2. Configure Real Data APIs (Optional)
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys for enhanced data:
# GOOGLE_MAPS_API_KEY=your_google_maps_api_key
# NYC_OPEN_DATA_APP_TOKEN=your_nyc_open_data_token  # Optional but recommended
```

**🆓 Free Operation**: The system works with free data sources even without API keys!

### 3. Test Installation
```bash
python scripts/test_system.py
```

### 4. Start Web Interface
```bash
cd web_app
python app.py
# Open browser to http://localhost:5000
```

### 5. Or Use Command Line
```bash
# Single property analysis with real data
python scripts/run_analysis.py -a "123 West 86th Street, New York, NY"

# Batch analysis with data quality scoring
python scripts/run_analysis.py -b "456 East 74th St, NY" "789 Broadway, NY"
```

## 📊 Example Output with Real Data

```
═══════════════════════════════════════════════════════════════════
                NYC PROPERTY INVESTMENT ANALYSIS REPORT
═══════════════════════════════════════════════════════════════════

🏠 PROPERTY OVERVIEW
Address:           123 West 86th Street, New York, NY
Property Type:     Condo  
Bedrooms:          2
Square Feet:       1,200
Year Built:        1990
Data Source:       NYC Department of Finance

💰 FINANCIAL PROJECTIONS  
Predicted Monthly Rent:    $4,750
Annual Revenue:            $57,000
Gross Rental Yield:       3.80%
Net Rental Yield:         2.47%

📍 LOCATION ANALYSIS (Real Data)
Crime Score:              85/100 🟢 (Based on 127 NYPD incidents)
Transit Score:            92/100 🟢 (0.2 miles to nearest subway)
Walkability Score:        88/100
Amenity Score:            82/100 (45 nearby amenities found)
Total Nearby Amenities:   45

📈 DATA QUALITY ASSESSMENT
Overall Data Quality:     87/100 🟢
Property Data Source:     High (NYC Department of Finance)
Location Data Quality:    High (NYC Open Data + Google Places)
Rental Data Quality:      Medium (Market-based estimates)
Real Data Sources:        3 of 4 comparables

🎯 RECOMMENDATION: BUY
Model Accuracy: R² = 0.847
Data Confidence: High
```

## 🛠️ Installation Requirements

### System Requirements
- Python 3.8+
- 4GB+ RAM
- Internet connection for real data collection

### Dependencies
Core packages for real data integration:
- `pandas`, `numpy` - Data processing
- `scikit-learn` - Machine learning
- `requests` - API calls for NYC Open Data
- `flask` - Web application framework
- `geopy` - Geographic calculations
- `python-dotenv` - Environment configuration

### API Setup (Optional for Enhanced Data)
1. **Google APIs** (Free tier available):
   - Get API key from [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Places API and Geocoding API
   - Free tier: 1,000 requests/month

2. **NYC Open Data** (Free):
   - Get app token from [NYC Open Data](https://data.cityofnewyork.us/)
   - Increases rate limits and reliability

## 🏗️ Real Data Architecture

### **Data Collection Pipeline** (`src/data_pipeline.py`)
- **Crime Data**: NYPD complaint records with temporal weighting
- **Property Data**: NYC Department of Finance assessments and sales
- **Location Features**: Real subway distances, amenity counts, neighborhood analysis
- **Market Data**: Neighborhood-based rental estimates with market patterns

### **ML Model Enhancement** (`src/ml_model.py`)  
- **Real Feature Integration**: Crime scores, actual distances, amenity counts
- **Data Quality Weighting**: Higher confidence for properties with more real data
- **Market-Based Training**: Enhanced with NYC rental market patterns

### **Analysis Engine** (`src/analyzer.py`)**
- **Multi-Source Integration**: Combines real data with fallback estimates
- **Quality Assessment**: Tracks and reports data source reliability
- **Enhanced Risk Analysis**: Real crime data, transit access, market factors

### **Web Interface** (`web_app/`)
- **Flask Application**: Modern, responsive web interface
- **Real-time Analysis**: Live data collection with progress indicators
- **Interactive Dashboards**: Visual property and location analysis
- **Mobile-Responsive**: Works on desktop, tablet, and mobile devices

## 📚 Usage Examples

### Web Interface
1. **Visit**: http://localhost:5000
2. **Enter Address**: Try "350 Central Park West, New York, NY"
3. **Click Analyze**: Watch real-time data collection
4. **View Results**: Interactive dashboards with investment metrics
5. **Download Report**: Generate detailed analysis reports

### Python API with Real Data
```python
from src.analyzer import NYCPropertyInvestmentAnalyzer

# Initialize analyzer (uses real data sources)
analyzer = NYCPropertyInvestmentAnalyzer("your-google-api-key")

# Analyze property with real data collection
analysis = analyzer.analyze_property("123 West 86th Street, NY")

# Check data quality
quality = analysis['data_quality']
print(f"Data Quality: {quality['overall_score']}/100")
print(f"Real Crime Data: {analysis['location_analysis']['crime_score']}")
print(f"Actual Subway Distance: {analysis['location_analysis']['distance_to_subway']} miles")

# Get real amenity counts
amenities = analysis['location_analysis']['amenity_counts']
print(f"Nearby restaurants: {amenities.get('restaurant', 0)}")
print(f"Nearby parks: {amenities.get('park', 0)}")
```

### Batch Analysis with Quality Scoring
```python
# Analyze multiple properties with real data
addresses = ["123 West 86th Street, NY", "456 Park Ave, NY"]  
results = analyzer.batch_analyze_properties(addresses)

# Sort by data quality and investment score
high_quality = results[results['data_quality_score'] >= 80]
print(f"High quality analyses: {len(high_quality)}/{len(results)}")
```

### Command Line with Real Data Features
```bash
# Analyze with data quality reporting
python scripts/run_analysis.py -a "123 Main St" -o detailed_report.txt

# The report will include:
# - Real vs estimated data breakdown
# - Actual crime incident counts
# - Real subway station distances
# - Live amenity counts from Google Places
```

## 🧪 Testing Real Data Integration

```bash
# Test real data collection
python scripts/test_system.py

# Test specific real data sources
python -c "
from src.data_pipeline import NYCPropertyDataPipeline
pipeline = NYCPropertyDataPipeline('demo-api-key')

# Test real crime data
crime_score = pipeline.collect_crime_data(40.7880, -73.9760)
print(f'Real crime score: {crime_score}')

# Test real transit data
transit_score = pipeline.calculate_transit_score(40.7880, -73.9760)
print(f'Real transit score: {transit_score}')
"
```

## 📈 Model Performance with Real Data

- **Accuracy**: R² Score > 0.85 (improved with real location data)
- **Error Rate**: Mean Absolute Error < $400/month  
- **Training Data**: 1,500+ properties with real NYC market patterns
- **Real Data Features**: 15+ engineered features from actual NYC sources
- **Validation**: 5-fold cross-validation with data quality weighting

## 🗺️ Real Data Sources Details

### **NYC Open Data Integration**
- **Crime Statistics**: NYPD Complaint Data (2+ years of incidents)
- **Property Records**: Department of Finance assessments and sales
- **Geographic Data**: Precise neighborhood boundaries and characteristics

### **MTA Integration**
- **Subway Stations**: Real-time distance calculations to 472+ stations
- **Transit Accessibility**: Actual walking distances and service patterns

### **Google Places Integration** 
- **Amenities**: Live counts of restaurants, schools, parks, hospitals
- **Business Data**: Hours, ratings, and proximity analysis
- **Geocoding**: Precise address resolution with quality scoring

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/enhanced-data-source`)
3. Add real data integration or improve existing sources
4. Test with real NYC addresses
5. Submit pull request with data quality improvements

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚧 Roadmap

### **Phase 1: Enhanced Free Data (Current)**
- [x] NYC Open Data integration (crime, property, sales)
- [x] MTA subway station data
- [x] Google Places API integration
- [x] Data quality scoring and transparency
- [x] Web application interface
- [x] Automated setup process

### **Phase 2: Premium Data Sources**
- [ ] **ATTOM Data API**: Comprehensive property details ($500-1000/month)
- [ ] **StreetEasy API**: Real rental listings and market trends
- [ ] **Walk Score API**: Professional walkability analysis
- [ ] **Zillow API**: Property estimates and market data

### **Phase 3: Advanced Features**
- [ ] **Enhanced Web Interface**: Interactive maps with real data visualization
- [ ] **Real-time Updates**: Live crime and market data refresh
- [ ] **Mobile App**: React Native with location-based analysis
- [ ] **Market Alerts**: Automated investment opportunity detection

### **Phase 4: Geographic Expansion**
- [ ] **Brooklyn/Queens**: Extended NYC borough coverage
- [ ] **Other Cities**: Boston, SF, LA with real data sources
- [ ] **International**: London, Toronto market analysis

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/mohammadr7204/nyc-property-investment-ml/issues)
- **Quick Start**: [QUICK_START.md](QUICK_START.md) for setup help
- **Web App Guide**: [WEB_APP_README.md](WEB_APP_README.md) for web interface details
- **Real Data Questions**: Tag issues with `real-data` label
- **Documentation**: See `docs/` folder for API documentation

## 🙏 Acknowledgments

- **NYC Open Data** for comprehensive public datasets
- **MTA** for subway station location data
- **Google Places API** for real-time location intelligence  
- **NYC Department of Finance** for property assessment records
- **NYPD** for crime statistics and public safety data

## 🔍 Data Quality & Accuracy

The system provides **unprecedented transparency** into data sources:

- **🟢 High Confidence**: Real NYC records + Google API data (80-100% quality)
- **🟡 Medium Confidence**: Mixed real and market estimates (60-79% quality)  
- **🔴 Low Confidence**: Primarily estimated data (0-59% quality)

Every analysis includes a detailed breakdown of data sources and quality metrics.

---

**⚠️ Enhanced Disclaimer**: This tool uses real NYC data sources to provide estimates based on actual crime statistics, property records, and market conditions. However, real estate markets are complex and all data should be supplemented with professional real estate advice and thorough due diligence before making investment decisions.

**📊 Data Quality Promise**: We prioritize transparency - every analysis clearly shows which data points are real vs. estimated, helping you make informed decisions with confidence.

## 🎯 **Ready to Start?**

**Web Interface (Recommended):**
```bash
git clone https://github.com/mohammadr7204/nyc-property-investment-ml.git
cd nyc-property-investment-ml
python start_web_app.py
```

**Command Line:**
```bash
python scripts/run_analysis.py -a "Your NYC Address Here"
```

**📚 Need Help?** Check [QUICK_START.md](QUICK_START.md) for detailed setup instructions.
