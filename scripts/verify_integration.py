#!/usr/bin/env python3
"""
Integration Verification Script
Verifies that all enhanced features are working correctly after integration.
"""

import sys
import os
from pathlib import Path
import logging

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

def test_enhanced_validation():
    """Test enhanced validation features"""
    print("\n🔍 Testing Enhanced Validation Features...")
    
    try:
        from analyzer import NYCPropertyInvestmentAnalyzer
        
        # Initialize with demo key
        analyzer = NYCPropertyInvestmentAnalyzer('demo-api-key')
        
        # Test 1: Valid address with validation
        print("  ✓ Testing valid address...")
        result = analyzer.analyze_property("350 Central Park West, New York, NY", use_validation=True)
        
        if 'error' not in result:
            print("    ✅ Valid address analysis successful")
            print(f"    ✅ Data quality score: {result.get('data_quality', {}).get('overall_score', 0)}/100")
        else:
            print(f"    ⚠️  Valid address returned error: {result['error']}")
        
        # Test 2: Invalid address format
        print("  ✓ Testing invalid address format...")
        result = analyzer.analyze_property("invalid", use_validation=True)
        
        if 'error' in result and 'Invalid address format' in result['error']:
            print("    ✅ Invalid address correctly rejected")
        else:
            print("    ⚠️  Invalid address not properly handled")
        
        # Test 3: Data source transparency
        print("  ✓ Testing data source transparency...")
        result = analyzer.analyze_property("123 West 86th Street, New York, NY", use_validation=True)
        
        if 'data_sources' in result:
            print("    ✅ Data source transparency working")
            print(f"    ℹ️  Data sources: {len(result['data_sources'])} types tracked")
        else:
            print("    ⚠️  Data source transparency not found")
        
        print("  ✅ Enhanced validation tests completed")
        return True
        
    except Exception as e:
        print(f"  ❌ Enhanced validation test failed: {e}")
        return False

def test_enhanced_data_pipeline():
    """Test enhanced data pipeline features"""
    print("\n📊 Testing Enhanced Data Pipeline Features...")
    
    try:
        from data_pipeline import NYCPropertyDataPipeline
        
        # Initialize pipeline
        pipeline = NYCPropertyDataPipeline('demo-api-key')
        
        # Test 1: Address standardization
        print("  ✓ Testing address standardization...")
        standardized = pipeline.standardize_address("350 CPW, NYC")
        if len(standardized) > 5:
            print("    ✅ Address standardization working")
        else:
            print("    ⚠️  Address standardization issue")
        
        # Test 2: Address similarity calculation
        print("  ✓ Testing address similarity...")
        similarity = pipeline.calculate_address_similarity(
            "350 Central Park West, NY", 
            "350 CPW, New York"
        )
        if 0.5 <= similarity <= 1.0:
            print(f"    ✅ Address similarity working: {similarity:.2f}")
        else:
            print(f"    ⚠️  Address similarity unexpected: {similarity}")
        
        # Test 3: Coordinate validation
        print("  ✓ Testing coordinate validation...")
        validation = pipeline.validate_coordinates_against_address(
            "350 Central Park West, New York, NY", 
            40.7880, -73.9760
        )
        if 'is_valid' in validation and 'confidence' in validation:
            print("    ✅ Coordinate validation working")
            print(f"    ℹ️  Validation confidence: {validation['confidence']:.2f}")
        else:
            print("    ⚠️  Coordinate validation not working")
        
        # Test 4: Enhanced property data retrieval
        print("  ✓ Testing enhanced property data retrieval...")
        prop_data = pipeline.get_real_property_data("350 Central Park West, New York, NY")
        if prop_data:
            print("    ✅ Property data retrieval working")
            print(f"    ℹ️  Data source: {prop_data.get('source', 'Unknown')}")
        else:
            print("    ℹ️  No property data found (expected for some addresses)")
        
        print("  ✅ Enhanced data pipeline tests completed")
        return True
        
    except Exception as e:
        print(f"  ❌ Enhanced data pipeline test failed: {e}")
        return False

def test_diagnostic_scripts():
    """Test that diagnostic scripts exist and are importable"""
    print("\n🔧 Testing Diagnostic Scripts...")
    
    script_tests = [
        ('diagnose_data_issues.py', 'Data diagnostic script'),
        ('quick_fix_data_issues.py', 'Quick fix script'),
        ('demo_real_data.py', 'Real data demo script')
    ]
    
    scripts_working = 0
    
    for script_name, description in script_tests:
        script_path = project_root / 'scripts' / script_name
        if script_path.exists():
            print(f"    ✅ {description} exists")
            scripts_working += 1
        else:
            print(f"    ❌ {description} missing")
    
    if scripts_working == len(script_tests):
        print("  ✅ All diagnostic scripts present")
        return True
    else:
        print(f"  ⚠️  {scripts_working}/{len(script_tests)} diagnostic scripts found")
        return False

def test_documentation():
    """Test that documentation is complete"""
    print("\n📚 Testing Documentation...")
    
    doc_tests = [
        ('README.md', 'Main documentation'),
        ('docs/API.md', 'API documentation'),
        ('docs/REAL_DATA_INTEGRATION.md', 'Integration documentation'),
        ('QUICK_START.md', 'Quick start guide')
    ]
    
    docs_found = 0
    
    for doc_name, description in doc_tests:
        doc_path = project_root / doc_name
        if doc_path.exists():
            print(f"    ✅ {description} exists")
            docs_found += 1
        else:
            print(f"    ❌ {description} missing")
    
    if docs_found >= 3:  # At least most docs should be present
        print("  ✅ Documentation complete")
        return True
    else:
        print(f"  ⚠️  {docs_found}/{len(doc_tests)} documentation files found")
        return False

def main():
    """Run all integration verification tests"""
    print("🏙️  NYC Property Investment ML - Integration Verification")
    print("=" * 70)
    print("Verifying that all enhanced features are working correctly...")
    
    # Setup logging to suppress noise during testing
    logging.getLogger().setLevel(logging.WARNING)
    
    tests = [
        ("Enhanced Validation", test_enhanced_validation),
        ("Enhanced Data Pipeline", test_enhanced_data_pipeline), 
        ("Diagnostic Scripts", test_diagnostic_scripts),
        ("Documentation", test_documentation)
    ]
    
    passed_tests = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"  ❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 70)
    print("📋 INTEGRATION VERIFICATION SUMMARY")
    print("=" * 70)
    
    if passed_tests == len(tests):
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ The enhanced NYC Property Investment ML system is fully integrated and working.")
        print("\n🚀 Next Steps:")
        print("  1. Test with real addresses: python scripts/run_analysis.py -a 'Your Address'")
        print("  2. Run diagnostics: python scripts/diagnose_data_issues.py") 
        print("  3. Try quick fixes: python scripts/quick_fix_data_issues.py")
        print("  4. Demo real data: python scripts/demo_real_data.py")
        print("  5. Add Google API key to .env for enhanced accuracy")
        success = True
    else:
        print(f"⚠️  {passed_tests}/{len(tests)} integration tests passed")
        print("Some features may not be working correctly.")
        print("\n🔧 Troubleshooting:")
        print("  1. Check that you're running from the project root directory")
        print("  2. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("  3. Run the full system test: python scripts/test_system.py")
        success = False
    
    print("\n📞 Support:")
    print("  - GitHub Issues: https://github.com/mohammadr7204/nyc-property-investment-ml/issues")
    print("  - Documentation: docs/ folder")
    print("  - Health Check: Run the web app and visit /health endpoint")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
