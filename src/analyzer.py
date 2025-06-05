"""
Main NYC Property Investment Analyzer
Integrates data collection pipeline with ML revenue prediction for complete property analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import logging
from .data_pipeline import NYCPropertyDataPipeline
from .ml_model import NYCRevenuePredictor

class NYCPropertyInvestmentAnalyzer:
    """
    Complete property investment analysis system for NYC.
    Integrates data collection pipeline with ML revenue prediction.
    """
    
    def __init__(self, google_api_key: str):
        self.google_api_key = google_api_key
        self.data_pipeline = NYCPropertyDataPipeline(google_api_key)
        self.revenue_predictor = NYCRevenuePredictor()
        self.logger = logging.getLogger(__name__)
        
        # Initialize model with synthetic data
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize and train the ML model with synthetic data"""
        self.logger.info("Training ML model with synthetic NYC data...")
        
        try:
            # Generate training data
            df = self.revenue_predictor.generate_synthetic_training_data(1500)
            X, y = self.revenue_predictor.prepare_features(df)
            
            # Train model
            metrics = self.revenue_predictor.train_model(X, y)
            self.logger.info(f"Model trained successfully. R² = {metrics['r2']:.3f}")
            
        except Exception as e:
            self.logger.error(f"Error initializing model: {e}")
            raise
    
    def analyze_property(self, address: str) -> Dict:
        """
        Complete analysis workflow for a single property.
        
        Steps:
        1. Collect property data
        2. Gather location features
        3. Find rental comparables
        4. Predict revenue
        5. Generate investment report
        
        Args:
            address: Property address to analyze
            
        Returns:
            Complete investment analysis dictionary
        """
        self.logger.info(f"Analyzing property: {address}")
        
        try:
            # Step 1: Collect basic property data
            property_data = self._simulate_property_data(address)
            
            # Step 2: Gather location features
            location_features = self._simulate_location_features(
                property_data['latitude'], 
                property_data['longitude']
            )
            
            # Step 3: Find rental comparables
            rental_comps = self._simulate_rental_comps(
                property_data['latitude'],
                property_data['longitude'], 
                property_data['bedrooms']
            )
            
            # Step 4: Predict revenue
            combined_features = {**property_data, **location_features}
            
            # Validate features before prediction
            validated_features = self.revenue_predictor.validate_features(combined_features)
            revenue_prediction = self.revenue_predictor.predict_revenue(validated_features)
            
            # Step 5: Generate investment analysis
            investment_analysis = self._generate_investment_analysis(
                property_data, location_features, rental_comps, revenue_prediction
            )
            
            self.logger.info(f"Analysis completed for {address}")
            return investment_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing property {address}: {e}")
            raise
    
    def _simulate_property_data(self, address: str) -> Dict:
        """Simulate property data collection (in production, would use real APIs)"""
        # Generate realistic NYC coordinates
        base_lat = 40.7589  # Near Central Park
        base_lng = -73.9851
        
        # Add variation for different areas
        lat_offset = np.random.uniform(-0.05, 0.05)
        lng_offset = np.random.uniform(-0.05, 0.05)
        
        return {
            'address': address,
            'latitude': base_lat + lat_offset,
            'longitude': base_lng + lng_offset,
            'property_type': np.random.choice(['Condo', 'Co-op', 'Rental'], p=[0.5, 0.3, 0.2]),
            'bedrooms': np.random.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1]),
            'bathrooms': np.random.uniform(1, 3.5),
            'sqft': np.random.randint(600, 2200),
            'year_built': np.random.randint(1960, 2020),
            'last_sale_price': np.random.randint(700000, 4000000),
        }
    
    def _simulate_location_features(self, lat: float, lng: float) -> Dict:
        """Simulate location feature collection"""
        return {
            'crime_score': self.data_pipeline.collect_crime_data(lat, lng),
            'transit_score': self.data_pipeline.calculate_transit_score(lat, lng),
            'amenity_score': self.data_pipeline.get_google_places_amenities(lat, lng)['score'],
            'walkability_score': np.random.uniform(70, 95),
            'distance_to_subway': np.random.uniform(0.05, 0.8),
            'distance_to_manhattan': np.random.uniform(0.5, 15),
            'neighborhood': self._determine_neighborhood(lat, lng)
        }
    
    def _determine_neighborhood(self, lat: float, lng: float) -> str:
        """Determine neighborhood based on coordinates"""
        # Simplified neighborhood mapping
        if lat > 40.78:
            if lng > -73.96:
                return np.random.choice(['Upper East Side', 'Yorkville'])
            else:
                return np.random.choice(['Upper West Side', 'Morningside Heights'])
        elif lat > 40.75:
            return np.random.choice(['Midtown', 'Chelsea', 'Hell\'s Kitchen'])
        elif lat > 40.72:
            return np.random.choice(['East Village', 'West Village', 'SoHo', 'NoHo'])
        else:
            return np.random.choice(['Financial District', 'Tribeca', 'Battery Park'])
    
    def _simulate_rental_comps(self, lat: float, lng: float, bedrooms: int) -> List[Dict]:
        """Simulate rental comparable search"""
        return self.data_pipeline.collect_rental_comparables(lat, lng, bedrooms)
    
    def _generate_investment_analysis(self, property_data: Dict, location_features: Dict, 
                                    rental_comps: List[Dict], revenue_prediction: Dict) -> Dict:
        """Generate comprehensive investment analysis"""
        
        monthly_rent = revenue_prediction['predicted_monthly_rent']
        annual_revenue = revenue_prediction['annual_revenue']
        purchase_price = property_data['last_sale_price']
        
        # Financial metrics
        gross_yield = (annual_revenue / purchase_price) * 100
        
        # Operating expenses (property taxes, insurance, maintenance, management)
        # NYC typically 35-45% of gross rental income
        expense_rate = 0.38  # 38% average for NYC
        estimated_expenses = annual_revenue * expense_rate
        net_revenue = annual_revenue - estimated_expenses
        net_yield = (net_revenue / purchase_price) * 100
        
        # Cash flow analysis
        monthly_expenses = estimated_expenses / 12
        monthly_cash_flow = monthly_rent - monthly_expenses
        
        # Comparable analysis
        if rental_comps:
            comp_rents = [comp['monthly_rent'] for comp in rental_comps]
            avg_comp_rent = np.mean(comp_rents)
            rent_premium = ((monthly_rent - avg_comp_rent) / avg_comp_rent) * 100
        else:
            avg_comp_rent = monthly_rent
            rent_premium = 0
        
        # Risk assessment
        risk_factors = []
        risk_score = 0
        
        if location_features['crime_score'] < 70:
            risk_factors.append("Below average safety score")
            risk_score += 1
        
        if location_features['distance_to_subway'] > 0.6:
            risk_factors.append("Limited subway access")
            risk_score += 1
        
        if property_data['year_built'] < 1970:
            risk_factors.append("Older building may require higher maintenance")
            risk_score += 1
        
        if gross_yield < 3:
            risk_factors.append("Low rental yield")
            risk_score += 2
        
        if location_features['distance_to_manhattan'] > 10:
            risk_factors.append("Far from Manhattan job centers")
            risk_score += 1
        
        # Overall risk assessment
        if risk_score <= 1:
            overall_risk = 'Low'
        elif risk_score <= 3:
            overall_risk = 'Medium'
        else:
            overall_risk = 'High'
        
        # Investment recommendation
        recommendation_score = 0
        
        # Positive factors
        if gross_yield >= 5:
            recommendation_score += 3
        elif gross_yield >= 4:
            recommendation_score += 2
        elif gross_yield >= 3:
            recommendation_score += 1
        
        if location_features['crime_score'] >= 80:
            recommendation_score += 2
        elif location_features['crime_score'] >= 70:
            recommendation_score += 1
        
        if location_features['transit_score'] >= 85:
            recommendation_score += 1
        
        if rent_premium > 0:
            recommendation_score += 1
        
        # Negative factors
        recommendation_score -= risk_score
        
        # Final recommendation
        if recommendation_score >= 6:
            recommendation = "STRONG BUY"
            confidence = "High"
        elif recommendation_score >= 4:
            recommendation = "BUY"
            confidence = "Medium-High"
        elif recommendation_score >= 2:
            recommendation = "HOLD"
            confidence = "Medium"
        elif recommendation_score >= 0:
            recommendation = "WEAK HOLD"
            confidence = "Low-Medium"
        else:
            recommendation = "AVOID"
            confidence = "High"
        
        return {
            'property_details': property_data,
            'location_analysis': location_features,
            'rental_comparables': rental_comps,
            'revenue_prediction': revenue_prediction,
            'financial_metrics': {
                'gross_rental_yield': round(gross_yield, 2),
                'net_rental_yield': round(net_yield, 2),
                'estimated_annual_expenses': round(estimated_expenses, 0),
                'net_annual_revenue': round(net_revenue, 0),
                'monthly_cash_flow': round(monthly_cash_flow, 0),
                'rent_vs_comparables': round(rent_premium, 1),
                'expense_ratio': round(expense_rate * 100, 1)
            },
            'risk_assessment': {
                'risk_factors': risk_factors,
                'overall_risk': overall_risk,
                'risk_score': risk_score
            },
            'investment_recommendation': {
                'recommendation': recommendation,
                'confidence': confidence,
                'recommendation_score': recommendation_score
            }
        }
    
    def generate_detailed_report(self, analysis: Dict) -> str:
        """Generate a detailed investment report"""
        
        prop = analysis['property_details']
        loc = analysis['location_analysis']
        rev = analysis['revenue_prediction']
        fin = analysis['financial_metrics']
        risk = analysis['risk_assessment']
        rec = analysis['investment_recommendation']
        
        report = f"""
═══════════════════════════════════════════════════════════════════
                NYC PROPERTY INVESTMENT ANALYSIS REPORT
═══════════════════════════════════════════════════════════════════

🏠 PROPERTY OVERVIEW
──────────────────────────────────────────────────────────────────
Address:           {prop['address']}
Property Type:     {prop['property_type']}
Bedrooms:          {prop['bedrooms']}
Bathrooms:         {prop['bathrooms']:.1f}
Square Feet:       {prop['sqft']:,}
Year Built:        {prop['year_built']}
Last Sale Price:   ${prop['last_sale_price']:,}
Neighborhood:      {loc['neighborhood']}

💰 FINANCIAL PROJECTIONS
──────────────────────────────────────────────────────────────────
Predicted Monthly Rent:    ${rev['predicted_monthly_rent']:,.0f}
Confidence Range:          ${rev['confidence_interval'][0]:,.0f} - ${rev['confidence_interval'][1]:,.0f}
Annual Revenue:            ${rev['annual_revenue']:,}

Gross Rental Yield:       {fin['gross_rental_yield']:.2f}%
Net Rental Yield:         {fin['net_rental_yield']:.2f}%
Monthly Cash Flow:        ${fin['monthly_cash_flow']:,.0f}
Expense Ratio:            {fin['expense_ratio']:.1f}%

📊 MARKET COMPARISON
──────────────────────────────────────────────────────────────────
Rent vs. Comparables:     {fin['rent_vs_comparables']:+.1f}%
Market Position:          {'Above Market' if fin['rent_vs_comparables'] > 5 else 'At Market' if fin['rent_vs_comparables'] > -5 else 'Below Market'}
Prediction Confidence:    {rev['prediction_confidence']}

📍 LOCATION ANALYSIS (Scores out of 100)
──────────────────────────────────────────────────────────────────
Crime Score:              {loc['crime_score']:.0f}/100 {'🟢' if loc['crime_score'] >= 80 else '🟡' if loc['crime_score'] >= 65 else '🔴'}
Walkability Score:        {loc['walkability_score']:.0f}/100
Transit Score:            {loc['transit_score']:.0f}/100 {'🟢' if loc['transit_score'] >= 80 else '🟡' if loc['transit_score'] >= 65 else '🔴'}
Amenity Score:            {loc['amenity_score']:.0f}/100
Distance to Subway:       {loc['distance_to_subway']:.1f} miles
Distance to Manhattan:    {loc['distance_to_manhattan']:.1f} miles

⚠️  RISK ASSESSMENT
──────────────────────────────────────────────────────────────────
Overall Risk Level:       {risk['overall_risk']} {'🟢' if risk['overall_risk'] == 'Low' else '🟡' if risk['overall_risk'] == 'Medium' else '🔴'}
Risk Factors:             {', '.join(risk['risk_factors']) if risk['risk_factors'] else 'None identified'}

🎯 INVESTMENT RECOMMENDATION
──────────────────────────────────────────────────────────────────
Recommendation:           {rec['recommendation']} {'🚀' if 'BUY' in rec['recommendation'] else '⏸️' if 'HOLD' in rec['recommendation'] else '❌'}
Confidence Level:         {rec['confidence']}

💡 KEY INSIGHTS
──────────────────────────────────────────────────────────────────
• {'Strong rental yield indicates excellent investment potential' if fin['gross_rental_yield'] >= 5 else 'Moderate rental yield suggests careful evaluation needed' if fin['gross_rental_yield'] >= 4 else 'Low rental yield - consider other investment options'}
• {'Excellent location scores support premium rents and tenant demand' if (loc['crime_score'] + loc['transit_score']) / 2 >= 80 else 'Good location fundamentals with room for improvement' if (loc['crime_score'] + loc['transit_score']) / 2 >= 65 else 'Location challenges may limit rental growth potential'}
• {'Modern property supports lower maintenance costs and higher rents' if prop['year_built'] >= 1990 else 'Mature property may require renovation budget but offers character' if prop['year_built'] >= 1970 else 'Older property requires significant maintenance consideration'}
• {f"Positive cash flow of ${fin['monthly_cash_flow']:,.0f}/month" if fin['monthly_cash_flow'] > 0 else f"Negative cash flow of ${abs(fin['monthly_cash_flow']):,.0f}/month requires additional capital"}

🔍 MODEL PERFORMANCE
──────────────────────────────────────────────────────────────────
Model Accuracy (R²):      {rev['model_r2']:.3f}
Prediction RMSE:          ${rev['model_rmse']:,.0f}

═══════════════════════════════════════════════════════════════════
DISCLAIMER: This analysis is based on algorithmic predictions and 
current market data. Consult with real estate professionals and 
conduct thorough due diligence before making investment decisions.
═══════════════════════════════════════════════════════════════════
        """
        
        return report
    
    def batch_analyze_properties(self, addresses: List[str]) -> pd.DataFrame:
        """Analyze multiple properties and return comparison DataFrame"""
        self.logger.info(f"Batch analyzing {len(addresses)} properties...")
        
        results = []
        
        for i, address in enumerate(addresses, 1):
            self.logger.info(f"Processing {i}/{len(addresses)}: {address}")
            
            try:
                analysis = self.analyze_property(address)
                
                # Extract key metrics for comparison
                prop = analysis['property_details']
                fin = analysis['financial_metrics']
                rec = analysis['investment_recommendation']
                loc = analysis['location_analysis']
                
                results.append({
                    'address': address,
                    'bedrooms': prop['bedrooms'],
                    'sqft': prop['sqft'],
                    'year_built': prop['year_built'],
                    'last_sale_price': prop['last_sale_price'],
                    'neighborhood': loc['neighborhood'],
                    'predicted_monthly_rent': analysis['revenue_prediction']['predicted_monthly_rent'],
                    'annual_revenue': analysis['revenue_prediction']['annual_revenue'],
                    'gross_yield': fin['gross_rental_yield'],
                    'net_yield': fin['net_rental_yield'],
                    'monthly_cash_flow': fin['monthly_cash_flow'],
                    'location_score': (loc['crime_score'] + loc['transit_score'] + loc['amenity_score']) / 3,
                    'recommendation': rec['recommendation'],
                    'overall_risk': analysis['risk_assessment']['overall_risk']
                })
                
            except Exception as e:
                self.logger.error(f"Error analyzing {address}: {e}")
                continue
        
        df = pd.DataFrame(results)
        
        if not df.empty:
            # Sort by gross yield (best opportunities first)
            df = df.sort_values('gross_yield', ascending=False)
            self.logger.info(f"Batch analysis complete: {len(df)} properties analyzed successfully")
        else:
            self.logger.warning("No properties analyzed successfully")
        
        return df
    
    def rank_investment_opportunities(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rank properties by investment attractiveness"""
        
        if df.empty:
            return df
        
        # Create composite investment score
        df = df.copy()
        
        # Normalize metrics to 0-100 scale
        df['yield_score'] = (df['gross_yield'] / df['gross_yield'].max()) * 100
        df['rent_score'] = (df['predicted_monthly_rent'] / df['predicted_monthly_rent'].max()) * 100
        df['location_score_norm'] = df['location_score']
        df['cash_flow_score'] = np.where(
            df['monthly_cash_flow'] > 0,
            np.minimum((df['monthly_cash_flow'] / 2000) * 50 + 50, 100),
            np.maximum((df['monthly_cash_flow'] / 2000) * 50 + 50, 0)
        )
        
        # Calculate composite score with weights
        df['investment_score'] = (
            df['yield_score'] * 0.3 +           # 30% weight on yield
            df['rent_score'] * 0.25 +          # 25% on rent potential
            df['location_score_norm'] * 0.25 + # 25% on location
            df['cash_flow_score'] * 0.2        # 20% on cash flow
        )
        
        # Adjust for risk
        risk_adjustment = {'Low': 1.0, 'Medium': 0.9, 'High': 0.75}
        df['investment_score'] *= df['overall_risk'].map(risk_adjustment)
        
        # Rank properties
        df['rank'] = df['investment_score'].rank(ascending=False, method='dense').astype(int)
        
        # Clean up temporary columns
        cols_to_drop = ['yield_score', 'rent_score', 'location_score_norm', 'cash_flow_score']
        df = df.drop(columns=cols_to_drop)
        
        return df.sort_values('rank')
    
    def save_analysis_report(self, analysis: Dict, filepath: str):
        """Save analysis report to file"""
        report = self.generate_detailed_report(analysis)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"Analysis report saved to {filepath}")
    
    def get_model_info(self) -> Dict:
        """Get information about the trained model"""
        return {
            'model_type': type(self.revenue_predictor.model).__name__ if self.revenue_predictor.model else 'Not trained',
            'model_metrics': self.revenue_predictor.model_metrics,
            'feature_importance': self.revenue_predictor.get_feature_importance()
        }
