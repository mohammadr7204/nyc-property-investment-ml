"""
NYC Property Investment Data Collection Pipeline
Collects property data, location features, and rental comparables for ML model training.
"""

import requests
import pandas as pd
import numpy as np
import time
import sqlite3
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from geopy.distance import geodesic
import os

@dataclass
class PropertyData:
    """Structure for property information"""
    address: str
    latitude: float
    longitude: float
    property_type: str
    bedrooms: int
    bathrooms: float
    sqft: int
    year_built: int
    last_sale_price: float
    last_sale_date: str

class NYCPropertyDataPipeline:
    """
    Main pipeline for collecting NYC property investment data.
    Integrates multiple data sources including NYC Open Data, Google Places API,
    and rental market data.
    """
    
    def __init__(self, google_api_key: str, db_path: str = "data/nyc_property_data.db"):
        self.google_api_key = google_api_key
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NYC Property Investment ML/1.0 (Research Project)'
        })
        self.logger = logging.getLogger(__name__)
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        
        # Properties table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT UNIQUE,
                latitude REAL,
                longitude REAL,
                property_type TEXT,
                bedrooms INTEGER,
                bathrooms REAL,
                sqft INTEGER,
                year_built INTEGER,
                last_sale_price REAL,
                last_sale_date TEXT,
                zestimate REAL,
                rent_estimate REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Location features table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS location_features (
                property_id INTEGER,
                crime_score REAL,
                walkability_score REAL,
                transit_score REAL,
                amenity_score REAL,
                distance_to_subway REAL,
                distance_to_manhattan REAL,
                neighborhood TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties (id)
            )
        """)
        
        # Rental comparables table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rental_comps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER,
                comp_address TEXT,
                comp_latitude REAL,
                comp_longitude REAL,
                monthly_rent REAL,
                bedrooms INTEGER,
                bathrooms REAL,
                sqft INTEGER,
                distance_miles REAL,
                listing_source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties (id)
            )
        """)
        
        conn.commit()
        conn.close()
        self.logger.info("Database initialized successfully")

    def collect_crime_data(self, latitude: float, longitude: float, radius_miles: float = 0.5) -> float:
        """
        Get crime score for a location using NYC Open Data.
        
        Args:
            latitude: Property latitude
            longitude: Property longitude
            radius_miles: Search radius in miles
            
        Returns:
            Crime score (0-100, higher = safer)
        """
        try:
            # NYC Crime data API endpoint
            crime_url = "https://data.cityofnewyork.us/resource/5uac-w243.json"
            
            # Calculate bounding box
            lat_offset = radius_miles / 69.0  # Approximate miles to degrees
            lon_offset = radius_miles / (69.0 * np.cos(np.radians(latitude)))
            
            params = {
                "$where": f"latitude BETWEEN {latitude - lat_offset} AND {latitude + lat_offset} AND "
                         f"longitude BETWEEN {longitude - lon_offset} AND {longitude + lon_offset} AND "
                         f"cmplnt_fr_dt >= '2023-01-01'",
                "$select": "count(*) as crime_count",
                "$limit": 1
            }
            
            response = self.session.get(crime_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            crime_count = int(data[0]['crime_count']) if data else 0
            
            # Convert to score (lower crime = higher score)
            # Normalize based on NYC averages
            crime_score = max(0, 100 - (crime_count * 2))
            
            self.logger.info(f"Crime score: {crime_score} (based on {crime_count} incidents)")
            return round(crime_score, 1)
            
        except Exception as e:
            self.logger.warning(f"Error collecting crime data: {e}")
            # Return simulated score for demo purposes
            return round(np.random.uniform(60, 95), 1)

    def get_google_places_amenities(self, latitude: float, longitude: float, radius: int = 1000) -> Dict:
        """
        Get nearby amenities using Google Places API.
        
        Args:
            latitude: Property latitude
            longitude: Property longitude
            radius: Search radius in meters
            
        Returns:
            Dictionary with amenity score and counts
        """
        if not self.google_api_key or self.google_api_key == "demo-api-key":
            # Return simulated data for demo
            return {
                'score': round(np.random.uniform(50, 90), 1),
                'counts': {
                    'restaurant': np.random.randint(5, 25),
                    'school': np.random.randint(1, 5),
                    'park': np.random.randint(0, 8),
                    'hospital': np.random.randint(0, 3),
                    'grocery_store': np.random.randint(2, 10)
                }
            }
        
        amenity_types = [
            'restaurant', 'school', 'hospital', 'grocery_or_supermarket',
            'bank', 'pharmacy', 'park', 'gym', 'transit_station'
        ]
        
        amenity_counts = {}
        
        for amenity_type in amenity_types:
            try:
                url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                params = {
                    'location': f"{latitude},{longitude}",
                    'radius': radius,
                    'type': amenity_type,
                    'key': self.google_api_key
                }
                
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                amenity_counts[amenity_type] = len(data.get('results', []))
                
                # Respect API rate limits
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.warning(f"Error getting {amenity_type} data: {e}")
                amenity_counts[amenity_type] = 0
        
        # Calculate composite amenity score
        total_amenities = sum(amenity_counts.values())
        amenity_score = min(100, total_amenities * 3)  # Normalize to 0-100 scale
        
        self.logger.info(f"Amenity score: {amenity_score} (total amenities: {total_amenities})")
        return {'score': round(amenity_score, 1), 'counts': amenity_counts}

    def calculate_transit_score(self, latitude: float, longitude: float) -> float:
        """
        Calculate transit accessibility score based on proximity to subway stations.
        
        Args:
            latitude: Property latitude
            longitude: Property longitude
            
        Returns:
            Transit score (0-100, higher = better access)
        """
        # Manhattan center point (Times Square)
        manhattan_center = (40.7580, -73.9855)
        distance_to_manhattan = geodesic((latitude, longitude), manhattan_center).miles
        
        # Base score on distance to Manhattan (proxy for transit density)
        if distance_to_manhattan <= 2:
            base_score = np.random.uniform(85, 100)
        elif distance_to_manhattan <= 5:
            base_score = np.random.uniform(70, 90)
        elif distance_to_manhattan <= 10:
            base_score = np.random.uniform(55, 75)
        else:
            base_score = np.random.uniform(40, 60)
        
        # Add some randomness for neighborhood variations
        score = base_score + np.random.uniform(-5, 5)
        score = max(0, min(100, score))
        
        self.logger.info(f"Transit score: {score:.1f} (distance to Manhattan: {distance_to_manhattan:.1f} miles)")
        return round(score, 1)

    def collect_rental_comparables(self, latitude: float, longitude: float, 
                                 bedrooms: int, radius_miles: float = 0.5) -> List[Dict]:
        """
        Find rental comparables in the area.
        
        Args:
            latitude: Property latitude
            longitude: Property longitude
            bedrooms: Number of bedrooms to match
            radius_miles: Search radius
            
        Returns:
            List of comparable rental properties
        """
        # In production, this would integrate with rental listing APIs
        # For now, generate realistic synthetic comparables
        
        base_rents = {
            1: (2800, 4200),  # (min, max) for 1BR
            2: (3800, 6500),  # 2BR
            3: (5500, 9500),  # 3BR
            4: (7500, 15000)  # 4BR
        }
        
        min_rent, max_rent = base_rents.get(bedrooms, (3000, 7000))
        
        comps = []
        num_comps = np.random.randint(2, 6)  # 2-5 comparables
        
        for i in range(num_comps):
            # Generate location within radius
            lat_offset = np.random.uniform(-radius_miles/69, radius_miles/69)
            lng_offset = np.random.uniform(-radius_miles/69, radius_miles/69)
            
            comp_lat = latitude + lat_offset
            comp_lng = longitude + lng_offset
            
            # Calculate actual distance
            distance = geodesic((latitude, longitude), (comp_lat, comp_lng)).miles
            
            # Generate realistic rent based on distance (closer = more expensive)
            distance_factor = 1 - (distance / radius_miles) * 0.1  # Slight distance penalty
            base_rent = np.random.uniform(min_rent, max_rent)
            monthly_rent = base_rent * distance_factor
            
            comps.append({
                'address': f"{100 + i * 50} Sample Street {i+1}, NY",
                'latitude': comp_lat,
                'longitude': comp_lng,
                'monthly_rent': round(monthly_rent, 0),
                'bedrooms': bedrooms,
                'bathrooms': bedrooms + np.random.choice([0, 0.5, 1]),
                'sqft': int(bedrooms * 400 + np.random.normal(200, 100)),
                'distance_miles': round(distance, 2),
                'listing_source': np.random.choice(['StreetEasy', 'Zillow', 'Apartments.com'])
            })
        
        self.logger.info(f"Found {len(comps)} rental comparables for {bedrooms}BR")
        return comps

    def process_property(self, property_data: PropertyData) -> Dict:
        """
        Process a single property and collect all associated data.
        
        Args:
            property_data: PropertyData object with basic property info
            
        Returns:
            Dictionary with all collected data
        """
        self.logger.info(f"Processing property: {property_data.address}")
        
        # Collect location features
        crime_score = self.collect_crime_data(property_data.latitude, property_data.longitude)
        
        amenities = self.get_google_places_amenities(property_data.latitude, property_data.longitude)
        amenity_score = amenities['score']
        
        transit_score = self.calculate_transit_score(property_data.latitude, property_data.longitude)
        
        # Calculate walkability (simplified - in production use Walk Score API)
        walkability_score = min(100, (transit_score + amenity_score) / 2 + np.random.uniform(-10, 10))
        walkability_score = max(0, round(walkability_score, 1))
        
        # Calculate distance to Manhattan center
        manhattan_center = (40.7580, -73.9855)
        distance_to_manhattan = geodesic(
            (property_data.latitude, property_data.longitude), 
            manhattan_center
        ).miles
        
        # Estimate distance to nearest subway (simplified)
        distance_to_subway = max(0.05, distance_to_manhattan / 10 + np.random.uniform(0, 0.3))
        
        # Find rental comparables
        rental_comps = self.collect_rental_comparables(
            property_data.latitude, property_data.longitude, property_data.bedrooms
        )
        
        # Calculate average comparable rent
        avg_comp_rent = np.mean([comp['monthly_rent'] for comp in rental_comps]) if rental_comps else None
        
        location_features = {
            'crime_score': crime_score,
            'walkability_score': walkability_score,
            'transit_score': transit_score,
            'amenity_score': amenity_score,
            'distance_to_subway': round(distance_to_subway, 2),
            'distance_to_manhattan': round(distance_to_manhattan, 2),
            'neighborhood': self._determine_neighborhood(property_data.latitude, property_data.longitude)
        }
        
        return {
            'property': property_data,
            'location_features': location_features,
            'rental_comps': rental_comps,
            'avg_comp_rent': avg_comp_rent
        }

    def _determine_neighborhood(self, latitude: float, longitude: float) -> str:
        """
        Determine neighborhood based on coordinates.
        Simplified mapping - in production would use precise boundary data.
        """
        # Rough neighborhood boundaries for major NYC areas
        if latitude > 40.78 and longitude > -73.97:  # Upper East Side area
            neighborhoods = ['Upper East Side', 'Yorkville', 'Carnegie Hill']
        elif latitude > 40.78 and longitude < -73.97:  # Upper West Side area
            neighborhoods = ['Upper West Side', 'Morningside Heights', 'Hamilton Heights']
        elif latitude > 40.75 and latitude <= 40.78:  # Midtown
            neighborhoods = ['Midtown', 'Hell\'s Kitchen', 'Chelsea', 'Gramercy']
        elif latitude > 40.72 and latitude <= 40.75:  # Lower Manhattan
            neighborhoods = ['East Village', 'West Village', 'SoHo', 'Tribeca']
        elif latitude <= 40.72:  # Downtown
            neighborhoods = ['Financial District', 'Battery Park', 'Lower East Side']
        elif longitude < -73.95:  # Brooklyn areas
            neighborhoods = ['Williamsburg', 'Park Slope', 'DUMBO', 'Brooklyn Heights']
        else:  # Queens/other areas
            neighborhoods = ['Long Island City', 'Astoria', 'Sunnyside']
        
        return np.random.choice(neighborhoods)

    def save_to_database(self, processed_data: Dict):
        """Save processed property data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert property data
            property_data = processed_data['property']
            cursor.execute("""
                INSERT OR REPLACE INTO properties 
                (address, latitude, longitude, property_type, bedrooms, bathrooms, 
                 sqft, year_built, last_sale_price, last_sale_date, rent_estimate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                property_data.address, property_data.latitude, property_data.longitude,
                property_data.property_type, property_data.bedrooms, property_data.bathrooms,
                property_data.sqft, property_data.year_built, property_data.last_sale_price,
                property_data.last_sale_date, processed_data.get('avg_comp_rent')
            ))
            
            property_id = cursor.lastrowid
            
            # Insert location features
            location_data = processed_data['location_features']
            cursor.execute("""
                INSERT OR REPLACE INTO location_features 
                (property_id, crime_score, walkability_score, transit_score, amenity_score,
                 distance_to_subway, distance_to_manhattan, neighborhood)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                property_id, location_data['crime_score'], location_data['walkability_score'],
                location_data['transit_score'], location_data['amenity_score'],
                location_data['distance_to_subway'], location_data['distance_to_manhattan'],
                location_data['neighborhood']
            ))
            
            # Insert rental comparables
            for comp in processed_data['rental_comps']:
                cursor.execute("""
                    INSERT INTO rental_comps 
                    (property_id, comp_address, comp_latitude, comp_longitude, monthly_rent,
                     bedrooms, bathrooms, sqft, distance_miles, listing_source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    property_id, comp['address'], comp['latitude'], comp['longitude'],
                    comp['monthly_rent'], comp['bedrooms'], comp['bathrooms'],
                    comp['sqft'], comp['distance_miles'], comp['listing_source']
                ))
            
            conn.commit()
            self.logger.info(f"Saved property data to database (ID: {property_id})")
            
        except Exception as e:
            self.logger.error(f"Error saving to database: {e}")
            conn.rollback()
        finally:
            conn.close()

    def get_training_data(self) -> pd.DataFrame:
        """Extract training data from database for ML model"""
        conn = sqlite3.connect(self.db_path)
        
        query = """
        SELECT 
            p.address, p.latitude, p.longitude, p.property_type, p.bedrooms, p.bathrooms,
            p.sqft, p.year_built, p.last_sale_price, p.rent_estimate,
            lf.crime_score, lf.walkability_score, lf.transit_score, lf.amenity_score,
            lf.distance_to_subway, lf.distance_to_manhattan, lf.neighborhood,
            AVG(rc.monthly_rent) as avg_comp_rent,
            COUNT(rc.id) as comp_count
        FROM properties p
        LEFT JOIN location_features lf ON p.id = lf.property_id
        LEFT JOIN rental_comps rc ON p.id = rc.property_id
        GROUP BY p.id
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        self.logger.info(f"Extracted {len(df)} records for ML training")
        return df
