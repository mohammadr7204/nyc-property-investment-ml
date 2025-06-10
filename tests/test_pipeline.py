"""
Unit tests for the data pipeline module
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_pipeline import NYCPropertyDataPipeline, PropertyData
from tests import TEST_CONFIG

class TestNYCPropertyDataPipeline:
    """Test cases for the data pipeline"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.pipeline = NYCPropertyDataPipeline(TEST_CONFIG['demo_api_key'])
        self.test_coords = TEST_CONFIG['test_coordinates']['upper_west_side']
    
    def test_pipeline_initialization(self):
        """Test pipeline initializes correctly"""
        assert self.pipeline.google_api_key == TEST_CONFIG['demo_api_key']
        assert hasattr(self.pipeline, 'session')
        assert hasattr(self.pipeline, 'logger')
    
    def test_collect_crime_data(self):
        """Test crime data collection"""
        lat, lng = self.test_coords
        crime_score = self.pipeline.collect_crime_data(lat, lng)
        
        assert isinstance(crime_score, float)
        assert 0 <= crime_score <= 100
    
    def test_get_google_places_amenities(self):
        """Test amenities data collection"""
        lat, lng = self.test_coords
        amenities = self.pipeline.get_google_places_amenities(lat, lng)
        
        assert isinstance(amenities, dict)
        assert 'score' in amenities
        assert 'counts' in amenities
        assert 0 <= amenities['score'] <= 100
    
    def test_calculate_transit_score(self):
        """Test transit score calculation"""
        lat, lng = self.test_coords
        transit_score = self.pipeline.calculate_transit_score(lat, lng)
        
        assert isinstance(transit_score, float)
        assert 0 <= transit_score <= 100
    
    def test_collect_rental_comparables(self):
        """Test rental comparables collection"""
        lat, lng = self.test_coords
        comps = self.pipeline.collect_rental_comparables(lat, lng, 2)
        
        assert isinstance(comps, list)
        assert len(comps) >= 2  # Should return at least 2 comparables
        
        if comps:
            comp = comps[0]
            required_fields = ['address', 'monthly_rent', 'bedrooms', 'sqft']
            for field in required_fields:
                assert field in comp
    
    def test_property_data_structure(self):
        """Test PropertyData dataclass"""
        prop_data = PropertyData(
            address="123 Test St, NY",
            latitude=40.7589,
            longitude=-73.9851,
            property_type="Condo",
            bedrooms=2,
            bathrooms=2.0,
            sqft=1000,
            year_built=1990,
            last_sale_price=1500000,
            last_sale_date="2024-01-01"
        )
        
        assert prop_data.address == "123 Test St, NY"
        assert prop_data.bedrooms == 2
        assert prop_data.sqft == 1000
    
    def test_neighborhood_determination(self):
        """Test neighborhood determination logic"""
        # Test different NYC coordinates
        coords_tests = [
            (40.7880, -73.9760),  # Upper West Side area
            (40.7691, -73.9563),  # Upper East Side area  
            (40.7230, -73.9977),  # SoHo area
            (40.7060, -74.0130),  # Financial District area
        ]
        
        for lat, lng in coords_tests:
            neighborhood = self.pipeline._determine_neighborhood(lat, lng)
            assert isinstance(neighborhood, str)
            assert len(neighborhood) > 0
    
    @pytest.mark.slow
    def test_process_property_integration(self):
        """Integration test for processing a complete property"""
        prop_data = PropertyData(
            address="123 West 86th Street, New York, NY",
            latitude=40.7880,
            longitude=-73.9760,
            property_type="Condo",
            bedrooms=2,
            bathrooms=2.0,
            sqft=1200,
            year_built=1990,
            last_sale_price=1500000,
            last_sale_date="2024-01-01"
        )
        
        result = self.pipeline.process_property(prop_data)
        
        # Check result structure
        assert 'property' in result
        assert 'location_features' in result
        assert 'rental_comps' in result
        assert 'avg_comp_rent' in result
        
        # Check location features
        loc_features = result['location_features']
        required_loc_fields = [
            'crime_score', 'walkability_score', 'transit_score', 
            'amenity_score', 'distance_to_subway', 'distance_to_manhattan'
        ]
        
        for field in required_loc_fields:
            assert field in loc_features
            if field.endswith('_score'):
                assert 0 <= loc_features[field] <= 100
