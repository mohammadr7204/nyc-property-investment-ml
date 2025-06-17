"""
Test suite for NYC Property Investment ML system
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

# Test configuration
TEST_CONFIG = {
    'demo_api_key': 'demo-api-key',
    'test_addresses': [
        '350 Central Park West, New York, NY',
        '123 West 86th Street, New York, NY',
        '456 East 74th Street, New York, NY'
    ],
    'test_coordinates': {
        'upper_west_side': (40.7880, -73.9760),
        'upper_east_side': (40.7691, -73.9563),
        'soho': (40.7230, -73.9977)
    }
}

class TestCompleteSystem:
    """Integration tests for the complete system"""
    
    def test_system_imports(self):
        """Test that all core modules can be imported"""
        from analyzer import NYCPropertyInvestmentAnalyzer
        from data_pipeline import NYCPropertyDataPipeline
        from ml_model import NYCRevenuePredictor
        
        assert NYCPropertyInvestmentAnalyzer is not None
        assert NYCPropertyDataPipeline is not None
        assert NYCRevenuePredictor is not None

    def test_analyzer_initialization(self):
        """Test analyzer initializes correctly"""
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        analyzer = NYCPropertyInvestmentAnalyzer(TEST_CONFIG['demo_api_key'])
        assert analyzer.google_api_key == TEST_CONFIG['demo_api_key']
        assert hasattr(analyzer, 'data_pipeline')
        assert hasattr(analyzer, 'revenue_predictor')

    @pytest.mark.integration
    def test_basic_property_analysis(self):
        """Test basic property analysis workflow"""
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        analyzer = NYCPropertyInvestmentAnalyzer(TEST_CONFIG['demo_api_key'])
        test_address = TEST_CONFIG['test_addresses'][0]
        
        analysis = analyzer.analyze_property(test_address)
        
        # Check analysis structure
        required_sections = [
            'property_details', 'location_analysis', 'rental_comparables',
            'revenue_prediction', 'financial_metrics', 'risk_assessment',
            'investment_recommendation'
        ]
        
        for section in required_sections:
            assert section in analysis, f"Missing section: {section}"
        
        # Check specific values are reasonable
        monthly_rent = analysis['revenue_prediction']['predicted_monthly_rent']
        assert 2000 <= monthly_rent <= 15000, f"Unreasonable rent: ${monthly_rent}"
        
        gross_yield = analysis['financial_metrics']['gross_rental_yield']
        assert 1 <= gross_yield <= 10, f"Unreasonable yield: {gross_yield}%"

    def test_enhanced_validation(self):
        """Test enhanced validation features"""
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        analyzer = NYCPropertyInvestmentAnalyzer(TEST_CONFIG['demo_api_key'])
        
        # Test valid address
        valid_address = TEST_CONFIG['test_addresses'][0]
        result = analyzer.analyze_property(valid_address, use_validation=True)
        
        assert 'error' not in result
        assert 'data_quality' in result
        assert result['data_quality']['overall_score'] >= 0
        
        # Test invalid address
        invalid_address = "invalid"
        result = analyzer.analyze_property(invalid_address, use_validation=True)
        
        assert 'error' in result
        assert 'Invalid address format' in result['error']

    def test_data_pipeline_features(self):
        """Test data pipeline enhanced features"""
        from data_pipeline import NYCPropertyDataPipeline
        
        pipeline = NYCPropertyDataPipeline(TEST_CONFIG['demo_api_key'])
        
        # Test address standardization
        standardized = pipeline.standardize_address("350 CPW, NYC")
        assert len(standardized) > 5
        assert isinstance(standardized, str)
        
        # Test address similarity
        similarity = pipeline.calculate_address_similarity(
            "350 Central Park West, NY", 
            "350 CPW, New York"
        )
        assert 0 <= similarity <= 1
        assert similarity > 0.5  # Should be reasonably similar
        
        # Test coordinate validation
        test_coords = TEST_CONFIG['test_coordinates']['upper_west_side']
        validation = pipeline.validate_coordinates_against_address(
            TEST_CONFIG['test_addresses'][0], 
            test_coords[0], test_coords[1]
        )
        assert 'is_valid' in validation
        assert 'confidence' in validation
        assert isinstance(validation['confidence'], float)

    def test_ml_model_training(self):
        """Test ML model training and prediction"""
        from ml_model import NYCRevenuePredictor
        
        predictor = NYCRevenuePredictor()
        
        # Generate training data
        df = predictor.generate_synthetic_training_data(200)
        assert len(df) == 200
        assert 'monthly_rent' in df.columns
        
        # Prepare features
        X, y = predictor.prepare_features(df)
        assert len(X) == len(y) == 200
        assert not X.empty
        
        # Train model
        metrics = predictor.train_model(X, y)
        assert 'r2' in predictor.model_metrics
        assert predictor.model_metrics['r2'] > 0.5  # Reasonable performance
        
        # Test prediction
        test_features = {
            'bedrooms': 2,
            'bathrooms': 2.0,
            'sqft': 1000,
            'year_built': 1990,
            'last_sale_price': 1500000,
            'property_type': 'Condo',
            'crime_score': 85,
            'transit_score': 90,
            'amenity_score': 75,
            'neighborhood': 'Upper West Side'
        }
        
        prediction = predictor.predict_revenue(test_features)
        assert 'predicted_monthly_rent' in prediction
        assert 2000 <= prediction['predicted_monthly_rent'] <= 15000

    def test_batch_analysis(self):
        """Test batch property analysis"""
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        analyzer = NYCPropertyInvestmentAnalyzer(TEST_CONFIG['demo_api_key'])
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

    def test_report_generation(self):
        """Test report generation"""
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        analyzer = NYCPropertyInvestmentAnalyzer(TEST_CONFIG['demo_api_key'])
        test_address = TEST_CONFIG['test_addresses'][0]
        
        analysis = analyzer.analyze_property(test_address)
        report = analyzer.generate_detailed_report(analysis)
        
        assert isinstance(report, str)
        assert len(report) > 1000  # Should be substantial
        assert 'PROPERTY OVERVIEW' in report
        assert 'FINANCIAL PROJECTIONS' in report
        assert test_address in report

    def test_web_app_functionality(self):
        """Test web application can be imported and initialized"""
        try:
            # Add web_app to path
            sys.path.insert(0, str(project_root / 'web_app'))
            
            import app
            assert hasattr(app, 'app')  # Flask app instance
            assert hasattr(app, 'get_analyzer')
            
        except ImportError:
            pytest.skip("Web app dependencies not available")

    def test_diagnostic_tools(self):
        """Test diagnostic tools are available"""
        diagnostic_scripts = [
            'scripts/diagnose_data_issues.py',
            'scripts/quick_fix_data_issues.py',
            'scripts/demo_real_data.py',
            'scripts/verify_integration.py'
        ]
        
        for script in diagnostic_scripts:
            script_path = project_root / script
            assert script_path.exists(), f"Missing diagnostic script: {script}"

    def test_documentation_completeness(self):
        """Test that required documentation exists"""
        required_docs = [
            'README.md',
            'QUICK_START.md',
            'docs/API.md',
            'docs/REAL_DATA_INTEGRATION.md'
        ]
        
        for doc in required_docs:
            doc_path = project_root / doc
            assert doc_path.exists(), f"Missing documentation: {doc}"
            assert doc_path.stat().st_size > 1000, f"Documentation too short: {doc}"

    def test_configuration_files(self):
        """Test configuration files are present"""
        config_files = [
            '.env.example',
            'requirements.txt',
            'web_requirements.txt',
            'pyproject.toml'
        ]
        
        for config_file in config_files:
            config_path = project_root / config_file
            assert config_path.exists(), f"Missing config file: {config_file}"

class TestDataQuality:
    """Test data quality assessment features"""
    
    def test_data_quality_scoring(self):
        """Test data quality scoring system"""
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        analyzer = NYCPropertyInvestmentAnalyzer(TEST_CONFIG['demo_api_key'])
        test_address = TEST_CONFIG['test_addresses'][0]
        
        analysis = analyzer.analyze_property(test_address)
        
        assert 'data_quality' in analysis
        quality = analysis['data_quality']
        
        assert 'overall_score' in quality
        assert 0 <= quality['overall_score'] <= 100
        assert 'confidence_level' in quality
        assert quality['confidence_level'] in ['high', 'medium', 'low']

    def test_data_source_transparency(self):
        """Test data source transparency features"""
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        analyzer = NYCPropertyInvestmentAnalyzer(TEST_CONFIG['demo_api_key'])
        test_address = TEST_CONFIG['test_addresses'][0]
        
        analysis = analyzer.analyze_property(test_address, use_validation=True)
        
        if 'data_sources' in analysis:
            sources = analysis['data_sources']
            assert isinstance(sources, dict)
            
            # Should have information about different data types
            expected_source_types = [
                'property_data', 'crime_data', 'transit_data', 'amenity_data'
            ]
            
            # At least some source types should be present
            found_sources = sum(1 for source_type in expected_source_types 
                              if source_type in sources)
            assert found_sources >= 2

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        analyzer = NYCPropertyInvestmentAnalyzer(TEST_CONFIG['demo_api_key'])
        
        # Test empty address
        result = analyzer.analyze_property("", use_validation=True)
        assert 'error' in result
        
        # Test very short address
        result = analyzer.analyze_property("123", use_validation=True)
        assert 'error' in result
        
        # Test non-NYC address
        result = analyzer.analyze_property("123 Main St, Boston, MA", use_validation=True)
        # Should either work with warnings or return an error
        assert 'error' in result or 'warnings' in result

    def test_empty_batch_analysis(self):
        """Test batch analysis with empty input"""
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        analyzer = NYCPropertyInvestmentAnalyzer(TEST_CONFIG['demo_api_key'])
        
        # Test empty list
        results = analyzer.batch_analyze_properties([])
        assert isinstance(results, pd.DataFrame)
        assert results.empty

if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])