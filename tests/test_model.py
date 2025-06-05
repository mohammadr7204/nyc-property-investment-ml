"""
Unit tests for the ML model module
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ml_model import NYCRevenuePredictor
from tests import TEST_CONFIG

class TestNYCRevenuePredictor:
    """Test cases for the ML revenue predictor"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.predictor = NYCRevenuePredictor()
    
    def test_predictor_initialization(self):
        """Test predictor initializes correctly"""
        assert self.predictor.model is None
        assert hasattr(self.predictor, 'scaler')
        assert hasattr(self.predictor, 'label_encoders')
        assert isinstance(self.predictor.label_encoders, dict)
    
    def test_generate_synthetic_training_data(self):
        """Test synthetic data generation"""
        df = self.predictor.generate_synthetic_training_data(100)
        
        # Check data structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 100
        
        # Check required columns
        required_cols = [
            'bedrooms', 'bathrooms', 'sqft', 'year_built', 'property_type',
            'crime_score', 'transit_score', 'amenity_score', 'neighborhood',
            'last_sale_price', 'monthly_rent'
        ]
        
        for col in required_cols:
            assert col in df.columns
        
        # Check data ranges
        assert df['bedrooms'].min() >= 1
        assert df['bedrooms'].max() <= 4
        assert df['monthly_rent'].min() >= 1800
        assert df['monthly_rent'].max() <= 25000
        assert df['crime_score'].min() >= 30
        assert df['crime_score'].max() <= 100
    
    def test_prepare_features(self):
        """Test feature preparation"""
        # Create test data
        df = self.predictor.generate_synthetic_training_data(50)
        
        X, y = self.predictor.prepare_features(df)
        
        # Check outputs
        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)
        assert len(X) == len(y) == 50
        
        # Check engineered features are created
        assert 'property_age' in X.columns
        assert 'price_per_sqft' in X.columns
        assert 'location_score' in X.columns
        
        # Check no missing values in key features
        assert not X['property_age'].isna().any()
        assert not X['price_per_sqft'].isna().any()
    
    @pytest.mark.slow
    def test_train_model(self):
        """Test model training"""
        # Generate training data
        df = self.predictor.generate_synthetic_training_data(500)
        X, y = self.predictor.prepare_features(df)
        
        # Train model
        results = self.predictor.train_model(X, y)
        
        # Check model was trained
        assert self.predictor.model is not None
        assert isinstance(results, dict)
        
        # Check metrics
        assert 'r2' in self.predictor.model_metrics
        assert 'rmse' in self.predictor.model_metrics
        assert 'mae' in self.predictor.model_metrics
        
        # Check reasonable performance
        assert self.predictor.model_metrics['r2'] > 0.7  # R² should be > 0.7
        assert self.predictor.model_metrics['rmse'] < 2000  # RMSE should be < $2000
    
    def test_predict_revenue(self):
        """Test revenue prediction"""
        # Train a simple model first
        df = self.predictor.generate_synthetic_training_data(200)
        X, y = self.predictor.prepare_features(df)
        self.predictor.train_model(X, y)
        
        # Test prediction
        test_features = {
            'bedrooms': 2,
            'bathrooms': 2.0,
            'sqft': 1000,
            'year_built': 1990,
            'property_type': 'Condo',
            'crime_score': 85,
            'transit_score': 90,
            'amenity_score': 75,
            'neighborhood': 'Upper West Side',
            'last_sale_price': 1500000,
            'walkability_score': 88,
            'distance_to_subway': 0.2,
            'distance_to_manhattan': 2.5
        }
        
        prediction = self.predictor.predict_revenue(test_features)
        
        # Check prediction structure
        required_keys = [
            'predicted_monthly_rent', 'confidence_interval', 'annual_revenue',
            'model_r2', 'prediction_confidence'
        ]
        
        for key in required_keys:
            assert key in prediction
        
        # Check prediction reasonableness
        monthly_rent = prediction['predicted_monthly_rent']
        assert 2000 <= monthly_rent <= 15000  # Reasonable NYC rent range
        
        # Check confidence interval
        ci_low, ci_high = prediction['confidence_interval']
        assert ci_low < monthly_rent < ci_high
    
    def test_validate_features(self):
        """Test feature validation"""
        # Test valid features
        valid_features = {
            'bedrooms': 2,
            'bathrooms': 2.0,
            'sqft': 1000,
            'year_built': 1990,
            'last_sale_price': 1500000
        }
        
        cleaned = self.predictor.validate_features(valid_features)
        assert 'bedrooms' in cleaned
        assert 'property_type' in cleaned  # Should add default
        
        # Test missing required feature
        invalid_features = {
            'bedrooms': 2,
            # missing required fields
        }
        
        with pytest.raises(ValueError):
            self.predictor.validate_features(invalid_features)
    
    def test_realistic_rent_calculation(self):
        """Test the realistic rent calculation logic"""
        # Test basic rent calculation components
        bedrooms = np.array([1, 2, 3])
        sqft = np.array([650, 950, 1300])
        year_built = np.array([1990, 2000, 2010])
        crime_score = np.array([75, 85, 95])
        transit_score = np.array([80, 90, 95])
        amenity_score = np.array([70, 80, 90])
        neighborhoods = np.array(['East Village', 'Chelsea', 'SoHo'])
        sale_price = np.array([1000000, 1500000, 2000000])
        
        rents = self.predictor._calculate_realistic_rent(
            bedrooms, sqft, year_built, crime_score, transit_score,
            amenity_score, neighborhoods, sale_price
        )
        
        # Check outputs
        assert len(rents) == 3
        assert all(isinstance(rent, (int, np.integer)) for rent in rents)
        assert all(1800 <= rent <= 25000 for rent in rents)
        
        # More bedrooms should generally mean higher rent
        # (though other factors can override this)
        assert rents[2] >= rents[0]  # 3BR >= 1BR
    
    def test_feature_importance(self):
        """Test feature importance extraction"""
        # Train model first
        df = self.predictor.generate_synthetic_training_data(200)
        X, y = self.predictor.prepare_features(df)
        self.predictor.train_model(X, y)
        
        # Get feature importance
        importance = self.predictor.get_feature_importance()
        
        if not importance.empty:
            assert 'feature' in importance.columns
            assert 'importance' in importance.columns
            assert len(importance) > 0
            assert all(importance['importance'] >= 0)
