"""
Company Name Cleaner
"""
import re
from typing import Dict


class CompanyCleaner:
    """Professional Company Name Cleaner"""
    
    # Company types in Arabic
    COMPANY_TYPES = [
        'شركة', 'مؤسسة', 'مكتب', 'مصنع', 'متجر',
        'شركه', 'مؤسسه', 'للمقاولات', 'للتجارة',
        'ذ.م.م', 'ذ م م', 'المحدودة'
    ]
    
    @staticmethod
    def clean(raw_company: str) -> Dict:
        """
        Clean company name
        
        Returns:
            {
                'clean': str,
                'status': str,
                'error': str,
                'type': str  # شركة، مؤسسة، مكتب، etc
            }
        """
        if not raw_company or str(raw_company).strip() == '':
            return {
                'clean': '',
                'status': 'optional',
                'error': '',
                'type': ''
            }
        
        company = str(raw_company).strip()
        
        # Check for errors
        if '#' in company:
            return {
                'clean': '',
                'status': 'error',
                'error': 'بيانات خاطئة',
                'type': ''
            }
        
        # Clean multiple spaces
        company = re.sub(r'\s+', ' ', company)
        
        # Detect company type
        company_type = ''
        for ctype in CompanyCleaner.COMPANY_TYPES:
            if ctype in company:
                company_type = ctype
                break
        
        # Remove extra dots and dashes
        company = re.sub(r'\.{2,}', '.', company)
        company = re.sub(r'-{2,}', '-', company)
        
        return {
            'clean': company.strip(),
            'status': 'valid',
            'error': '',
            'type': company_type
        }

