"""
Unit tests for the main analyzer module
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from analyzer import NYCPropertyInvestmentAnalyzer
from tests import TEST_CONFIG

class TestNYCPropertyInvestmentAnalyzer:
    """Test cases for the main analyzer"""
    
    @pytest.fixture(scope="class")
    def analyzer(self):
        """Create analyzer instance for testing"""
        return NYCPropertyInvestmentAnalyzer(TEST_CONFIG['demo_api_key'])
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initializes correctly"""
        assert analyzer.google_api_key == TEST_CONFIG['demo_api_key']
        assert hasattr(analyzer, 'data_pipeline')
        assert hasattr(analyzer, 'revenue_predictor')
        assert analyzer.revenue_predictor.model is not None  # Model should be trained
    
    def test_analyze_property(self, analyzer):
        """Test single property analysis"""
        test_address = TEST_CONFIG['test_addresses'][0]
        
        analysis = analyzer.analyze_property(test_address)
        
        # Check analysis structure
        required_sections = [
            'property_details', 'location_analysis', 'rental_comparables',
            'revenue_prediction', 'financial_metrics', 'risk_assessment',
            'investment_recommendation'
        ]
        
        for section in required_sections:
            assert section in analysis
        
        # Check property details
        prop = analysis['property_details']
        assert prop['address'] == test_address
        assert 'bedrooms' in prop
        assert 'sqft' in prop
        
        # Check revenue prediction
        rev = analysis['revenue_prediction']
        assert 'predicted_monthly_rent' in rev
        assert 'annual_revenue' in rev
        assert rev['predicted_monthly_rent'] > 0
        
        # Check financial metrics
        fin = analysis['financial_metrics']
        assert 'gross_rental_yield' in fin
        assert 'net_rental_yield' in fin
        assert fin['gross_rental_yield'] > 0
        
        # Check recommendation
        rec = analysis['investment_recommendation']
        assert 'recommendation' in rec
        assert rec['recommendation'] in ['STRONG BUY', 'BUY', 'HOLD', 'WEAK HOLD', 'AVOID']
    
    def test_generate_detailed_report(self, analyzer):
        """Test report generation"""
        test_address = TEST_CONFIG['test_addresses'][0]
        analysis = analyzer.analyze_property(test_address)
        
        report = analyzer.generate_detailed_report(analysis)
        
        assert isinstance(report, str)
        assert len(report) > 1000  # Should be a substantial report
        assert 'PROPERTY OVERVIEW' in report
        assert 'FINANCIAL PROJECTIONS' in report
        assert 'INVESTMENT RECOMMENDATION' in report
        assert test_address in report
    
    def test_batch_analyze_properties(self, analyzer):
        """Test batch property analysis"""
        test_addresses = TEST_CONFIG['test_addresses'][:2]  # Limit for testing
        
        results = analyzer.batch_analyze_properties(test_addresses)
        
        assert isinstance(results, pd.DataFrame)
        assert len(results) == len(test_addresses)
        
        # Check required columns
        required_cols = [
            'address', 'predicted_monthly_rent', 'gross_yield', 
            'recommendation', 'overall_risk'
        ]
        
        for col in required_cols:
            assert col in results.columns
    
    def test_rank_investment_opportunities(self, analyzer):
        """Test investment opportunity ranking"""
        # Create test data
        test_data = pd.DataFrame({
            'address': ['Address 1', 'Address 2', 'Address 3'],
            'predicted_monthly_rent': [4000, 5000, 3500],
            'gross_yield': [4.5, 5.2, 3.8],
            'monthly_cash_flow': [500, 800, 200],
            'location_score': [75, 85, 70],
            'overall_risk': ['Low', 'Medium', 'High']
        })
        
        ranked = analyzer.rank_investment_opportunities(test_data)
        
        assert isinstance(ranked, pd.DataFrame)
        assert 'rank' in ranked.columns
        assert 'investment_score' in ranked.columns
        
        # Check ranking order (rank 1 should be best)
        assert ranked.iloc[0]['rank'] == 1
        assert ranked['rank'].is_monotonic_increasing
    
    def test_simulate_property_data(self, analyzer):
        """Test property data simulation"""
        test_address = "123 Test Street, NY"
        
        prop_data = analyzer._simulate_property_data(test_address)
        
        # Check required fields
        required_fields = [
            'address', 'latitude', 'longitude', 'property_type',
            'bedrooms', 'bathrooms', 'sqft', 'year_built', 'last_sale_price'
        ]
        
        for field in required_fields:
            assert field in prop_data
        
        # Check data types and ranges
        assert prop_data['address'] == test_address
        assert 40.6 <= prop_data['latitude'] <= 40.9  # NYC latitude range
        assert -74.1 <= prop_data['longitude'] <= -73.7  # NYC longitude range
        assert 1 <= prop_data['bedrooms'] <= 4
        assert prop_data['sqft'] > 0
    
    def test_simulate_location_features(self, analyzer):
        """Test location features simulation"""
        lat, lng = TEST_CONFIG['test_coordinates']['upper_west_side']
        
        loc_features = analyzer._simulate_location_features(lat, lng)
        
        # Check required fields
        required_fields = [
            'crime_score', 'transit_score', 'amenity_score', 'walkability_score',
            'distance_to_subway', 'distance_to_manhattan', 'neighborhood'
        ]
        
        for field in required_fields:
            assert field in loc_features
        
        # Check score ranges
        score_fields = ['crime_score', 'transit_score', 'amenity_score', 'walkability_score']
        for field in score_fields:
            assert 0 <= loc_features[field] <= 100
    
    def test_get_model_info(self, analyzer):
        """Test model information retrieval"""
        model_info = analyzer.get_model_info()
        
        assert isinstance(model_info, dict)
        assert 'model_type' in model_info
        assert 'model_metrics' in model_info
        assert 'feature_importance' in model_info
        
        # Model should be trained
        assert model_info['model_type'] != 'Not trained'
    
    def test_edge_cases(self, analyzer):
        """Test edge cases and error handling"""
        # Test empty batch analysis
        empty_results = analyzer.batch_analyze_properties([])
        assert empty_results.empty
        
        # Test ranking empty dataframe
        empty_ranked = analyzer.rank_investment_opportunities(pd.DataFrame())
        assert empty_ranked.empty
    
    @pytest.mark.integration
    def test_full_workflow(self, analyzer):
        """Integration test for complete workflow"""
        test_address = TEST_CONFIG['test_addresses'][0]
        
        # Analyze property
        analysis = analyzer.analyze_property(test_address)
        
        # Generate report
        report = analyzer.generate_detailed_report(analysis)
        
        # Check workflow completed successfully
        assert analysis is not None
        assert report is not None
        assert len(report) > 0
        
        # Check key metrics are reasonable
        monthly_rent = analysis['revenue_prediction']['predicted_monthly_rent']
        gross_yield = analysis['financial_metrics']['gross_rental_yield']
        
        assert 2000 <= monthly_rent <= 15000  # Reasonable NYC rent
        assert 1 <= gross_yield <= 10  # Reasonable yield range
