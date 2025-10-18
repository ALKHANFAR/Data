"""
Name Cleaner
"""
import re
from typing import Dict


class NameCleaner:
    """Professional Name Cleaner - Industrial Grade"""
    
    # Titles to remove
    TITLES = [
        'السيد', 'السيدة', 'الأستاذ', 'الدكتور', 'المهندس',
        'د.', 'م.', 'أ.', 'mr', 'mrs', 'ms', 'dr', 'prof', 'eng',
        'mr.', 'mrs.', 'ms.', 'dr.', 'prof.', 'eng.'
    ]
    
    @staticmethod
    def clean(raw_name: str) -> Dict:
        """
        Clean and validate name with title removal
        
        Returns:
            {
                'clean': str,
                'status': str,
                'error': str,
                'extracted_phone': str or None
            }
        """
        if not raw_name or str(raw_name).strip() == '':
            return {
                'clean': '',
                'status': 'optional',
                'error': '',
                'extracted_phone': None
            }
        
        name = str(raw_name).strip()
        
        # Check for errors
        if '#' in name:
            return {
                'clean': '',
                'status': 'error',
                'error': 'بيانات خاطئة',
                'extracted_phone': None
            }
        
        # Extract phone if mixed (e.g., "أحمد 0501234567")
        phone_pattern = r'(\+?[\d\s\-\(\)]{8,})'
        phone_match = re.search(phone_pattern, name)
        extracted_phone = phone_match.group(1).strip() if phone_match else None
        if phone_match:
            name = re.sub(phone_pattern, '', name).strip()
        
        # Remove titles
        name_lower = name.lower()
        for title in NameCleaner.TITLES:
            if name_lower.startswith(title.lower() + ' '):
                name = name[len(title):].strip()
                name_lower = name.lower()
        
        # Remove numbers
        name = re.sub(r'\d+', '', name)
        
        # Keep only letters and spaces (Arabic + English)
        name = re.sub(r'[^a-zA-Z\u0600-\u06FF\s]', '', name)
        
        # Clean multiple spaces
        name = re.sub(r'\s+', ' ', name).strip()
        
        # Check minimum length
        if len(name) < 2:
            return {
                'clean': '',
                'status': 'error',
                'error': 'اسم قصير جداً',
                'extracted_phone': extracted_phone
            }
        
        # Capitalize properly
        words = name.split()
        capitalized = []
        for word in words:
            if len(word) > 0:
                capitalized.append(word[0].upper() + word[1:].lower())
        
        name = ' '.join(capitalized)
        
        return {
            'clean': name,
            'status': 'valid',
            'error': '',
            'extracted_phone': extracted_phone
        }

