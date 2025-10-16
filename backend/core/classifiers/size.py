"""
Company Size Classifier
"""
from typing import Dict


class SizeClassifier:
    """Company Size Classification"""
    
    SIZE_CATEGORIES = {
        'micro': {
            'name': 'متناهية الصغر',
            'name_en': 'Micro',
            'employees': '1-5',
            'revenue_range': '< 3M SAR'
        },
        'small': {
            'name': 'صغيرة',
            'name_en': 'Small',
            'employees': '6-49',
            'revenue_range': '3M-40M SAR'
        },
        'medium': {
            'name': 'متوسطة',
            'name_en': 'Medium',
            'employees': '50-249',
            'revenue_range': '40M-200M SAR'
        },
        'large': {
            'name': 'كبيرة',
            'name_en': 'Large',
            'employees': '250+',
            'revenue_range': '> 200M SAR'
        }
    }
    
    @staticmethod
    def classify_by_data(employees: int = None, revenue: float = None) -> Dict:
        """
        Classify size by employees or revenue
        
        Returns:
            {
                'size': str,
                'size_en': str,
                'category': str,
                'confidence': float
            }
        """
        if employees:
            if employees <= 5:
                return {
                    'size': 'متناهية الصغر',
                    'size_en': 'Micro',
                    'category': 'micro',
                    'confidence': 0.9
                }
            elif employees <= 49:
                return {
                    'size': 'صغيرة',
                    'size_en': 'Small',
                    'category': 'small',
                    'confidence': 0.9
                }
            elif employees <= 249:
                return {
                    'size': 'متوسطة',
                    'size_en': 'Medium',
                    'category': 'medium',
                    'confidence': 0.9
                }
            else:
                return {
                    'size': 'كبيرة',
                    'size_en': 'Large',
                    'category': 'large',
                    'confidence': 0.9
                }
        
        # Default to small if no data
        return {
            'size': 'غير محدد',
            'size_en': 'Unspecified',
            'category': 'unknown',
            'confidence': 0.0
        }

