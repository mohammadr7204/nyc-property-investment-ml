"""
Main NYC Property Investment Analyzer
Integrates data collection pipeline with ML revenue prediction for complete property analysis.
Enhanced with real data sources and improved accuracy.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import logging
from src.data_pipeline import NYCPropertyDataPipeline, PropertyData
from src.ml_model import NYCRevenuePredictor

class NYCPropertyInvestmentAnalyzer:
    """
    Complete property investment analysis system for NYC.
    Integrates real data collection pipeline with ML revenue prediction.
    """

    def __init__(self, google_api_key: str):
        self.google_api_key = google_api_key
        self.data_pipeline = NYCPropertyDataPipeline(google_api_key)
        self.revenue_predictor = NYCRevenuePredictor()
        self.logger = logging.getLogger(__name__)

        # Initialize model with synthetic data (can be retrained with real data later)
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
            self.logger.info(f"Model trained successfully. R² = {metrics.get('r2', 0):.3f}")

        except Exception as e:
            self.logger.error(f"Error initializing model: {e}")
            raise

    def analyze_property(self, address: str) -> Dict:
        """
        Complete analysis workflow for a single property using real data sources.

        Steps:
        1. Geocode address to get coordinates
        2. Collect real property data from NYC records
        3. Gather real location features (crime, transit, amenities)
        4. Find real rental comparables
        5. Predict revenue using ML model
        6. Generate comprehensive investment analysis

        Args:
            address: Property address to analyze

        Returns:
            Complete investment analysis dictionary with data quality scores
        """
        self.logger.info(f"Analyzing property with real data: {address}")

        try:
            # Step 1: Geocode address to get real coordinates
            coordinates = self.data_pipeline.geocode_address(address)
            if not coordinates:
                self.logger.warning(f"Could not geocode address: {address}")
                # Fallback to simulated data
                return self._analyze_with_fallback_data(address)

            # Step 2: Collect real property data
            property_data = self._collect_real_property_data(address, coordinates)

            # Step 3: Gather real location features
            location_features = self._collect_real_location_features(
                property_data['latitude'],
                property_data['longitude']
            )

            # Step 4: Find real rental comparables
            rental_comps = self._collect_real_rental_comps(
                property_data['latitude'],
                property_data['longitude'],
                property_data['bedrooms']
            )

            # Step 5: Predict revenue using ML model
            combined_features = {**property_data, **location_features}

            # Validate features before prediction
            validated_features = self.revenue_predictor.validate_features(combined_features)
            revenue_prediction = self.revenue_predictor.predict_revenue(validated_features)

            # Step 6: Generate comprehensive investment analysis
            investment_analysis = self._generate_investment_analysis(
                property_data, location_features, rental_comps, revenue_prediction
            )

            # Add data quality information
            investment_analysis['data_quality'] = self._assess_data_quality(
                property_data, location_features, rental_comps, coordinates
            )

            self.logger.info(f"Real data analysis completed for {address} "
                           f"(quality: {investment_analysis['data_quality']['overall_score']}/100)")
            return investment_analysis

        except Exception as e:
            self.logger.error(f"Error analyzing property {address}: {e}")
            # Fallback to basic analysis
            return self._analyze_with_fallback_data(address)

    def _collect_real_property_data(self, address: str, coordinates: Dict) -> Dict:
        """
        Collect real property data using NYC Department of Finance records
        """
        try:
            # Try to get real property data from NYC Open Data
            nyc_property_data = self.data_pipeline.get_real_property_data(address)

            if nyc_property_data:
                # Merge with coordinates
                property_data = {
                    'address': address,
                    'latitude': coordinates['lat'],
                    'longitude': coordinates['lng'],
                    **nyc_property_data
                }
                self.logger.info(f"Retrieved real property data from {nyc_property_data.get('source', 'NYC records')}")
            else:
                # Generate realistic estimates based on location
                property_data = self._estimate_property_data_by_location(address, coordinates)
                self.logger.info("Using location-based property estimates")

            return property_data

        except Exception as e:
            self.logger.error(f"Error collecting real property data: {e}")
            return self._estimate_property_data_by_location(address, coordinates)

    def _estimate_property_data_by_location(self, address: str, coordinates: Dict) -> Dict:
        """
        Estimate property data based on NYC location patterns when real data unavailable
        """
        lat, lng = coordinates['lat'], coordinates['lng']

        # Determine neighborhood tier based on location
        neighborhood = self.data_pipeline._determine_neighborhood(lat, lng)

        # Property characteristics based on neighborhood patterns
        if neighborhood in ['Tribeca', 'SoHo', 'West Village']:
            # Luxury neighborhoods
            property_type = np.random.choice(['Condo', 'Co-op'], p=[0.7, 0.3])
            bedrooms = np.random.choice([1, 2, 3, 4], p=[0.2, 0.4, 0.3, 0.1])
            sqft_base = {1: 800, 2: 1200, 3: 1600, 4: 2200}
            price_base = {1: 1200000, 2: 1800000, 3: 2800000, 4: 4000000}
        elif neighborhood in ['Upper East Side', 'Upper West Side', 'Chelsea']:
            # Mid-tier neighborhoods
            property_type = np.random.choice(['Condo', 'Co-op', 'Rental'], p=[0.4, 0.4, 0.2])
            bedrooms = np.random.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1])
            sqft_base = {1: 650, 2: 1000, 3: 1400, 4: 1800}
            price_base = {1: 800000, 2: 1300000, 3: 2000000, 4: 2800000}
        else:
            # Affordable neighborhoods
            property_type = np.random.choice(['Condo', 'Co-op', 'Rental'], p=[0.3, 0.3, 0.4])
            bedrooms = np.random.choice([1, 2, 3, 4], p=[0.4, 0.4, 0.15, 0.05])
            sqft_base = {1: 550, 2: 850, 3: 1200, 4: 1500}
            price_base = {1: 600000, 2: 900000, 3: 1400000, 4: 1900000}

        sqft = int(sqft_base[bedrooms] * np.random.uniform(0.85, 1.15))
        bathrooms = max(1.0, bedrooms + np.random.choice([-0.5, 0, 0.5]))
        year_built = np.random.randint(1960, 2020)
        last_sale_price = int(price_base[bedrooms] * np.random.uniform(0.8, 1.2))

        return {
            'address': address,
            'latitude': lat,
            'longitude': lng,
            'property_type': property_type,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'sqft': sqft,
            'year_built': year_built,
            'last_sale_price': last_sale_price,
            'data_quality': 'estimated',
            'source': 'Location-based estimation'
        }

    def _collect_real_location_features(self, lat: float, lng: float) -> Dict:
        """
        Collect real location features using enhanced data pipeline methods
        """
        try:
            # Use real data collection methods from enhanced pipeline
            crime_score = self.data_pipeline.collect_crime_data(lat, lng)
            transit_score = self.data_pipeline.calculate_transit_score(lat, lng)
            amenities_data = self.data_pipeline.get_google_places_amenities(lat, lng)
            amenity_score = amenities_data['score']

            # Calculate enhanced walkability score
            walkability_score = min(100, (transit_score * 0.6 + amenity_score * 0.4))

            # Get real distances
            manhattan_center = (40.7580, -73.9855)
            from geopy.distance import geodesic
            distance_to_manhattan = geodesic((lat, lng), manhattan_center).miles

            # Get real subway distance
            subway_stations = self.data_pipeline.get_subway_stations()
            distance_to_subway = self.data_pipeline._calculate_nearest_subway_distance(
                lat, lng, subway_stations
            )

            # Determine neighborhood
            neighborhood = self.data_pipeline._determine_neighborhood(lat, lng)

            location_features = {
                'crime_score': crime_score,
                'transit_score': transit_score,
                'amenity_score': amenity_score,
                'walkability_score': round(walkability_score, 1),
                'distance_to_subway': round(distance_to_subway, 2),
                'distance_to_manhattan': round(distance_to_manhattan, 2),
                'neighborhood': neighborhood,
                'amenity_counts': amenities_data.get('counts', {}),
                'total_amenities': amenities_data.get('total_amenities', 0)
            }

            self.logger.info(f"Real location features collected: Crime {crime_score}, "
                           f"Transit {transit_score}, Amenities {amenity_score}")

            return location_features

        except Exception as e:
            self.logger.error(f"Error collecting real location features: {e}")
            # Fallback to estimation
            return self._estimate_location_features(lat, lng)

    def _estimate_location_features(self, lat: float, lng: float) -> Dict:
        """Fallback location feature estimation"""
        neighborhood = self.data_pipeline._determine_neighborhood(lat, lng)

        # Estimate based on neighborhood and distance to Manhattan
        manhattan_center = (40.7580, -73.9855)
        from geopy.distance import geodesic
        distance_to_manhattan = geodesic((lat, lng), manhattan_center).miles

        if distance_to_manhattan <= 3:
            crime_score = np.random.uniform(75, 90)
            transit_score = np.random.uniform(80, 95)
            amenity_score = np.random.uniform(70, 90)
        elif distance_to_manhattan <= 8:
            crime_score = np.random.uniform(70, 85)
            transit_score = np.random.uniform(65, 85)
            amenity_score = np.random.uniform(60, 80)
        else:
            crime_score = np.random.uniform(65, 80)
            transit_score = np.random.uniform(50, 70)
            amenity_score = np.random.uniform(50, 70)

        return {
            'crime_score': round(crime_score, 1),
            'transit_score': round(transit_score, 1),
            'amenity_score': round(amenity_score, 1),
            'walkability_score': round((transit_score + amenity_score) / 2, 1),
            'distance_to_subway': round(np.random.uniform(0.1, 0.8), 2),
            'distance_to_manhattan': round(distance_to_manhattan, 2),
            'neighborhood': neighborhood,
            'amenity_counts': {},
            'total_amenities': 0
        }

    def _collect_real_rental_comps(self, lat: float, lng: float, bedrooms: int) -> List[Dict]:
        """
        Collect real rental comparables using enhanced pipeline methods
        """
        try:
            return self.data_pipeline.collect_rental_comparables(lat, lng, bedrooms)
        except Exception as e:
            self.logger.error(f"Error collecting real rental comparables: {e}")
            return self._generate_fallback_comps(lat, lng, bedrooms)

    def _generate_fallback_comps(self, lat: float, lng: float, bedrooms: int) -> List[Dict]:
        """Generate fallback rental comparables"""
        neighborhood = self.data_pipeline._determine_neighborhood(lat, lng)

        # Base rents by neighborhood and bedrooms
        base_rents = {
            'Tribeca': {1: 4500, 2: 6500, 3: 9500, 4: 13000},
            'SoHo': {1: 4200, 2: 6200, 3: 9000, 4: 12500},
            'West Village': {1: 4000, 2: 5800, 3: 8500, 4: 12000},
            'Chelsea': {1: 3800, 2: 5500, 3: 8000, 4: 11500},
            'Upper East Side': {1: 3200, 2: 4800, 3: 7200, 4: 10000},
            'Upper West Side': {1: 3000, 2: 4500, 3: 6800, 4: 9500}
        }

        base_rent = base_rents.get(neighborhood, {1: 3000, 2: 4500, 3: 6800, 4: 9500}).get(bedrooms, 4500)

        comps = []
        for i in range(4):
            rent = base_rent * np.random.uniform(0.85, 1.15)
            comps.append({
                'address': f"Comparable {i+1}, {neighborhood}, NY",
                'latitude': lat + np.random.uniform(-0.01, 0.01),
                'longitude': lng + np.random.uniform(-0.01, 0.01),
                'monthly_rent': round(rent, 0),
                'bedrooms': bedrooms,
                'bathrooms': bedrooms + np.random.choice([0, 0.5, 1]),
                'sqft': bedrooms * 450 + np.random.randint(-100, 200),
                'distance_miles': round(np.random.uniform(0.1, 0.5), 2),
                'listing_source': 'Market Estimate'
            })

        return comps

    def _analyze_with_fallback_data(self, address: str) -> Dict:
        """
        Fallback analysis using simulated data when real data unavailable
        """
        self.logger.warning(f"Using fallback data analysis for {address}")

        # Generate simulated property data
        property_data = self._simulate_property_data(address)

        # Generate simulated location features
        location_features = self._simulate_location_features(
            property_data['latitude'],
            property_data['longitude']
        )

        # Generate simulated rental comparables
        rental_comps = self._simulate_rental_comps(
            property_data['latitude'],
            property_data['longitude'],
            property_data['bedrooms']
        )

        # Predict revenue
        combined_features = {**property_data, **location_features}
        validated_features = self.revenue_predictor.validate_features(combined_features)
        revenue_prediction = self.revenue_predictor.predict_revenue(validated_features)

        # Generate investment analysis
        investment_analysis = self._generate_investment_analysis(
            property_data, location_features, rental_comps, revenue_prediction
        )

        # Mark as simulated data
        investment_analysis['data_quality'] = {
            'overall_score': 50,
            'data_source': 'simulated',
            'geocoding_quality': 'low',
            'property_data_quality': 'simulated',
            'location_data_quality': 'simulated',
            'rental_data_quality': 'simulated'
        }

        return investment_analysis

    def _simulate_property_data(self, address: str) -> Dict:
        """Simulate property data (kept for fallback)"""
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
        """Simulate location features (kept for fallback)"""
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
        return self.data_pipeline._determine_neighborhood(lat, lng)

    def _simulate_rental_comps(self, lat: float, lng: float, bedrooms: int) -> List[Dict]:
        """Simulate rental comparables (kept for fallback)"""
        return self.data_pipeline.collect_rental_comparables(lat, lng, bedrooms)

    def _assess_data_quality(self, property_data: Dict, location_features: Dict,
                           rental_comps: List[Dict], coordinates: Dict) -> Dict:
        """
        Assess the quality of collected data for transparency
        """
        quality_score = 0

        # Geocoding quality (20 points)
        geocoding_quality = coordinates.get('data_quality', 'low')
        if geocoding_quality == 'high':
            quality_score += 20
            geo_score = 'high'
        elif geocoding_quality == 'medium':
            quality_score += 15
            geo_score = 'medium'
        else:
            quality_score += 10
            geo_score = 'low'

        # Property data quality (30 points)
        prop_source = property_data.get('source', 'estimated')
        if 'NYC' in prop_source:
            quality_score += 30
            prop_quality = 'high'
        elif 'estimated' in prop_source:
            quality_score += 20
            prop_quality = 'medium'
        else:
            quality_score += 10
            prop_quality = 'low'

        # Location data quality (25 points)
        if location_features.get('crime_score', 0) > 0:
            quality_score += 10
        if location_features.get('total_amenities', 0) > 5:
            quality_score += 10
        if location_features.get('distance_to_subway', 999) < 2:
            quality_score += 5
        location_quality = 'high' if quality_score >= 70 else 'medium' if quality_score >= 50 else 'low'

        # Rental comps quality (25 points)
        rental_sources = [comp.get('listing_source', 'unknown') for comp in rental_comps]
        real_sources = [s for s in rental_sources if s not in ['Estimated', 'Market Estimate']]

        if len(real_sources) >= 3:
            quality_score += 25
            rental_quality = 'high'
        elif len(real_sources) >= 1:
            quality_score += 15
            rental_quality = 'medium'
        else:
            quality_score += 5
            rental_quality = 'low'

        return {
            'overall_score': min(100, quality_score),
            'data_source': 'mixed' if quality_score >= 70 else 'estimated',
            'geocoding_quality': geo_score,
            'property_data_quality': prop_quality,
            'location_data_quality': location_quality,
            'rental_data_quality': rental_quality,
            'real_data_sources': len(real_sources),
            'total_comparables': len(rental_comps)
        }

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

        # Enhanced risk assessment
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

        # New risk factors based on real data
        if location_features.get('total_amenities', 0) < 10:
            risk_factors.append("Limited nearby amenities")
            risk_score += 1

        if len(rental_comps) < 3:
            risk_factors.append("Limited rental market data")
            risk_score += 1

        # Overall risk assessment
        if risk_score <= 1:
            overall_risk = 'Low'
        elif risk_score <= 3:
            overall_risk = 'Medium'
        else:
            overall_risk = 'High'

        # Enhanced investment recommendation
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

        if location_features.get('total_amenities', 0) >= 20:
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
        """Generate a detailed investment report with data quality information"""

        prop = analysis['property_details']
        loc = analysis['location_analysis']
        rev = analysis['revenue_prediction']
        fin = analysis['financial_metrics']
        risk = analysis['risk_assessment']
        rec = analysis['investment_recommendation']
        quality = analysis.get('data_quality', {})

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
Rental Comparables:       {quality.get('total_comparables', 0)} found

📍 LOCATION ANALYSIS (Scores out of 100)
──────────────────────────────────────────────────────────────────
Crime Score:              {loc['crime_score']:.0f}/100 {'🟢' if loc['crime_score'] >= 80 else '🟡' if loc['crime_score'] >= 65 else '🔴'}
Walkability Score:        {loc['walkability_score']:.0f}/100
Transit Score:            {loc['transit_score']:.0f}/100 {'🟢' if loc['transit_score'] >= 80 else '🟡' if loc['transit_score'] >= 65 else '🔴'}
Amenity Score:            {loc['amenity_score']:.0f}/100
Distance to Subway:       {loc['distance_to_subway']:.1f} miles
Distance to Manhattan:    {loc['distance_to_manhattan']:.1f} miles
Total Nearby Amenities:   {loc.get('total_amenities', 0)}

⚠️  RISK ASSESSMENT
──────────────────────────────────────────────────────────────────
Overall Risk Level:       {risk['overall_risk']} {'🟢' if risk['overall_risk'] == 'Low' else '🟡' if risk['overall_risk'] == 'Medium' else '🔴'}
Risk Factors:             {', '.join(risk['risk_factors']) if risk['risk_factors'] else 'None identified'}

🎯 INVESTMENT RECOMMENDATION
──────────────────────────────────────────────────────────────────
Recommendation:           {rec['recommendation']} {'🚀' if 'BUY' in rec['recommendation'] else '⏸️' if 'HOLD' in rec['recommendation'] else '❌'}
Confidence Level:         {rec['confidence']}

📈 DATA QUALITY ASSESSMENT
──────────────────────────────────────────────────────────────────
Overall Data Quality:     {quality.get('overall_score', 0)}/100 {'🟢' if quality.get('overall_score', 0) >= 80 else '🟡' if quality.get('overall_score', 0) >= 60 else '🔴'}
Property Data Source:     {quality.get('property_data_quality', 'unknown').title()}
Location Data Quality:    {quality.get('location_data_quality', 'unknown').title()}
Rental Data Quality:      {quality.get('rental_data_quality', 'unknown').title()}
Real Data Sources:        {quality.get('real_data_sources', 0)} of {quality.get('total_comparables', 0)} comparables

💡 KEY INSIGHTS
──────────────────────────────────────────────────────────────────
• {'Strong rental yield indicates excellent investment potential' if fin['gross_rental_yield'] >= 5 else 'Moderate rental yield suggests careful evaluation needed' if fin['gross_rental_yield'] >= 4 else 'Low rental yield - consider other investment options'}
• {'Excellent location scores support premium rents and tenant demand' if (loc['crime_score'] + loc['transit_score']) / 2 >= 80 else 'Good location fundamentals with room for improvement' if (loc['crime_score'] + loc['transit_score']) / 2 >= 65 else 'Location challenges may limit rental growth potential'}
• {'Modern property supports lower maintenance costs and higher rents' if prop['year_built'] >= 1990 else 'Mature property may require renovation budget but offers character' if prop['year_built'] >= 1970 else 'Older property requires significant maintenance consideration'}
• {f"Positive cash flow of ${fin['monthly_cash_flow']:,.0f}/month" if fin['monthly_cash_flow'] > 0 else f"Negative cash flow of ${abs(fin['monthly_cash_flow']):,.0f}/month requires additional capital"}
• {'High data quality provides reliable analysis' if quality.get('overall_score', 0) >= 80 else 'Medium data quality - consider additional research' if quality.get('overall_score', 0) >= 60 else 'Limited data available - use with caution'}

🔍 MODEL PERFORMANCE
──────────────────────────────────────────────────────────────────
Model Accuracy (R²):      {rev['model_r2']:.3f}
Prediction RMSE:          ${rev['model_rmse']:,.0f}

═══════════════════════════════════════════════════════════════════
DISCLAIMER: This analysis is based on algorithmic predictions and
available market data. Data quality: {quality.get('overall_score', 0)}/100. Consult with real estate
professionals and conduct thorough due diligence before making
investment decisions.
═══════════════════════════════════════════════════════════════════
        """

        return report

    def batch_analyze_properties(self, addresses: List[str]) -> pd.DataFrame:
        """Analyze multiple properties and return comparison DataFrame"""
        self.logger.info(f"Batch analyzing {len(addresses)} properties with real data...")

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
                quality = analysis.get('data_quality', {})

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
                    'overall_risk': analysis['risk_assessment']['overall_risk'],
                    'data_quality_score': quality.get('overall_score', 0),
                    'total_amenities': loc.get('total_amenities', 0),
                    'distance_to_subway': loc['distance_to_subway']
                })

            except Exception as e:
                self.logger.error(f"Error analyzing {address}: {e}")
                continue

        df = pd.DataFrame(results)

        if not df.empty:
            # Sort by investment attractiveness (gross yield weighted by data quality)
            df['weighted_score'] = df['gross_yield'] * (df['data_quality_score'] / 100)
            df = df.sort_values('weighted_score', ascending=False)
            self.logger.info(f"Batch analysis complete: {len(df)} properties analyzed successfully")
        else:
            self.logger.warning("No properties analyzed successfully")

        return df

    def rank_investment_opportunities(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rank properties by investment attractiveness with data quality weighting"""

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

        # Data quality bonus
        df['quality_bonus'] = df['data_quality_score'] / 100 * 10  # Up to 10 point bonus

        # Calculate composite score with weights
        df['investment_score'] = (
            df['yield_score'] * 0.3 +           # 30% weight on yield
            df['rent_score'] * 0.25 +          # 25% on rent potential
            df['location_score_norm'] * 0.25 + # 25% on location
            df['cash_flow_score'] * 0.15 +     # 15% on cash flow
            df['quality_bonus'] * 0.05         # 5% on data quality
        )

        # Adjust for risk
        risk_adjustment = {'Low': 1.0, 'Medium': 0.9, 'High': 0.75}
        df['investment_score'] *= df['overall_risk'].map(risk_adjustment)

        # Rank properties
        df['rank'] = df['investment_score'].rank(ascending=False, method='dense').astype(int)

        # Clean up temporary columns
        cols_to_drop = ['yield_score', 'rent_score', 'location_score_norm', 'cash_flow_score', 'quality_bonus', 'weighted_score']
        df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

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
            'feature_importance': self.revenue_predictor.get_feature_importance(),
            'data_pipeline_version': 'enhanced_with_real_data_v2.0'
        }
