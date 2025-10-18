"""
Phone Number Cleaner - 78 Countries Support
Separates Mobile from Landline
"""
import re
from typing import Dict, Optional
from backend.config.countries import get_country_info


class PhoneCleaner:
    """Professional Phone Number Cleaner - Industrial Grade"""
    
    # Service numbers to exclude
    SERVICE_NUMBERS = ['900', '911', '999', '112', '996', '997', '998']
    
    # Fake marketing numbers (commonly used fake numbers)
    FAKE_NUMBERS = [
        '0555555555', '0500000000', '0511111111', '0522222222', '0533333333',
        '0544444444', '0566666666', '0577777777', '0588888888', '0599999999',
        '966555555555', '966500000000', '966511111111', '966522222222',
        '0000000000', '1111111111', '1234567890', '0123456789',
        '9665555555555', '9665000000000'
    ]
    
    @staticmethod
    def extract_numbers(text: str) -> str:
        """Extract only numbers from text, handling extensions"""
        if not text:
            return ""
        
        # Convert to string
        text = str(text).strip()
        
        # Check for Excel errors
        excel_errors = ['#ERROR', '#REF', '#N/A', '#VALUE', '#DIV/0', '#NAME', '#NULL']
        if any(err in text.upper() for err in excel_errors):
            return ""
        
        # Remove extensions (e.g., "ext. 123", "ext 123", "x123", "extension 123")
        text = re.sub(r'\s*(ext\.?|extension|x)\s*\d+', '', text, flags=re.IGNORECASE)
        
        # Convert Arabic numbers to English
        arabic_nums = '٠١٢٣٤٥٦٧٨٩'
        english_nums = '0123456789'
        trans_table = str.maketrans(arabic_nums, english_nums)
        text = text.translate(trans_table)
        
        # Extract only digits
        numbers = re.sub(r'[^0-9]', '', text)
        
        return numbers
    
    @staticmethod
    def is_fake_number(phone: str) -> bool:
        """Check if it's a fake marketing number"""
        # Check full number
        if phone in PhoneCleaner.FAKE_NUMBERS:
            return True
        
        # Check last 10 digits (local format)
        if len(phone) >= 10:
            local = phone[-10:]
            if local in PhoneCleaner.FAKE_NUMBERS:
                return True
            
            # Check for repeating patterns (all same digit)
            if len(set(local)) == 1:
                return True
            
            # Check for sequential patterns
            if local in ['0123456789', '9876543210', '1234567890']:
                return True
        
        return False
    
    @staticmethod
    def is_service_number(phone: str) -> bool:
        """Check if it's a service/emergency number"""
        for service in PhoneCleaner.SERVICE_NUMBERS:
            if phone.startswith(service):
                return True
        return False
    
    @staticmethod
    def normalize_phone(phone: str) -> str:
        """Normalize phone number"""
        if not phone:
            return ""
        
        # Remove leading 00
        if phone.startswith('00'):
            phone = phone[2:]
        
        # Remove leading +
        if phone.startswith('+'):
            phone = phone[1:]
        
        return phone
    
    @staticmethod
    def detect_country_code(phone: str) -> Optional[str]:
        """Detect country code from phone number"""
        # Try codes from longest to shortest
        codes = sorted(
            ['966', '971', '965', '974', '973', '968', '962', '961', '970', '967', 
             '964', '963', '213', '212', '216', '249', '218', '222', '252', '253',
             '420', '380', '358', '353', '351', '880', '977', '234', '254', '233',
             '256', '255', '251', '225', '221', '44', '49', '39', '34', '31', '32',
             '41', '43', '46', '47', '45', '48', '36', '40', '30', '52', '55', '54',
             '56', '57', '51', '58', '98', '92', '93', '91', '94', '86', '81', '82',
             '65', '60', '62', '63', '66', '84', '61', '64', '90', '33', '20', '27',
             '7', '1'],
            key=len,
            reverse=True
        )
        
        for code in codes:
            if phone.startswith(code):
                return code
        
        return None
    
    @staticmethod
    def is_unified_number(phone: str, country_code: str) -> bool:
        """Check if it's a Saudi unified number (920)"""
        if country_code == '966':
            after_code = phone[len(country_code):]
            return after_code.startswith('920')
        return False
    
    @staticmethod
    def convert_local_to_international(phone: str) -> Optional[str]:
        """Convert local format to international"""
        # Saudi Arabia patterns (mobile + landline + unified)
        if re.match(r'^5\d{8}$', phone):
            return '966' + phone
        if re.match(r'^05\d{8}$', phone):
            return '966' + phone[1:]
        # Saudi unified numbers (920)
        if re.match(r'^920\d{6}$', phone):
            return '966' + phone
        if re.match(r'^0920\d{6}$', phone):
            return '966' + phone[1:]
        # Saudi landlines (01x, 02x, 03x, 04x)
        if re.match(r'^0[1-4]\d{7}$', phone):
            return '966' + phone[1:]
        if re.match(r'^[1-4]\d{7}$', phone):
            return '966' + phone
        
        # UAE patterns (mobile + landline)
        if re.match(r'^5\d{8}$', phone):
            return '971' + phone
        if re.match(r'^05\d{8}$', phone):
            return '971' + phone[1:]
        # UAE landlines (02, 03, 04, etc.)
        if re.match(r'^[234679]\d{7}$', phone):
            return '971' + phone
        if re.match(r'^0[234679]\d{7}$', phone):
            return '971' + phone[1:]
        
        # Kuwait patterns
        if re.match(r'^[569]\d{7}$', phone):
            return '965' + phone
        
        # Qatar patterns
        if re.match(r'^[3567]\d{7}$', phone):
            return '974' + phone
        
        # Bahrain patterns
        if re.match(r'^[36]\d{7}$', phone):
            return '973' + phone
        
        # Oman patterns
        if re.match(r'^9\d{7}$', phone):
            return '968' + phone
        
        # Egypt patterns
        if re.match(r'^1\d{9}$', phone):
            return '20' + phone
        if re.match(r'^01\d{8}$', phone):
            return '20' + phone[1:]
        
        # Jordan patterns
        if re.match(r'^7\d{8}$', phone):
            return '962' + phone
        if re.match(r'^07\d{8}$', phone):
            return '962' + phone[1:]
        
        # Tunisia patterns
        if re.match(r'^[2459]\d{7}$', phone):
            return '216' + phone
        
        # Turkey patterns
        if re.match(r'^5\d{9}$', phone):
            return '90' + phone
        if re.match(r'^05\d{9}$', phone):
            return '90' + phone[1:]
        
        return None
    
    @staticmethod
    def validate_phone(phone: str) -> Dict:
        """
        Validate and clean phone number
        
        Returns:
            {
                'clean': str,           # Clean international format
                'country': str,         # Country name
                'country_code': str,    # Country code
                'status': str,          # 'valid', 'error'
                'type': str,            # 'mobile', 'landline', 'unknown'
                'error': str,           # Error message if any
                'category': str         # Error category
            }
        """
        # Extract numbers only
        phone = PhoneCleaner.extract_numbers(phone)
        
        # Check if empty
        if not phone:
            return {
                'clean': '',
                'country': '',
                'country_code': '',
                'status': 'error',
                'type': 'unknown',
                'error': 'رقم فارغ',
                'category': 'empty'
            }
        
        # Check minimum length
        if len(phone) < 8:
            return {
                'clean': '',
                'country': '',
                'country_code': '',
                'status': 'error',
                'type': 'unknown',
                'error': f'قصير جداً ({len(phone)} أرقام)',
                'category': 'too_short'
            }
        
        # Normalize
        phone = PhoneCleaner.normalize_phone(phone)
        
        # Check fake numbers (BEFORE service numbers for efficiency)
        if PhoneCleaner.is_fake_number(phone):
            return {
                'clean': '',
                'country': '',
                'country_code': '',
                'status': 'error',
                'type': 'fake',
                'error': 'رقم مزيف/تسويقي',
                'category': 'fake_number'
            }
        
        # Check service numbers
        if PhoneCleaner.is_service_number(phone):
            return {
                'clean': '',
                'country': '',
                'country_code': '',
                'status': 'error',
                'type': 'service',
                'error': 'رقم خدمة/طوارئ',
                'category': 'service_number'
            }
        
        # Detect country code
        country_code = PhoneCleaner.detect_country_code(phone)
        
        # If no country code, try local conversion
        if not country_code:
            converted = PhoneCleaner.convert_local_to_international(phone)
            if converted:
                phone = converted
                country_code = PhoneCleaner.detect_country_code(phone)
        
        # If still no country code
        if not country_code:
            return {
                'clean': '',
                'country': 'غير معروف',
                'country_code': '',
                'status': 'error',
                'type': 'unknown',
                'error': 'كود دولة غير معروف',
                'category': 'unknown_country'
            }
        
        # Get country info
        country_info = get_country_info(country_code)
        
        if not country_info:
            return {
                'clean': '',
                'country': 'غير معروف',
                'country_code': country_code,
                'status': 'error',
                'type': 'unknown',
                'error': 'دولة غير مدعومة',
                'category': 'unsupported_country'
            }
        
        # Check length
        if len(phone) != country_info['length']:
            return {
                'clean': '',
                'country': country_info['name'],
                'country_code': country_code,
                'status': 'error',
                'type': 'unknown',
                'error': f"طول خاطئ: {len(phone)} بدلاً من {country_info['length']}",
                'category': 'wrong_length'
            }
        
        # Get digits after country code
        after_code = phone[len(country_code):]
        
        # Check if unified system (USA/Canada)
        if country_info.get('unified'):
            return {
                'clean': phone,
                'country': country_info['name'],
                'country_code': country_code,
                'status': 'valid',
                'type': 'mobile',
                'error': '',
                'category': 'mobile',
                'note': 'نظام موحد'
            }
        
        # Check for Saudi unified numbers (920) - INDUSTRIAL GRADE
        if PhoneCleaner.is_unified_number(phone, country_code):
            return {
                'clean': phone,
                'country': country_info['name'],
                'country_code': country_code,
                'status': 'valid',
                'type': 'unified_number',
                'error': '',
                'category': 'unified_number',
                'note': 'رقم موحد'
            }
        
        # Check mobile prefixes
        is_mobile = False
        if country_info.get('mobile'):
            for prefix in country_info['mobile']:
                if after_code.startswith(prefix):
                    is_mobile = True
                    break
        
        if is_mobile:
            return {
                'clean': phone,
                'country': country_info['name'],
                'country_code': country_code,
                'status': 'valid',
                'type': 'mobile',
                'error': '',
                'category': 'mobile'
            }
        
        # Check landline prefixes - NOW ACCEPTED AS VALID (INDUSTRIAL GRADE)
        is_landline = False
        if country_info.get('landline'):
            for prefix in country_info['landline']:
                if after_code.startswith(prefix):
                    is_landline = True
                    break
        
        if is_landline:
            return {
                'clean': phone,
                'country': country_info['name'],
                'country_code': country_code,
                'status': 'valid',  # Changed from 'error' to 'valid'
                'type': 'landline',
                'error': '',
                'category': 'landline',
                'note': f'رقم أرضي (يبدأ بـ {after_code[:2]})'
            }
        
        # Unknown prefix
        return {
            'clean': '',
            'country': country_info['name'],
            'country_code': country_code,
            'status': 'error',
            'type': 'unknown',
            'error': f"بادئة غير معروفة: {after_code[:2]}",
            'category': 'unknown_prefix'
        }
    
    @staticmethod
    def clean(raw_phone: str) -> Dict:
        """
        Main cleaning method
        
        Args:
            raw_phone: Raw phone number string
            
        Returns:
            Dictionary with cleaning results
        """
        return PhoneCleaner.validate_phone(raw_phone)

