#!/usr/bin/env python3
"""
Data Source Diagnostic Script
Identifies and diagnoses data source accuracy issues including:
- Address matching problems
- Coordinate validation failures
- Data quality assessment
- API response validation
"""

import sys
import os
from pathlib import Path
import time
import logging
from typing import Dict, List, Optional
import traceback

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from data_pipeline import NYCPropertyDataPipeline
from analyzer import NYCPropertyInvestmentAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataSourceDiagnostic:
    """Comprehensive data source diagnostic tool"""
    
    def __init__(self, google_api_key: str = 'demo-api-key'):
        self.api_key = google_api_key
        self.pipeline = NYCPropertyDataPipeline(google_api_key)
        self.analyzer = NYCPropertyInvestmentAnalyzer(google_api_key)
        
    def diagnose_address_issues(self, addresses: List[str]) -> Dict:
        """Diagnose address matching and validation issues"""
        
        print("\n" + "="*80)
        print("🔍 DIAGNOSING ADDRESS MATCHING ISSUES")
        print("="*80)
        
        results = {
            'addresses_tested': len(addresses),
            'successful_geocoding': 0,
            'failed_geocoding': 0,
            'validation_failures': 0,
            'coordinate_mismatches': 0,
            'property_data_found': 0,
            'issues': []
        }
        
        for i, address in enumerate(addresses, 1):
            print(f"\n[{i}/{len(addresses)}] Testing: {address}")
            print("-" * 60)
            
            try:
                # Step 1: Basic address validation
                is_valid = self.analyzer._basic_address_validation(address)
                print(f"✓ Basic validation: {'PASS' if is_valid else 'FAIL'}")
                
                if not is_valid:
                    results['issues'].append(f"Basic validation failed for: {address}")
                    continue
                
                # Step 2: Geocoding test
                coordinates = self.pipeline.geocode_address(address)
                if coordinates:
                    results['successful_geocoding'] += 1
                    print(f"✓ Geocoding: SUCCESS ({coordinates['lat']:.4f}, {coordinates['lng']:.4f})")
                    print(f"  Formatted: {coordinates['formatted_address']}")
                    print(f"  Quality: {coordinates.get('data_quality', 'unknown')}")
                else:
                    results['failed_geocoding'] += 1
                    results['issues'].append(f"Geocoding failed for: {address}")
                    print("✗ Geocoding: FAILED")
                    continue
                
                # Step 3: Coordinate validation
                validation = self.pipeline.validate_coordinates_against_address(
                    address, coordinates['lat'], coordinates['lng']
                )
                
                if validation['is_valid']:
                    print(f"✓ Coordinate validation: PASS (confidence: {validation['confidence']:.2f})")
                else:
                    results['validation_failures'] += 1
                    results['coordinate_mismatches'] += 1
                    print(f"✗ Coordinate validation: FAIL (confidence: {validation['confidence']:.2f})")
                    print(f"  Issues: {', '.join(validation['issues'])}")
                    results['issues'].extend(validation['issues'])
                
                # Step 4: Property data lookup test
                property_data = self.pipeline.get_real_property_data(address)
                if property_data:
                    results['property_data_found'] += 1
                    print(f"✓ Property data: FOUND (source: {property_data.get('source', 'unknown')})")
                    print(f"  Type: {property_data.get('property_type', 'unknown')}")
                    print(f"  Bedrooms: {property_data.get('bedrooms', 'unknown')}")
                else:
                    print("⚠ Property data: NOT FOUND (will use estimates)")
                
                # Step 5: Address similarity test with standardization
                standardized = self.pipeline.standardize_address(address)
                print(f"✓ Standardized: {standardized}")
                
                # Small delay to respect rate limits
                time.sleep(0.5)
                
            except Exception as e:
                print(f"✗ ERROR: {str(e)}")
                results['issues'].append(f"Exception for {address}: {str(e)}")
                
        print(f"\n" + "="*80)
        print("📊 ADDRESS DIAGNOSTIC SUMMARY")
        print("="*80)
        print(f"Total addresses tested: {results['addresses_tested']}")
        print(f"Successful geocoding: {results['successful_geocoding']}")
        print(f"Failed geocoding: {results['failed_geocoding']}")
        print(f"Coordinate validation failures: {results['validation_failures']}")
        print(f"Property data found: {results['property_data_found']}")
        print(f"Total issues: {len(results['issues'])}")
        
        if results['issues']:
            print(f"\n🚨 IDENTIFIED ISSUES:")
            for issue in results['issues'][:10]:  # Show first 10 issues
                print(f"  • {issue}")
            if len(results['issues']) > 10:
                print(f"  ... and {len(results['issues']) - 10} more")
        
        return results
    
    def test_location_data_accuracy(self, test_coordinates: List[tuple]) -> Dict:
        """Test location data collection accuracy"""
        
        print("\n" + "="*80)
        print("📍 TESTING LOCATION DATA ACCURACY")
        print("="*80)
        
        results = {
            'coordinates_tested': len(test_coordinates),
            'crime_data_success': 0,
            'transit_data_success': 0,
            'amenity_data_success': 0,
            'issues': []
        }
        
        for i, (name, lat, lng) in enumerate(test_coordinates, 1):
            print(f"\n[{i}/{len(test_coordinates)}] Testing: {name} ({lat:.4f}, {lng:.4f})")
            print("-" * 60)
            
            try:
                # Test crime data collection
                crime_score = self.pipeline.collect_crime_data(lat, lng)
                if 0 <= crime_score <= 100:
                    results['crime_data_success'] += 1
                    print(f"✓ Crime data: {crime_score:.1f}/100")
                else:
                    print(f"⚠ Crime data: {crime_score:.1f}/100 (out of range)")
                    results['issues'].append(f"Crime score out of range for {name}: {crime_score}")
                
                # Test transit data
                transit_score = self.pipeline.calculate_transit_score(lat, lng)
                if 0 <= transit_score <= 100:
                    results['transit_data_success'] += 1
                    print(f"✓ Transit data: {transit_score:.1f}/100")
                else:
                    print(f"⚠ Transit data: {transit_score:.1f}/100 (out of range)")
                    results['issues'].append(f"Transit score out of range for {name}: {transit_score}")
                
                # Test amenity data
                amenities = self.pipeline.get_google_places_amenities(lat, lng)
                if 'score' in amenities and 0 <= amenities['score'] <= 100:
                    results['amenity_data_success'] += 1
                    print(f"✓ Amenity data: {amenities['score']:.1f}/100 ({amenities.get('total_amenities', 0)} amenities)")
                else:
                    print(f"⚠ Amenity data: Invalid response")
                    results['issues'].append(f"Invalid amenity data for {name}")
                
                # Test real subway distance calculation
                try:
                    stations_df = self.pipeline.get_subway_stations()
                    if not stations_df.empty:
                        distance = self.pipeline._calculate_nearest_subway_distance(lat, lng, stations_df)
                        print(f"✓ Subway distance: {distance:.2f} miles")
                    else:
                        print(f"⚠ Subway stations: Data not loaded")
                        results['issues'].append(f"Subway station data unavailable for {name}")
                except Exception as e:
                    print(f"✗ Subway calculation error: {str(e)}")
                    results['issues'].append(f"Subway calculation failed for {name}: {str(e)}")
                
                # Small delay to respect rate limits
                time.sleep(1.0)
                
            except Exception as e:
                print(f"✗ ERROR: {str(e)}")
                results['issues'].append(f"Exception for {name}: {str(e)}")
        
        print(f"\n" + "="*80)
        print("📊 LOCATION DATA SUMMARY")
        print("="*80)
        print(f"Coordinates tested: {results['coordinates_tested']}")
        print(f"Crime data success: {results['crime_data_success']}")
        print(f"Transit data success: {results['transit_data_success']}")
        print(f"Amenity data success: {results['amenity_data_success']}")
        print(f"Issues found: {len(results['issues'])}")
        
        return results
    
    def test_api_connectivity(self) -> Dict:
        """Test API connectivity and response quality"""
        
        print("\n" + "="*80)
        print("🌐 TESTING API CONNECTIVITY")
        print("="*80)
        
        results = {
            'nyc_open_data': False,
            'google_geocoding': False,
            'google_places': False,
            'mta_data': False,
            'issues': []
        }
        
        # Test NYC Open Data
        try:
            test_url = "https://data.cityofnewyork.us/resource/5uac-w243.json"
            response = self.pipeline.session.get(test_url, params={"$limit": 1}, timeout=10)
            if response.status_code == 200:
                results['nyc_open_data'] = True
                print("✓ NYC Open Data: CONNECTED")
            else:
                print(f"✗ NYC Open Data: HTTP {response.status_code}")
                results['issues'].append(f"NYC Open Data HTTP error: {response.status_code}")
        except Exception as e:
            print(f"✗ NYC Open Data: CONNECTION FAILED - {str(e)}")
            results['issues'].append(f"NYC Open Data connection failed: {str(e)}")
        
        # Test Google Geocoding API
        if self.api_key != 'demo-api-key':
            try:
                test_coords = self.pipeline.geocode_address("350 Central Park West, New York, NY")
                if test_coords:
                    results['google_geocoding'] = True
                    print("✓ Google Geocoding API: CONNECTED")
                else:
                    print("✗ Google Geocoding API: NO RESPONSE")
                    results['issues'].append("Google Geocoding API returned no results")
            except Exception as e:
                print(f"✗ Google Geocoding API: FAILED - {str(e)}")
                results['issues'].append(f"Google Geocoding API failed: {str(e)}")
        else:
            print("⚠ Google Geocoding API: DEMO MODE (no API key)")
        
        # Test Google Places API
        if self.api_key != 'demo-api-key':
            try:
                test_amenities = self.pipeline.get_google_places_amenities(40.7880, -73.9760)
                if test_amenities and 'score' in test_amenities:
                    results['google_places'] = True
                    print("✓ Google Places API: CONNECTED")
                else:
                    print("✗ Google Places API: NO RESPONSE")
                    results['issues'].append("Google Places API returned no results")
            except Exception as e:
                print(f"✗ Google Places API: FAILED - {str(e)}")
                results['issues'].append(f"Google Places API failed: {str(e)}")
        else:
            print("⚠ Google Places API: DEMO MODE (no API key)")
        
        # Test MTA Data
        try:
            stations_df = self.pipeline.get_subway_stations()
            if not stations_df.empty and len(stations_df) > 400:
                results['mta_data'] = True
                print(f"✓ MTA Subway Data: CONNECTED ({len(stations_df)} stations)")
            else:
                print(f"✗ MTA Subway Data: INSUFFICIENT DATA ({len(stations_df)} stations)")
                results['issues'].append(f"MTA data insufficient: only {len(stations_df)} stations")
        except Exception as e:
            print(f"✗ MTA Subway Data: FAILED - {str(e)}")
            results['issues'].append(f"MTA data failed: {str(e)}")
        
        return results
    
    def run_full_diagnostic(self, test_addresses: List[str] = None) -> Dict:
        """Run comprehensive diagnostic on all data sources"""
        
        if test_addresses is None:
            test_addresses = [
                "350 Central Park West, New York, NY",
                "1 Wall Street, New York, NY",
                "123 West 86th Street, New York, NY",
                "456 East 74th Street, New York, NY",
                "789 Broadway, New York, NY",
                "350 CPW, NYC",  # Abbreviated format
                "123 Fake Street, NY",  # Non-existent
            ]
        
        test_coordinates = [
            ("Upper West Side", 40.7880, -73.9760),
            ("Financial District", 40.7074, -74.0113),
            ("SoHo", 40.7230, -73.9977),
            ("Williamsburg", 40.7081, -73.9571),
        ]
        
        print("🏙️ NYC Property Investment ML - Data Source Diagnostic")
        print("="*80)
        print("This diagnostic will test all data sources and identify issues")
        print("with address matching, coordinate validation, and data quality.")
        print("="*80)
        
        # Test API connectivity first
        api_results = self.test_api_connectivity()
        
        # Test address issues
        address_results = self.diagnose_address_issues(test_addresses)
        
        # Test location data accuracy
        location_results = self.test_location_data_accuracy(test_coordinates)
        
        # Generate comprehensive report
        print("\n" + "="*80)
        print("📋 COMPREHENSIVE DIAGNOSTIC REPORT")
        print("="*80)
        
        total_issues = (len(api_results['issues']) + 
                       len(address_results['issues']) + 
                       len(location_results['issues']))
        
        print(f"🔍 APIs Tested: 4")
        print(f"📍 Addresses Tested: {address_results['addresses_tested']}")
        print(f"🗺️ Coordinates Tested: {location_results['coordinates_tested']}")
        print(f"❌ Total Issues Found: {total_issues}")
        
        # API Status
        print(f"\n🌐 API STATUS:")
        print(f"  NYC Open Data: {'✓' if api_results['nyc_open_data'] else '✗'}")
        print(f"  Google Geocoding: {'✓' if api_results['google_geocoding'] else '⚠' if self.api_key == 'demo-api-key' else '✗'}")
        print(f"  Google Places: {'✓' if api_results['google_places'] else '⚠' if self.api_key == 'demo-api-key' else '✗'}")
        print(f"  MTA Subway Data: {'✓' if api_results['mta_data'] else '✗'}")
        
        # Address Accuracy
        geocoding_rate = (address_results['successful_geocoding'] / address_results['addresses_tested'] * 100) if address_results['addresses_tested'] > 0 else 0
        validation_rate = ((address_results['addresses_tested'] - address_results['validation_failures']) / address_results['addresses_tested'] * 100) if address_results['addresses_tested'] > 0 else 0
        
        print(f"\n📍 ADDRESS ACCURACY:")
        print(f"  Geocoding Success Rate: {geocoding_rate:.1f}%")
        print(f"  Validation Success Rate: {validation_rate:.1f}%")
        print(f"  Property Data Found: {address_results['property_data_found']}/{address_results['addresses_tested']}")
        
        # Location Data Quality
        crime_rate = (location_results['crime_data_success'] / location_results['coordinates_tested'] * 100) if location_results['coordinates_tested'] > 0 else 0
        transit_rate = (location_results['transit_data_success'] / location_results['coordinates_tested'] * 100) if location_results['coordinates_tested'] > 0 else 0
        amenity_rate = (location_results['amenity_data_success'] / location_results['coordinates_tested'] * 100) if location_results['coordinates_tested'] > 0 else 0
        
        print(f"\n🗺️ LOCATION DATA QUALITY:")
        print(f"  Crime Data Success: {crime_rate:.1f}%")
        print(f"  Transit Data Success: {transit_rate:.1f}%")
        print(f"  Amenity Data Success: {amenity_rate:.1f}%")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if not api_results['google_geocoding'] and self.api_key == 'demo-api-key':
            print("  • Add Google Maps API key for improved geocoding accuracy")
        if not api_results['google_places'] and self.api_key == 'demo-api-key':
            print("  • Add Google Maps API key for real amenity data")
        if address_results['validation_failures'] > 0:
            print(f"  • {address_results['validation_failures']} addresses failed coordinate validation")
        if not api_results['mta_data']:
            print("  • MTA subway data unavailable - transit scores will be estimated")
        if total_issues == 0:
            print("  • ✅ All systems operational! No issues detected.")
        
        return {
            'api_results': api_results,
            'address_results': address_results,
            'location_results': location_results,
            'total_issues': total_issues,
            'overall_health': 'EXCELLENT' if total_issues == 0 else 'GOOD' if total_issues < 5 else 'NEEDS_ATTENTION'
        }

def main():
    """Main diagnostic function"""
    print("🏙️ NYC Property Investment ML - Data Diagnostic Tool")
    print("=" * 80)
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv(project_root / '.env')
        print("✅ Environment variables loaded")
    except ImportError:
        print("⚠️ python-dotenv not available, using system environment variables")
    
    # Get API key
    api_key = os.getenv('GOOGLE_MAPS_API_KEY', 'demo-api-key')
    
    # Initialize diagnostic tool
    diagnostic = DataSourceDiagnostic(api_key)
    
    # Get test addresses from command line or use defaults
    if len(sys.argv) > 1:
        test_addresses = sys.argv[1:]
        print(f"Testing {len(test_addresses)} custom addresses")
    else:
        test_addresses = None
        print("Using default test addresses")
    
    try:
        # Run full diagnostic
        results = diagnostic.run_full_diagnostic(test_addresses)
        
        print(f"\n" + "="*80)
        print(f"🎯 DIAGNOSTIC COMPLETE")
        print("="*80)
        print(f"Overall System Health: {results['overall_health']}")
        
        if results['total_issues'] > 0:
            print(f"\n⚠️ Found {results['total_issues']} issues that may affect accuracy.")
            print("Run this diagnostic regularly to monitor data source health.")
        else:
            print("\n🎉 All data sources are working perfectly!")
        
        print("\n💡 To test specific addresses:")
        print("python scripts/diagnose_data_issues.py \"Your Address 1\" \"Your Address 2\"")
        
        return results['overall_health'] in ['EXCELLENT', 'GOOD']
        
    except KeyboardInterrupt:
        print("\n⏹️ Diagnostic interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Diagnostic failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
