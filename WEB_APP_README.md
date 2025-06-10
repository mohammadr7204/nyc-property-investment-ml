# NYC Property Investment ML - Web Application 🏙️

A sleek, modern web interface for the NYC Property Investment ML system. Get AI-powered property investment insights through an intuitive web dashboard.

![Web App Preview](https://img.shields.io/badge/Status-Ready%20to%20Use-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey)

## 🚀 Quick Start (5 Minutes)

### 1. **Auto Setup (Recommended)**
```bash
# Run the automated setup script
python start_web_app.py
```
This will automatically:
- ✅ Check system requirements
- ✅ Install missing packages
- ✅ Create necessary directories
- ✅ Initialize the database
- ✅ Start the web server
- ✅ Open your browser to http://localhost:5000

### 2. **Manual Setup**
If you prefer manual setup:

```bash
# Install web app requirements
pip install -r web_requirements.txt

# Copy web app files to web_app/ directory
mkdir -p web_app/templates web_app/static/css web_app/static/js

# Copy the provided files:
# - app.py → web_app/app.py
# - templates/*.html → web_app/templates/
# - static/css/style.css → web_app/static/css/
# - static/js/main.js → web_app/static/js/

# Setup environment
cp .env.example .env

# Initialize the system
python scripts/setup_project.py

# Start the web server
cd web_app
python app.py
```

## 📁 File Structure

```
your-project/
├── web_app/                    # Web application files
│   ├── app.py                  # Main Flask application
│   ├── templates/              # HTML templates
│   │   ├── base.html          # Base template
│   │   ├── index.html         # Main page
│   │   └── error.html         # Error pages
│   └── static/                # Static assets
│       ├── css/
│       │   └── style.css      # Custom styles
│       └── js/
│           └── main.js        # JavaScript functions
├── src/                       # Core ML system (existing)
├── requirements.txt           # Core system requirements
├── web_requirements.txt       # Web app requirements
└── start_web_app.py          # Auto-setup script
```

## 🌟 Features

### 🎨 **Modern UI/UX**
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Theme**: Professional color scheme
- **Smooth Animations**: Engaging user interactions
- **Real-time Feedback**: Progress indicators and notifications

### 🔍 **Property Analysis**
- **Smart Address Input**: Autocomplete for NYC addresses
- **Real-time Processing**: Live progress updates during analysis
- **Comprehensive Results**: Interactive charts and detailed metrics
- **Download Reports**: Generate PDF/text reports

### 📊 **Interactive Dashboard**
- **Location Radar Chart**: Crime, transit, walkability, amenity scores
- **Investment Breakdown**: Revenue vs expenses visualization
- **Risk Assessment**: Clear risk factor identification
- **Recommendation System**: BUY/HOLD/AVOID with confidence levels

### 🔧 **Developer Features**
- **RESTful API**: JSON endpoints for integration
- **Error Handling**: Graceful error recovery
- **Logging**: Comprehensive logging system
- **Health Checks**: System status monitoring

## 🎯 Usage Examples

### Basic Property Analysis
1. **Enter Address**: Type any NYC address (e.g., "350 Central Park West, New York, NY")
2. **Click Analyze**: Watch real-time progress as data is collected
3. **View Results**: Interactive dashboard with charts and metrics
4. **Download Report**: Generate detailed PDF/text reports

### API Usage (for developers)
```javascript
// Analyze a property via API
fetch('/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ address: '123 West 86th Street, New York, NY' })
})
.then(response => response.json())
.then(data => console.log(data.analysis));
```

## 🔑 Configuration

### Environment Variables (.env file)
```bash
# Google Maps API Key (optional - enhances accuracy)
GOOGLE_MAPS_API_KEY=your_actual_api_key_here

# NYC Open Data Token (optional - higher rate limits)
NYC_OPEN_DATA_APP_TOKEN=your_token_here

# Database Configuration
DATABASE_PATH=data/nyc_property_data.db

# Logging
LOG_LEVEL=INFO
```

### API Keys (Optional but Recommended)

#### Google Maps API Key
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **Places API** and **Geocoding API**
3. Create API key and add to `.env` file
4. **Free tier**: 1,000 requests/month

#### NYC Open Data Token
1. Visit [NYC Open Data](https://data.cityofnewyork.us/)
2. Sign up and get app token
3. Add to `.env` file for higher rate limits

## 🐛 Troubleshooting

### Common Issues

#### "Module not found" Error
```bash
# Make sure you're in the right directory
cd your-project-directory

# Install requirements
pip install -r web_requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

#### "Port 5000 already in use"
```bash
# Kill process using port 5000
# On Mac/Linux:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

#### "Database errors"
```bash
# Reinitialize database
python scripts/setup_project.py

# Check database file permissions
ls -la data/nyc_property_data.db
```

#### "API rate limiting"
- Add NYC Open Data token to `.env`
- Use Google API key for better performance
- Wait a few minutes between large batch analyses

### Getting Help

1. **Check Logs**: Look in `logs/` directory for detailed error messages
2. **Health Check**: Visit http://localhost:5000/health to check system status
3. **Browser Console**: Open developer tools to see JavaScript errors
4. **GitHub Issues**: Report bugs with system info and error messages

## 🚀 Deployment Options

### Local Development
```bash
python start_web_app.py
# Access at http://localhost:5000
```

### Production (Gunicorn)
```bash
pip install gunicorn
cd web_app
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
```bash
# Build image
docker build -t nyc-property-ml-web .

# Run container
docker run -p 5000:5000 nyc-property-ml-web
```

### Cloud Deployment
- **Heroku**: Ready for deployment with Procfile
- **AWS/GCP**: Works with any Python WSGI server
- **DigitalOcean**: One-click deployment ready

## 📈 Performance Tips

### For Better Analysis Speed
1. **Add Google API Key**: Faster geocoding and amenity data
2. **NYC Open Data Token**: Higher rate limits
3. **SSD Storage**: Faster database operations
4. **More RAM**: Better for ML model training

### For Web Performance
1. **Enable Gzip**: Compress responses
2. **Use CDN**: For static assets
3. **Browser Caching**: Set appropriate cache headers
4. **Database Indexing**: Optimize queries

## 🔒 Security Notes

### Production Deployment
- Change `SECRET_KEY` in production
- Use HTTPS (SSL/TLS certificates)
- Set `FLASK_ENV=production`
- Configure proper CORS settings
- Use environment variables for secrets

### API Security
- Implement rate limiting
- Add authentication if needed
- Validate all inputs
- Use CSRF protection

## 📊 System Requirements

### Minimum Requirements
- **Python**: 3.8+
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Network**: Internet connection for real data

### Recommended Requirements
- **Python**: 3.9+
- **RAM**: 8GB+
- **Storage**: 5GB+ (SSD preferred)
- **Network**: High-speed internet
- **Browser**: Chrome, Firefox, Safari, Edge (latest)

## 🎉 What's Next?

### Planned Features
- [ ] **Batch Analysis**: Compare multiple properties side-by-side
- [ ] **Investment Portfolio**: Track multiple investments
- [ ] **Market Trends**: Historical price and rent analysis
- [ ] **Neighborhood Reports**: Area-wide investment insights
- [ ] **Email Reports**: Scheduled analysis reports
- [ ] **Mobile App**: React Native companion app

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 🎯 Ready to Start?

**Just run one command:**
```bash
python start_web_app.py
```

Your NYC property analysis web app will be running at **http://localhost:5000** in under 30 seconds! 🚀

**Need help?** Check the troubleshooting section above or open an issue on GitHub.