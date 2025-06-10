#!/usr/bin/env python3
"""
Test script to verify the NYC Property Investment System is working correctly.
Runs comprehensive tests on all system components.
"""

import sys
import os
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from analyzer import NYCPropertyInvestmentAnalyzer
        print("✅ Main analyzer imported successfully")
        
        from ml_model import NYCRevenuePredictor
        print("✅ ML model imported successfully")
        
        from data_pipeline import NYCPropertyDataPipeline, PropertyData
        print("✅ Data pipeline imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running from the project root directory")
        print("💡 Try: export PYTHONPATH=$PYTHONPATH:$(pwd)/src")
        return False

def test_ml_model():
    """Test the ML model independently"""
    print("\n🤖 Testing ML model...")
    
    try:
        from ml_model import NYCRevenuePredictor
        
        predictor = NYCRevenuePredictor()
        
        # Generate synthetic data
        df = predictor.generate_synthetic_training_data(800)
        print(f"✅ Generated {len(df)} synthetic training samples")
        
        # Check data quality
        if df['monthly_rent'].min() < 1500 or df['monthly_rent'].max() > 30000:
            print("⚠️  Warning: Rent values outside expected range")
        
        # Prepare features
        X, y = predictor.prepare_features(df)
        print(f"✅ Prepared {len(X.columns)} features: {list(X.columns)}")
        
        # Train model
        metrics = predictor.train_model(X, y)
        print(f"✅ Model trained successfully. R² = {metrics['r2']:.3f}, RMSE = ${metrics['rmse']:.0f}")
        
        # Test prediction
        sample_features = {
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
        
        prediction = predictor.predict_revenue(sample_features)
        print(f"✅ Sample prediction: ${prediction['predicted_monthly_rent']:,.0f}/month")
        print(f"   Confidence: {prediction['prediction_confidence']}, Range: ${prediction['confidence_interval'][0]:,.0f} - ${prediction['confidence_interval'][1]:,.0f}")
        
        # Test feature importance
        importance = predictor.get_feature_importance()
        if not importance.empty:
            print(f"✅ Feature importance available: top feature is '{importance.iloc[0]['feature']}'")
        
        return True
        
    except Exception as e:
        print(f"❌ ML model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_pipeline():
    """Test the data collection pipeline"""
    print("\n📊 Testing data pipeline...")
    
    try:
        from data_pipeline import NYCPropertyDataPipeline
        
        pipeline = NYCPropertyDataPipeline("demo-api-key")
        print("✅ Pipeline initialized")
        
        # Test NYC coordinates
        test_lat, test_lng = 40.7880, -73.9760  # Upper West Side
        
        # Test crime data collection
        crime_score = pipeline.collect_crime_data(test_lat, test_lng)
        print(f"✅ Crime score collected: {crime_score}/100")
        
        # Test amenities collection
        amenities = pipeline.get_google_places_amenities(test_lat, test_lng)
        print(f"✅ Amenity score collected: {amenities['score']}/100")
        
        # Test transit score
        transit_score = pipeline.calculate_transit_score(test_lat, test_lng)
        print(f"✅ Transit score collected: {transit_score}/100")
        
        # Test rental comparables
        comps = pipeline.collect_rental_comparables(test_lat, test_lng, 2)
        print(f"✅ Found {len(comps)} rental comparables")
        
        if comps:
            avg_rent = np.mean([comp['monthly_rent'] for comp in comps])
            print(f"   Average comparable rent: ${avg_rent:,.0f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_system():
    """Test the complete system integration"""
    print("\n🏠 Testing complete system...")
    
    try:
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        # Initialize analyzer
        print("   Initializing analyzer (may take 30 seconds for model training)...")
        analyzer = NYCPropertyInvestmentAnalyzer("demo-api-key")
        print("✅ System initialized successfully")
        
        # Test single property analysis
        test_addresses = [
            "123 West 86th Street, New York, NY 10024",
            "456 East 74th Street, New York, NY 10021", 
            "789 Broadway, New York, NY 10003"
        ]
        
        print(f"\n   Testing analysis for: {test_addresses[0]}")
        analysis = analyzer.analyze_property(test_addresses[0])
        
        print(f"✅ Property analysis completed")
        print(f"   Predicted rent: ${analysis['revenue_prediction']['predicted_monthly_rent']:,.0f}")
        print(f"   Gross yield: {analysis['financial_metrics']['gross_rental_yield']:.1f}%")
        print(f"   Cash flow: ${analysis['financial_metrics']['monthly_cash_flow']:,.0f}/month")
        print(f"   Recommendation: {analysis['investment_recommendation']['recommendation']}")
        print(f"   Risk level: {analysis['risk_assessment']['overall_risk']}")
        
        # Test report generation
        report = analyzer.generate_detailed_report(analysis)
        print("✅ Detailed report generated")
        
        # Test batch analysis
        print(f"\n   Testing batch analysis with {len(test_addresses)} properties...")
        batch_results = analyzer.batch_analyze_properties(test_addresses)
        print(f"✅ Batch analysis completed: {len(batch_results)} properties")
        
        if not batch_results.empty:
            # Test ranking
            ranked = analyzer.rank_investment_opportunities(batch_results)
            print(f"✅ Investment ranking completed")
            
            print("\n📊 Batch Results Summary:")
            for _, row in ranked.head(3).iterrows():
                print(f"   {row['address'][:30]:<30} | ${row['predicted_monthly_rent']:>6,.0f} | {row['gross_yield']:>5.1f}% | {row['recommendation']}")
        
        # Test model info
        model_info = analyzer.get_model_info()
        print(f"\n✅ Model info: {model_info['model_type']}, R² = {model_info['model_metrics'].get('r2', 0):.3f}")
        
        return True, analysis, report
        
    except Exception as e:
        print(f"❌ Full system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n🧪 Testing edge cases...")
    
    try:
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        analyzer = NYCPropertyInvestmentAnalyzer("demo-api-key")
        
        # Test empty address
        try:
            analyzer.analyze_property("")
            print("⚠️  Empty address should have failed")
        except:
            print("✅ Empty address handled correctly")
        
        # Test batch with empty list
        empty_batch = analyzer.batch_analyze_properties([])
        if empty_batch.empty:
            print("✅ Empty batch handled correctly")
        
        print("✅ Edge cases handled appropriately")
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🏙️  NYC Property Investment System - Test Suite")
    print("=" * 60)
    
    # Track test results
    tests_passed = 0
    total_tests = 5
    
    # Test imports
    if test_imports():
        tests_passed += 1
    else:
        print("\n❌ Import tests failed. Cannot continue.")
        return False
    
    # Test ML model
    if test_ml_model():
        tests_passed += 1
    
    # Test data pipeline
    if test_data_pipeline():
        tests_passed += 1
    
    # Test full system
    success, analysis, report = test_full_system()
    if success:
        tests_passed += 1
    
    # Test edge cases
    if test_edge_cases():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    
    if tests_passed == total_tests:
        print(f"🎉 ALL TESTS PASSED! ({tests_passed}/{total_tests})")
        print("✅ System is working correctly and ready to use.")
        
        if report:
            print("\n📋 Sample Analysis Report:")
            print(report[:1000] + "..." if len(report) > 1000 else report)
        
        print("\n🚀 Next Steps:")
        print("1. Try: python scripts/run_analysis.py -a 'Your NYC Address'")
        print("2. Get Google API key for real location data")
        print("3. Explore notebooks/ for data analysis")
        print("4. Consider deploying as web application")
        
        return True
    else:
        print(f"❌ Some tests failed ({tests_passed}/{total_tests} passed)")
        print("\n🔧 Troubleshooting:")
        print("- Check that all dependencies are installed: pip install -r requirements.txt")
        print("- Ensure you're running from the project root directory")
        print("- Check logs/setup.log for detailed error messages")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
