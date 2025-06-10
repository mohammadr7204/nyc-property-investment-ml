"""
NYC Property Revenue Prediction Model
Machine learning models for predicting monthly rental revenue based on property and location features.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import logging
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class NYCRevenuePredictor:
    """
    Machine Learning model for predicting monthly rental revenue of NYC properties.
    Uses property characteristics, location features, and market data.
    """

    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_importance = None
        self.model_metrics = {}
        self.logger = logging.getLogger(__name__)

    def generate_synthetic_training_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """
        Generate synthetic training data for model development.
        Based on real NYC rental market patterns.

        Args:
            n_samples: Number of synthetic samples to generate

        Returns:
            DataFrame with synthetic property and rental data
        """
        np.random.seed(42)

        # Property characteristics
        bedrooms = np.random.choice([1, 2, 3, 4], n_samples, p=[0.3, 0.4, 0.2, 0.1])
        bathrooms = bedrooms + np.random.choice([0, 0.5, 1], n_samples, p=[0.3, 0.4, 0.3])
        bathrooms = np.clip(bathrooms, 1, 4)

        # Square footage based on bedrooms
        sqft_base = {1: 650, 2: 950, 3: 1300, 4: 1800}
        sqft = np.array([sqft_base[br] + np.random.normal(0, 150) for br in bedrooms])
        sqft = np.clip(sqft, 400, 3000)

        # Year built affects rent (newer = higher)
        year_built = np.random.normal(1980, 20, n_samples).astype(int)
        year_built = np.clip(year_built, 1950, 2024)

        # Property types
        property_types = np.random.choice(['Condo', 'Co-op', 'Rental'], n_samples, p=[0.4, 0.3, 0.3])

        # Location features (0-100 scales)
        crime_score = np.random.normal(75, 15, n_samples)
        crime_score = np.clip(crime_score, 30, 100)

        walkability_score = np.random.normal(78, 18, n_samples)
        walkability_score = np.clip(walkability_score, 40, 100)

        transit_score = np.random.normal(80, 15, n_samples)
        transit_score = np.clip(transit_score, 45, 100)

        amenity_score = np.random.normal(65, 20, n_samples)
        amenity_score = np.clip(amenity_score, 25, 100)

        # Distance features
        distance_to_subway = np.random.exponential(0.3, n_samples)
        distance_to_subway = np.clip(distance_to_subway, 0.05, 2.0)

        distance_to_manhattan = np.random.exponential(5, n_samples)
        distance_to_manhattan = np.clip(distance_to_manhattan, 0.5, 25)

        # Neighborhoods (major NYC areas)
        neighborhoods = np.random.choice([
            'Upper West Side', 'Upper East Side', 'Midtown', 'Chelsea', 'SoHo',
            'East Village', 'West Village', 'Tribeca', 'Financial District',
            'Williamsburg', 'Park Slope', 'Astoria', 'Long Island City',
            'DUMBO', 'Carroll Gardens', 'Red Hook'
        ], n_samples)

        # Last sale price (affects rental potential)
        last_sale_price = np.random.lognormal(14.2, 0.5, n_samples)
        last_sale_price = np.clip(last_sale_price, 400000, 8000000)

        # Calculate realistic rental revenue using NYC market patterns
        monthly_rent = self._calculate_realistic_rent(
            bedrooms, bathrooms, sqft, year_built, property_types,
            crime_score, walkability_score, transit_score, amenity_score,
            distance_to_subway, distance_to_manhattan, neighborhoods,
            last_sale_price
        )

        # Create DataFrame
        df = pd.DataFrame({
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'sqft': sqft.astype(int),
            'year_built': year_built,
            'property_type': property_types,
            'crime_score': crime_score,
            'walkability_score': walkability_score,
            'transit_score': transit_score,
            'amenity_score': amenity_score,
            'distance_to_subway': distance_to_subway,
            'distance_to_manhattan': distance_to_manhattan,
            'neighborhood': neighborhoods,
            'last_sale_price': last_sale_price.astype(int),
            'monthly_rent': monthly_rent
        })

        self.logger.info(f"Generated {n_samples} synthetic property records")
        return df

    def _calculate_realistic_rent(self, bedrooms, bathrooms, sqft, year_built, property_types,
                                crime_score, walkability_score, transit_score, amenity_score,
                                distance_to_subway, distance_to_manhattan, neighborhoods,
                                last_sale_price):
        """Calculate realistic rental prices based on NYC market patterns"""

        # Base rent by bedrooms (NYC 2024 market rates)
        base_rent_map = {1: 3200, 2: 4500, 3: 6500, 4: 9000}
        monthly_rent = np.array([base_rent_map[br] for br in bedrooms], dtype=float)

        # Square footage adjustment ($2-4 per sqft premium/discount)
        sqft_adjustment = (sqft - 900) * 2.5
        monthly_rent += sqft_adjustment

        # Property age adjustment (newer = premium)
        age = 2024 - year_built
        age_factor = np.exp(-age / 80)  # Exponential decay with age
        monthly_rent *= (0.85 + 0.3 * age_factor)

        # Property type adjustment
        type_multipliers = {'Condo': 1.1, 'Co-op': 0.95, 'Rental': 1.0}
        for i, ptype in enumerate(property_types):
            monthly_rent[i] *= type_multipliers[ptype]

        # Location score adjustments (normalized to 0-1)
        location_score = (crime_score + walkability_score + transit_score + amenity_score) / 400
        monthly_rent *= (0.7 + 0.6 * location_score)

        # Distance penalties
        subway_factor = np.exp(-distance_to_subway / 1.5)  # Subway proximity crucial in NYC
        manhattan_factor = np.exp(-distance_to_manhattan / 15)  # Manhattan proximity premium
        monthly_rent *= subway_factor * manhattan_factor

        # Neighborhood premiums (based on actual NYC market data)
        neighborhood_multipliers = {
            'Tribeca': 1.8, 'SoHo': 1.7, 'West Village': 1.6, 'Chelsea': 1.4,
            'Upper East Side': 1.3, 'Upper West Side': 1.25, 'Midtown': 1.2,
            'East Village': 1.1, 'Financial District': 1.05, 'DUMBO': 1.0,
            'Williamsburg': 1.0, 'Park Slope': 0.95, 'Carroll Gardens': 0.9,
            'Long Island City': 0.85, 'Astoria': 0.8, 'Red Hook': 0.75
        }
        for i, neighborhood in enumerate(neighborhoods):
            monthly_rent[i] *= neighborhood_multipliers.get(neighborhood, 1.0)

        # Sale price correlation (higher value properties command higher rents)
        price_factor = np.log(last_sale_price / 1000000)  # Log of price in millions
        monthly_rent *= (0.8 + 0.2 * np.clip(price_factor, 0, 2))

        # Bathroom premium
        bathroom_factor = 1 + (bathrooms - bedrooms) * 0.15
        monthly_rent *= bathroom_factor

        # Add realistic market noise
        monthly_rent *= np.random.normal(1.0, 0.08, len(monthly_rent))

        # Round to nearest integer and clip to realistic range
        return np.clip(np.round(monthly_rent), 1800, 25000).astype(int)

    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        """
        Prepare features for machine learning.

        Args:
            df: Input DataFrame with property data

        Returns:
            Tuple of (features DataFrame, target Series)
        """
        df_processed = df.copy()

        # Handle missing values with sensible defaults
        numeric_columns = ['crime_score', 'walkability_score', 'transit_score', 'amenity_score',
                          'distance_to_subway', 'distance_to_manhattan']

        for col in numeric_columns:
            if col in df_processed.columns:
                df_processed[col] = df_processed[col].fillna(df_processed[col].median())

        # Feature engineering
        df_processed['property_age'] = 2024 - df_processed['year_built']
        df_processed['price_per_sqft'] = df_processed['last_sale_price'] / df_processed['sqft']
        df_processed['rooms_total'] = df_processed['bedrooms'] + df_processed['bathrooms']

        # Composite location score
        location_cols = ['crime_score', 'walkability_score', 'transit_score', 'amenity_score']
        available_location_cols = [col for col in location_cols if col in df_processed.columns]
        if available_location_cols:
            df_processed['location_score'] = df_processed[available_location_cols].mean(axis=1)
        else:
            df_processed['location_score'] = 75  # Default neutral score

        # Transportation convenience score
        if 'distance_to_subway' in df_processed.columns and 'distance_to_manhattan' in df_processed.columns:
            df_processed['transport_score'] = (
                100 * np.exp(-df_processed['distance_to_subway'] / 0.5) * 0.6 +
                100 * np.exp(-df_processed['distance_to_manhattan'] / 10) * 0.4
            )
        else:
            df_processed['transport_score'] = 75

        # Size efficiency score
        df_processed['sqft_per_room'] = df_processed['sqft'] / df_processed['rooms_total']

        # Encode categorical variables
        categorical_features = ['property_type', 'neighborhood']
        for feature in categorical_features:
            if feature in df_processed.columns:
                if feature not in self.label_encoders:
                    self.label_encoders[feature] = LabelEncoder()
                    df_processed[f'{feature}_encoded'] = self.label_encoders[feature].fit_transform(
                        df_processed[feature].astype(str)
                    )
                else:
                    # Handle new categories in prediction
                    known_categories = set(self.label_encoders[feature].classes_)
                    df_processed[feature] = df_processed[feature].astype(str).apply(
                        lambda x: x if x in known_categories else 'Unknown'
                    )

                    # Add 'Unknown' category if not present
                    if 'Unknown' not in known_categories:
                        self.label_encoders[feature].classes_ = np.append(
                            self.label_encoders[feature].classes_, 'Unknown'
                        )

                    df_processed[f'{feature}_encoded'] = self.label_encoders[feature].transform(
                        df_processed[feature]
                    )

        # Select features for model training
        base_features = [
            'bedrooms', 'bathrooms', 'sqft', 'property_age', 'last_sale_price',
            'price_per_sqft', 'rooms_total', 'location_score', 'transport_score',
            'sqft_per_room'
        ]

        # Add available numeric features
        optional_features = [
            'crime_score', 'walkability_score', 'transit_score', 'amenity_score',
            'distance_to_subway', 'distance_to_manhattan'
        ]

        feature_columns = [col for col in base_features if col in df_processed.columns]
        feature_columns.extend([col for col in optional_features if col in df_processed.columns])

        # Add encoded categorical features
        encoded_features = [col for col in df_processed.columns if col.endswith('_encoded')]
        feature_columns.extend(encoded_features)

        X = df_processed[feature_columns]
        y = df_processed['monthly_rent'] if 'monthly_rent' in df_processed.columns else None

        self.logger.info(f"Prepared {len(feature_columns)} features for {len(X)} samples")
        return X, y

    def train_model(self, X: pd.DataFrame, y: pd.Series) -> Dict:
        """
        Train and evaluate multiple models, select the best one.

        Args:
            X: Feature matrix
            y: Target variable (monthly rent)

        Returns:
            Dictionary with training results and metrics
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=None
        )

        # Define models to try
        models = {
            'Random Forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingRegressor(
                n_estimators=100,
                max_depth=8,
                learning_rate=0.1,
                min_samples_split=5,
                random_state=42
            )
        }

        results = {}
        best_score = -float('inf')
        best_model = None

        for name, model in models.items():
            self.logger.info(f"Training {name}...")

            # Train model
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()

            results[name] = {
                'model': model,
                'rmse': rmse,
                'mae': mae,
                'r2': r2,
                'cv_r2_mean': cv_mean,
                'cv_r2_std': cv_std,
                'predictions': y_pred
            }

            self.logger.info(f"{name}: R² = {r2:.3f}, RMSE = ${rmse:.0f}, CV = {cv_mean:.3f}±{cv_std:.3f}")

            # Select best model based on cross-validation R²
            if cv_mean > best_score:
                best_score = cv_mean
                best_model = model
                self.model_metrics = {
                    'r2': r2,
                    'rmse': rmse,
                    'mae': mae,
                    'cv_r2_mean': cv_mean,
                    'cv_r2_std': cv_std
                }

        self.model = best_model
        best_model_name = max(results.keys(), key=lambda k: results[k]['cv_r2_mean'])

        self.logger.info(f"\nBest model: {best_model_name}")
        self.logger.info(f"CV R² Score: {self.model_metrics['cv_r2_mean']:.3f} ± {self.model_metrics['cv_r2_std']:.3f}")

        # Calculate feature importance for tree-based models
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)

            self.logger.info("\nTop 5 Most Important Features:")
            for idx, row in self.feature_importance.head().iterrows():
                self.logger.info(f"  {row['feature']}: {row['importance']:.3f}")

        return results

    def predict_revenue(self, features: Dict) -> Dict:
        """
        Predict monthly rental revenue for a single property.

        Args:
            features: Dictionary with property features

        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model() first.")

        # Convert to DataFrame
        df = pd.DataFrame([features])

        # Prepare features using the same preprocessing
        X, _ = self.prepare_features(df)

        # Make prediction
        prediction = self.model.predict(X)[0]

        # Calculate confidence interval based on model RMSE
        rmse = self.model_metrics.get('rmse', prediction * 0.1)
        confidence_lower = max(1500, prediction - 1.96 * rmse)
        confidence_upper = prediction + 1.96 * rmse

        # Calculate annual metrics
        annual_revenue = prediction * 12
        annual_revenue_range = (confidence_lower * 12, confidence_upper * 12)

        return {
            'predicted_monthly_rent': round(prediction, 0),
            'confidence_interval': (round(confidence_lower, 0), round(confidence_upper, 0)),
            'annual_revenue': round(annual_revenue, 0),
            'annual_revenue_range': (round(annual_revenue_range[0], 0), round(annual_revenue_range[1], 0)),
            'model_r2': self.model_metrics.get('r2', 0),
            'model_rmse': self.model_metrics.get('rmse', 0),
            'prediction_confidence': 'High' if rmse < prediction * 0.15 else 'Medium' if rmse < prediction * 0.25 else 'Low'
        }

    def save_model(self, filepath: str):
        """Save the trained model and preprocessing objects"""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")

        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_importance': self.feature_importance,
            'model_metrics': self.model_metrics
        }

        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        joblib.dump(model_data, filepath)
        self.logger.info(f"Model saved to {filepath}")

    def load_model(self, filepath: str):
        """Load a trained model and preprocessing objects"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_importance = model_data['feature_importance']
        self.model_metrics = model_data['model_metrics']
        self.logger.info(f"Model loaded from {filepath}")

    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance if available"""
        if self.feature_importance is None:
            self.logger.warning("Feature importance not available")
            return pd.DataFrame()
        return self.feature_importance.copy()

    def validate_features(self, features: Dict) -> Dict:
        """
        Validate and clean input features.

        Args:
            features: Raw feature dictionary

        Returns:
            Cleaned feature dictionary
        """
        cleaned = features.copy()

        # Ensure required features have reasonable values
        required_features = ['bedrooms', 'bathrooms', 'sqft', 'year_built', 'last_sale_price']

        for feature in required_features:
            if feature not in cleaned:
                raise ValueError(f"Required feature '{feature}' is missing")

        # Validate ranges
        if cleaned['bedrooms'] < 0 or cleaned['bedrooms'] > 10:
            self.logger.warning(f"Unusual bedroom count: {cleaned['bedrooms']}")

        if cleaned['sqft'] < 200 or cleaned['sqft'] > 10000:
            self.logger.warning(f"Unusual square footage: {cleaned['sqft']}")

        if cleaned['year_built'] < 1800 or cleaned['year_built'] > 2024:
            self.logger.warning(f"Unusual year built: {cleaned['year_built']}")

        # Set defaults for optional features
        defaults = {
            'crime_score': 75,
            'walkability_score': 75,
            'transit_score': 75,
            'amenity_score': 65,
            'distance_to_subway': 0.3,
            'distance_to_manhattan': 5.0,
            'property_type': 'Condo',
            'neighborhood': 'Midtown'
        }

        for feature, default_value in defaults.items():
            if feature not in cleaned:
                cleaned[feature] = default_value
                self.logger.info(f"Set default value for {feature}: {default_value}")

        return cleaned
