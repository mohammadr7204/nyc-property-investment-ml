# NYC Property Investment ML - API Documentation

This document provides detailed API documentation for the NYC Property Investment ML system.

## 🏗️ Core Components

### NYCPropertyInvestmentAnalyzer

Main analyzer class that orchestrates property analysis.

```python
from src.analyzer import NYCPropertyInvestmentAnalyzer

# Initialize
analyzer = NYCPropertyInvestmentAnalyzer("your-google-api-key")

# Analyze single property
analysis = analyzer.analyze_property("123 West 86th Street, New York, NY")

# Batch analysis
addresses = ["Address 1", "Address 2", "Address 3"]
results = analyzer.batch_analyze_properties(addresses)
```

#### Methods

##### `analyze_property(address: str) -> Dict`

Analyzes a single property and returns comprehensive investment analysis.

**Parameters:**
- `address` (str): Property address to analyze

**Returns:**
- `Dict`: Complete analysis including:
  - `property_details`: Basic property information
  - `location_analysis`: Location scores and features
  - `rental_comparables`: Nearby rental properties
  - `revenue_prediction`: ML-based revenue prediction
  - `financial_metrics`: Investment metrics and yields
  - `risk_assessment`: Risk factors and overall risk level
  - `investment_recommendation`: Buy/Hold/Avoid recommendation

**Example:**
```python
analysis = analyzer.analyze_property("123 West 86th Street, NY")
print(f"Predicted rent: ${analysis['revenue_prediction']['predicted_monthly_rent']:,}")
print(f"Recommendation: {analysis['investment_recommendation']['recommendation']}")
```

##### `batch_analyze_properties(addresses: List[str]) -> pd.DataFrame`

Analyzes multiple properties and returns comparison DataFrame.

**Parameters:**
- `addresses` (List[str]): List of property addresses

**Returns:**
- `pd.DataFrame`: Comparison table with key metrics

**Example:**
```python
addresses = ["123 Main St, NY", "456 Park Ave, NY"]
results = analyzer.batch_analyze_properties(addresses)
print(results.sort_values('gross_yield', ascending=False))
```

##### `generate_detailed_report(analysis: Dict) -> str`

Generates a formatted investment report.

**Parameters:**
- `analysis` (Dict): Analysis result from `analyze_property()`

**Returns:**
- `str`: Formatted text report

##### `rank_investment_opportunities(df: pd.DataFrame) -> pd.DataFrame`

Ranks properties by investment attractiveness.

**Parameters:**
- `df` (pd.DataFrame): Results from `batch_analyze_properties()`

**Returns:**
- `pd.DataFrame`: Ranked properties with investment scores

### NYCRevenuePredictor

Machine learning model for predicting rental revenue.

```python
from src.ml_model import NYCRevenuePredictor

predictor = NYCRevenuePredictor()

# Train model
df = predictor.generate_synthetic_training_data(1000)
X, y = predictor.prepare_features(df)
metrics = predictor.train_model(X, y)

# Make prediction
features = {
    'bedrooms': 2,
    'bathrooms': 2.0,
    'sqft': 1000,
    # ... other features
}
prediction = predictor.predict_revenue(features)
```

#### Methods

##### `generate_synthetic_training_data(n_samples: int) -> pd.DataFrame`

Generates synthetic training data based on NYC market patterns.

**Parameters:**
- `n_samples` (int): Number of samples to generate

**Returns:**
- `pd.DataFrame`: Synthetic property and rental data

##### `train_model(X: pd.DataFrame, y: pd.Series) -> Dict`

Trains ML models and selects the best performer.

**Parameters:**
- `X` (pd.DataFrame): Feature matrix
- `y` (pd.Series): Target variable (monthly rent)

**Returns:**
- `Dict`: Training results and metrics

##### `predict_revenue(features: Dict) -> Dict`

Predicts monthly rental revenue for a property.

**Parameters:**
- `features` (Dict): Property and location features

**Returns:**
- `Dict`: Prediction results including:
  - `predicted_monthly_rent`: Main prediction
  - `confidence_interval`: Prediction range
  - `annual_revenue`: Yearly revenue estimate
  - `prediction_confidence`: High/Medium/Low confidence

### NYCPropertyDataPipeline

Data collection and processing pipeline.

```python
from src.data_pipeline import NYCPropertyDataPipeline

pipeline = NYCPropertyDataPipeline("your-google-api-key")

# Collect location features
crime_score = pipeline.collect_crime_data(40.7880, -73.9760)
amenities = pipeline.get_google_places_amenities(40.7880, -73.9760)
transit_score = pipeline.calculate_transit_score(40.7880, -73.9760)
```

#### Methods

##### `collect_crime_data(latitude: float, longitude: float) -> float`

Collects crime data for a location.

**Parameters:**
- `latitude` (float): Property latitude
- `longitude` (float): Property longitude

**Returns:**
- `float`: Crime score (0-100, higher = safer)

##### `get_google_places_amenities(latitude: float, longitude: float) -> Dict`

Collects nearby amenities using Google Places API.

**Parameters:**
- `latitude` (float): Property latitude
- `longitude` (float): Property longitude

**Returns:**
- `Dict`: Amenity score and counts

##### `calculate_transit_score(latitude: float, longitude: float) -> float`

Calculates transit accessibility score.

**Parameters:**
- `latitude` (float): Property latitude
- `longitude` (float): Property longitude

**Returns:**
- `float`: Transit score (0-100, higher = better access)

## 📊 Data Structures

### Analysis Result Structure

```python
analysis = {
    'property_details': {
        'address': str,
        'latitude': float,
        'longitude': float,
        'property_type': str,  # 'Condo', 'Co-op', 'Rental'
        'bedrooms': int,
        'bathrooms': float,
        'sqft': int,
        'year_built': int,
        'last_sale_price': float
    },
    'location_analysis': {
        'crime_score': float,      # 0-100
        'walkability_score': float, # 0-100
        'transit_score': float,    # 0-100
        'amenity_score': float,    # 0-100
        'distance_to_subway': float,     # miles
        'distance_to_manhattan': float,  # miles
        'neighborhood': str
    },
    'revenue_prediction': {
        'predicted_monthly_rent': float,
        'confidence_interval': Tuple[float, float],
        'annual_revenue': float,
        'model_r2': float,
        'prediction_confidence': str  # 'High', 'Medium', 'Low'
    },
    'financial_metrics': {
        'gross_rental_yield': float,    # Percentage
        'net_rental_yield': float,     # Percentage
        'estimated_annual_expenses': float,
        'net_annual_revenue': float,
        'monthly_cash_flow': float,
        'rent_vs_comparables': float,  # Percentage difference
        'expense_ratio': float         # Percentage
    },
    'risk_assessment': {
        'risk_factors': List[str],
        'overall_risk': str,  # 'Low', 'Medium', 'High'
        'risk_score': int
    },
    'investment_recommendation': {
        'recommendation': str,  # 'STRONG BUY', 'BUY', 'HOLD', 'WEAK HOLD', 'AVOID'
        'confidence': str,      # 'High', 'Medium-High', 'Medium', 'Low-Medium'
        'recommendation_score': int
    }
}
```

### Feature Dictionary Structure

```python
features = {
    # Required features
    'bedrooms': int,
    'bathrooms': float,
    'sqft': int,
    'year_built': int,
    'last_sale_price': float,
    
    # Optional features (defaults provided)
    'property_type': str,          # 'Condo', 'Co-op', 'Rental'
    'crime_score': float,          # 0-100
    'walkability_score': float,    # 0-100
    'transit_score': float,        # 0-100
    'amenity_score': float,        # 0-100
    'distance_to_subway': float,   # miles
    'distance_to_manhattan': float, # miles
    'neighborhood': str
}
```

## 🔧 Configuration

### Environment Variables

- `GOOGLE_MAPS_API_KEY`: Google Maps API key for location data
- `DATABASE_PATH`: Path to SQLite database file
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FILE`: Path to log file

### API Key Setup

1. Get Google Maps API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable these APIs:
   - Places API
   - Geocoding API
   - Maps JavaScript API
3. Set in environment or `.env` file

## 🎯 Usage Examples

### Basic Property Analysis

```python
from src.analyzer import NYCPropertyInvestmentAnalyzer

# Initialize with API key
analyzer = NYCPropertyInvestmentAnalyzer("your-api-key")

# Analyze property
address = "123 West 86th Street, New York, NY"
analysis = analyzer.analyze_property(address)

# Extract key metrics
rent = analysis['revenue_prediction']['predicted_monthly_rent']
yield_rate = analysis['financial_metrics']['gross_rental_yield']
recommendation = analysis['investment_recommendation']['recommendation']

print(f"Predicted Rent: ${rent:,}/month")
print(f"Gross Yield: {yield_rate:.1f}%")
print(f"Recommendation: {recommendation}")
```

### Batch Analysis and Ranking

```python
# Analyze multiple properties
addresses = [
    "123 West 86th Street, New York, NY",
    "456 East 74th Street, New York, NY", 
    "789 Broadway, New York, NY"
]

# Batch analysis
results = analyzer.batch_analyze_properties(addresses)

# Rank by investment potential
ranked = analyzer.rank_investment_opportunities(results)

# Display top opportunities
print("Top Investment Opportunities:")
for _, row in ranked.head().iterrows():
    print(f"{row['address']}: {row['gross_yield']:.1f}% yield, {row['recommendation']}")
```

### Custom ML Model Training

```python
from src.ml_model import NYCRevenuePredictor

# Initialize predictor
predictor = NYCRevenuePredictor()

# Generate training data
df = predictor.generate_synthetic_training_data(2000)

# Prepare features
X, y = predictor.prepare_features(df)

# Train model
metrics = predictor.train_model(X, y)
print(f"Model R² Score: {metrics['r2']:.3f}")

# Save model
predictor.save_model("models/custom_model.pkl")
```

### Data Pipeline Usage

```python
from src.data_pipeline import NYCPropertyDataPipeline

# Initialize pipeline
pipeline = NYCPropertyDataPipeline("your-api-key")

# Collect data for specific location
lat, lng = 40.7880, -73.9760  # Upper West Side

# Get location scores
crime = pipeline.collect_crime_data(lat, lng)
amenities = pipeline.get_google_places_amenities(lat, lng)
transit = pipeline.calculate_transit_score(lat, lng)

print(f"Crime Score: {crime}/100")
print(f"Amenity Score: {amenities['score']}/100")
print(f"Transit Score: {transit}/100")
```

## ⚠️ Error Handling

### Common Exceptions

- `ValueError`: Invalid input parameters
- `requests.RequestException`: API call failures
- `sqlite3.Error`: Database errors
- `KeyError`: Missing required features

### Best Practices

```python
try:
    analysis = analyzer.analyze_property(address)
except ValueError as e:
    print(f"Invalid input: {e}")
except requests.RequestException as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🔍 Performance Considerations

### API Rate Limits

- Google Places API: 100,000 requests/day (free tier)
- NYC Open Data: No strict limits, but use reasonable delays
- Implement exponential backoff for failed requests

### Memory Usage

- Large batch analyses may require significant memory
- Consider processing in chunks for >100 properties
- Monitor memory usage with `psutil` for large datasets

### Caching

- Location features are cached in SQLite database
- API responses can be cached to reduce calls
- Model predictions can be cached for repeated queries

## 📈 Model Performance

### Current Metrics

- **R² Score**: >0.85 on synthetic data
- **RMSE**: <$400/month average error
- **Training Time**: ~30 seconds for 1500 samples
- **Prediction Time**: <100ms per property

### Improving Performance

1. **More Training Data**: Collect real rental data
2. **Feature Engineering**: Add more location features
3. **Model Tuning**: Hyperparameter optimization
4. **Ensemble Methods**: Combine multiple models

For detailed examples and tutorials, see the `notebooks/` directory.
