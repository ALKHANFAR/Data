"""
Geographic Classifier
Classifies by Country, Region, City
"""
from typing import Dict, Optional
from backend.config.countries import COUNTRIES


class GeographicClassifier:
    """Geographic Classification System"""
    
    @staticmethod
    def classify_by_phone(country_code: str) -> Dict:
        """Classify geography by phone country code"""
        country_info = COUNTRIES.get(country_code)
        
        if not country_info:
            return {
                'country': 'غير معروف',
                'country_en': 'Unknown',
                'country_code': country_code,
                'region': '',
                'cities': []
            }
        
        return {
            'country': country_info['name'],
            'country_en': country_info.get('name_en', country_info['name']),
            'country_code': country_code,
            'region': '',
            'cities': country_info.get('cities', [])
        }
    
    @staticmethod
    def find_saudi_region(city: str) -> Optional[str]:
        """Find Saudi region from city name"""
        if not city:
            return None
        
        saudi_info = COUNTRIES.get('966')
        if not saudi_info or 'regions' not in saudi_info:
            return None
        
        city_lower = city.lower().strip()
        
        for region, cities in saudi_info['regions'].items():
            for region_city in cities:
                if city_lower in region_city.lower() or region_city.lower() in city_lower:
                    return region
        
        return None
    
    @staticmethod
    def classify_location(city: str = None, region: str = None, country_code: str = None) -> Dict:
        """
        Classify complete location
        
        Returns:
            {
                'country': str,
                'country_en': str,
                'country_code': str,
                'region': str,
                'city': str,
                'confidence': float
            }
        """
        result = {
            'country': '',
            'country_en': '',
            'country_code': country_code or '',
            'region': region or '',
            'city': city or '',
            'confidence': 0.0
        }
        
        # If we have country code
        if country_code:
            country_info = COUNTRIES.get(country_code)
            if country_info:
                result['country'] = country_info['name']
                result['country_en'] = country_info.get('name_en', country_info['name'])
                result['confidence'] = 0.9
                
                # If Saudi, try to find region from city
                if country_code == '966' and city and not region:
                    found_region = GeographicClassifier.find_saudi_region(city)
                    if found_region:
                        result['region'] = found_region
                        result['confidence'] = 1.0
        
        return result

