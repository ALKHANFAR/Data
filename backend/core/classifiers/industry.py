"""
Industry Classifier
Classifies companies by industry/activity
"""
from typing import Dict, List
import re


class IndustryClassifier:
    """Industry Classification System"""
    
    # Industry keywords (Arabic)
    INDUSTRIES = {
        'مقاولات': {
            'keywords': ['مقاولات', 'بناء', 'تشييد', 'إنشاءات', 'معمار', 'هدم', 'ترميم'],
            'name_en': 'Construction',
            'category': 'construction'
        },
        'مصانع': {
            'keywords': ['مصنع', 'صناعة', 'إنتاج', 'تصنيع', 'معمل'],
            'name_en': 'Manufacturing',
            'category': 'manufacturing'
        },
        'تجارة': {
            'keywords': ['تجارة', 'استيراد', 'تصدير', 'توريد', 'بيع', 'شراء', 'تسويق'],
            'name_en': 'Trading',
            'category': 'trading'
        },
        'خدمات': {
            'keywords': ['خدمات', 'صيانة', 'تنظيف', 'نقل', 'شحن', 'توصيل'],
            'name_en': 'Services',
            'category': 'services'
        },
        'مطاعم': {
            'keywords': ['مطعم', 'كافيه', 'مقهى', 'بوفيه', 'مأكولات'],
            'name_en': 'Restaurant',
            'category': 'food'
        },
        'عقارات': {
            'keywords': ['عقارات', 'عقار', 'استثمار عقاري', 'تطوير عقاري'],
            'name_en': 'Real Estate',
            'category': 'real_estate'
        },
        'تقنية': {
            'keywords': ['تقنية', 'برمجة', 'برمجيات', 'تطبيقات', 'أنظمة', 'IT'],
            'name_en': 'Technology',
            'category': 'technology'
        },
        'استشارات': {
            'keywords': ['استشارات', 'استشاري', 'دراسات', 'إدارة'],
            'name_en': 'Consulting',
            'category': 'consulting'
        },
        'صحة': {
            'keywords': ['طبية', 'صحية', 'عيادة', 'مستشفى', 'صيدلية'],
            'name_en': 'Healthcare',
            'category': 'healthcare'
        },
        'تعليم': {
            'keywords': ['تعليم', 'تدريب', 'مدرسة', 'معهد', 'أكاديمية'],
            'name_en': 'Education',
            'category': 'education'
        }
    }
    
    @staticmethod
    def classify_by_name(company_name: str, activity: str = None) -> Dict:
        """
        Classify industry by company name and activity
        
        Returns:
            {
                'industry': str,
                'industry_en': str,
                'category': str,
                'confidence': float,
                'matched_keywords': List[str]
            }
        """
        if not company_name:
            return {
                'industry': 'غير محدد',
                'industry_en': 'Unspecified',
                'category': 'unknown',
                'confidence': 0.0,
                'matched_keywords': []
            }
        
        # Combine name and activity
        text = (company_name + ' ' + (activity or '')).lower()
        
        # Find matches
        matches = {}
        for industry, info in IndustryClassifier.INDUSTRIES.items():
            matched_keywords = []
            for keyword in info['keywords']:
                if keyword in text:
                    matched_keywords.append(keyword)
            
            if matched_keywords:
                matches[industry] = {
                    'info': info,
                    'score': len(matched_keywords),
                    'keywords': matched_keywords
                }
        
        # No matches
        if not matches:
            return {
                'industry': 'غير محدد',
                'industry_en': 'Unspecified',
                'category': 'unknown',
                'confidence': 0.0,
                'matched_keywords': []
            }
        
        # Get best match
        best = max(matches.items(), key=lambda x: x[1]['score'])
        industry_name = best[0]
        match_info = best[1]
        
        # Calculate confidence
        confidence = min(match_info['score'] * 0.3, 1.0)
        
        return {
            'industry': industry_name,
            'industry_en': match_info['info']['name_en'],
            'category': match_info['info']['category'],
            'confidence': confidence,
            'matched_keywords': match_info['keywords']
        }

