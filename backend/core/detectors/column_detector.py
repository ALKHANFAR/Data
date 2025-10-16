"""
Automatic Column Detection
Detects: Phone, Email, Name, Company, City, Region, etc.
"""
import re
from typing import Dict, List, Optional
import pandas as pd


class ColumnDetector:
    """Smart Column Detector"""
    
    # Arabic keywords for detection
    PHONE_KEYWORDS_AR = ['هاتف', 'جوال', 'موبايل', 'رقم', 'تلفون', 'واتس', 'whatsapp']
    EMAIL_KEYWORDS_AR = ['ايميل', 'بريد', 'email', 'mail', 'إيميل']
    NAME_KEYWORDS_AR = ['اسم', 'name', 'الاسم', 'صاحب', 'مالك']
    COMPANY_KEYWORDS_AR = ['شركة', 'مؤسسة', 'مكتب', 'company', 'منشأة', 'الشركة']
    CITY_KEYWORDS_AR = ['مدينة', 'city', 'المدينة', 'بلد']
    REGION_KEYWORDS_AR = ['منطقة', 'region', 'المنطقة', 'محافظة']
    ACTIVITY_KEYWORDS_AR = ['نشاط', 'activity', 'النشاط', 'مجال', 'تخصص']
    ADDRESS_KEYWORDS_AR = ['عنوان', 'address', 'العنوان', 'موقع', 'حي']
    WEBSITE_KEYWORDS_AR = ['موقع', 'website', 'الموقع', 'رابط', 'link']
    
    # English keywords
    PHONE_KEYWORDS_EN = ['phone', 'mobile', 'cell', 'tel', 'telephone', 'number', 'contact']
    EMAIL_KEYWORDS_EN = ['email', 'mail', 'e-mail']
    NAME_KEYWORDS_EN = ['name', 'owner', 'person', 'contact']
    COMPANY_KEYWORDS_EN = ['company', 'business', 'organization', 'firm', 'corp']
    
    @staticmethod
    def normalize_column_name(col: str) -> str:
        """Normalize column name for comparison"""
        if not col:
            return ""
        
        # Convert to lowercase
        col = str(col).lower().strip()
        
        # Remove extra spaces
        col = re.sub(r'\s+', ' ', col)
        
        # Remove special characters
        col = re.sub(r'[^\w\s\u0600-\u06FF]', '', col)
        
        return col
    
    @staticmethod
    def contains_keywords(text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    @staticmethod
    def analyze_sample_data(data: pd.Series, sample_size: int = 100) -> Dict:
        """Analyze sample data to determine column type"""
        # Get non-null sample
        sample = data.dropna().head(sample_size)
        
        if len(sample) == 0:
            return {'type': 'unknown', 'confidence': 0}
        
        # Convert to string
        sample = sample.astype(str)
        
        # Count patterns
        phone_count = 0
        email_count = 0
        url_count = 0
        number_count = 0
        arabic_count = 0
        
        for value in sample:
            # Phone pattern
            if re.search(r'[\d\+\(\)\-\s]{8,}', value):
                digits = re.sub(r'[^\d]', '', value)
                if 8 <= len(digits) <= 15:
                    phone_count += 1
            
            # Email pattern
            if '@' in value and '.' in value:
                if re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
                    email_count += 1
            
            # URL pattern
            if 'http' in value or 'www.' in value or '.com' in value:
                url_count += 1
            
            # Number pattern
            if value.replace('.', '').replace(',', '').isdigit():
                number_count += 1
            
            # Arabic text
            if re.search(r'[\u0600-\u06FF]', value):
                arabic_count += 1
        
        total = len(sample)
        
        # Determine type based on highest percentage
        if phone_count / total > 0.5:
            return {'type': 'phone', 'confidence': phone_count / total}
        elif email_count / total > 0.5:
            return {'type': 'email', 'confidence': email_count / total}
        elif url_count / total > 0.5:
            return {'type': 'website', 'confidence': url_count / total}
        elif arabic_count / total > 0.7:
            return {'type': 'text_arabic', 'confidence': arabic_count / total}
        elif number_count / total > 0.8:
            return {'type': 'number', 'confidence': number_count / total}
        else:
            return {'type': 'text', 'confidence': 0.5}
    
    @staticmethod
    def detect_column_type(col_name: str, data: pd.Series) -> Dict:
        """
        Detect column type from name and data
        
        Returns:
            {
                'original_name': str,
                'detected_type': str,  # phone, email, name, company, city, etc.
                'confidence': float,
                'method': str  # 'name', 'data', 'both'
            }
        """
        normalized = ColumnDetector.normalize_column_name(col_name)
        
        # Try detection by name first
        detected_by_name = None
        confidence_by_name = 0.0
        
        if ColumnDetector.contains_keywords(normalized, 
            ColumnDetector.PHONE_KEYWORDS_AR + ColumnDetector.PHONE_KEYWORDS_EN):
            detected_by_name = 'phone'
            confidence_by_name = 0.9
        
        elif ColumnDetector.contains_keywords(normalized,
            ColumnDetector.EMAIL_KEYWORDS_AR + ColumnDetector.EMAIL_KEYWORDS_EN):
            detected_by_name = 'email'
            confidence_by_name = 0.9
        
        elif ColumnDetector.contains_keywords(normalized,
            ColumnDetector.NAME_KEYWORDS_AR + ColumnDetector.NAME_KEYWORDS_EN):
            detected_by_name = 'name'
            confidence_by_name = 0.8
        
        elif ColumnDetector.contains_keywords(normalized,
            ColumnDetector.COMPANY_KEYWORDS_AR + ColumnDetector.COMPANY_KEYWORDS_EN):
            detected_by_name = 'company'
            confidence_by_name = 0.8
        
        elif ColumnDetector.contains_keywords(normalized, ColumnDetector.CITY_KEYWORDS_AR):
            detected_by_name = 'city'
            confidence_by_name = 0.8
        
        elif ColumnDetector.contains_keywords(normalized, ColumnDetector.REGION_KEYWORDS_AR):
            detected_by_name = 'region'
            confidence_by_name = 0.8
        
        elif ColumnDetector.contains_keywords(normalized, ColumnDetector.ACTIVITY_KEYWORDS_AR):
            detected_by_name = 'activity'
            confidence_by_name = 0.8
        
        elif ColumnDetector.contains_keywords(normalized, ColumnDetector.WEBSITE_KEYWORDS_AR):
            detected_by_name = 'website'
            confidence_by_name = 0.8
        
        # Analyze data
        data_analysis = ColumnDetector.analyze_sample_data(data)
        detected_by_data = data_analysis['type']
        confidence_by_data = data_analysis['confidence']
        
        # Combine results
        if detected_by_name and confidence_by_name >= 0.8:
            # High confidence from name
            return {
                'original_name': col_name,
                'detected_type': detected_by_name,
                'confidence': confidence_by_name,
                'method': 'name'
            }
        
        elif detected_by_data in ['phone', 'email', 'website'] and confidence_by_data >= 0.6:
            # High confidence from data
            return {
                'original_name': col_name,
                'detected_type': detected_by_data,
                'confidence': confidence_by_data,
                'method': 'data'
            }
        
        elif detected_by_name and detected_by_data == detected_by_name:
            # Both agree
            avg_confidence = (confidence_by_name + confidence_by_data) / 2
            return {
                'original_name': col_name,
                'detected_type': detected_by_name,
                'confidence': min(avg_confidence + 0.1, 1.0),
                'method': 'both'
            }
        
        else:
            # Use name-based if available, otherwise data-based
            if detected_by_name:
                return {
                    'original_name': col_name,
                    'detected_type': detected_by_name,
                    'confidence': confidence_by_name,
                    'method': 'name'
                }
            else:
                return {
                    'original_name': col_name,
                    'detected_type': detected_by_data,
                    'confidence': confidence_by_data,
                    'method': 'data'
                }
    
    @staticmethod
    def detect_all_columns(df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Detect all columns in dataframe
        
        Returns:
            {
                'column_name': {
                    'original_name': str,
                    'detected_type': str,
                    'confidence': float,
                    'method': str
                },
                ...
            }
        """
        results = {}
        
        for col in df.columns:
            detection = ColumnDetector.detect_column_type(col, df[col])
            results[col] = detection
        
        return results

