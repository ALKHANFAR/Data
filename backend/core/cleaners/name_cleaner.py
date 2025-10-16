"""
Name Cleaner
"""
import re
from typing import Dict


class NameCleaner:
    """Professional Name Cleaner"""
    
    @staticmethod
    def clean(raw_name: str) -> Dict:
        """
        Clean and validate name
        
        Returns:
            {
                'clean': str,
                'status': str,
                'error': str
            }
        """
        if not raw_name or str(raw_name).strip() == '':
            return {
                'clean': '',
                'status': 'optional',
                'error': ''
            }
        
        name = str(raw_name).strip()
        
        # Check for errors
        if '#' in name:
            return {
                'clean': '',
                'status': 'error',
                'error': 'بيانات خاطئة'
            }
        
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
                'error': 'اسم قصير جداً'
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
            'error': ''
        }

