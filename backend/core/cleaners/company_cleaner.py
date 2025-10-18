"""
Company Name Cleaner
"""
import re
from typing import Dict


class CompanyCleaner:
    """Professional Company Name Cleaner - Industrial Grade"""
    
    # Company types in Arabic
    COMPANY_TYPES = [
        'شركة', 'مؤسسة', 'مكتب', 'مصنع', 'متجر',
        'شركه', 'مؤسسه', 'للمقاولات', 'للتجارة',
        'ذ.م.م', 'ذ م م', 'المحدودة'
    ]
    
    # Legal suffixes to remove
    LEGAL_SUFFIXES = [
        'ذات مسؤولية محدودة', 'ذ.م.م', 'ذ م م',
        'مساهمة مقفلة', 'مساهمة مفتوحة',
        'المحدودة', 'المحدوده',
        'llc', 'l.l.c', 'ltd', 'ltd.', 'limited',
        'inc', 'inc.', 'incorporated',
        'corp', 'corp.', 'corporation',
        'co', 'co.', 'company'
    ]
    
    @staticmethod
    def clean(raw_company: str) -> Dict:
        """
        Clean company name with legal suffix removal
        
        Returns:
            {
                'clean': str,
                'status': str,
                'error': str,
                'type': str,
                'clean_name_only': str  # Without legal suffixes
            }
        """
        if not raw_company or str(raw_company).strip() == '':
            return {
                'clean': '',
                'status': 'optional',
                'error': '',
                'type': '',
                'clean_name_only': ''
            }
        
        company = str(raw_company).strip()
        
        # Check for errors
        if '#' in company:
            return {
                'clean': '',
                'status': 'error',
                'error': 'بيانات خاطئة',
                'type': '',
                'clean_name_only': ''
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
        
        # Create clean version without legal suffixes
        clean_name_only = company
        company_lower = company.lower()
        for suffix in CompanyCleaner.LEGAL_SUFFIXES:
            suffix_lower = suffix.lower()
            if company_lower.endswith(' ' + suffix_lower):
                clean_name_only = company[:-(len(suffix)+1)].strip()
                break
            elif company_lower.endswith(suffix_lower):
                clean_name_only = company[:-len(suffix)].strip()
                break
        
        return {
            'clean': company.strip(),
            'status': 'valid',
            'error': '',
            'type': company_type,
            'clean_name_only': clean_name_only
        }

