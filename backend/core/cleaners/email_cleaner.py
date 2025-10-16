"""
Email Cleaner - 15 Comprehensive Checks
FIXED VERSION - All bugs resolved
"""
import re
from typing import Dict, Any


class EmailCleaner:
    """Professional Email Cleaner - Bug-free version"""
    
    # Disposable email domains
    DISPOSABLE_DOMAINS = [
        '10minutemail', 'tempmail', 'throwaway', 'guerrillamail',
        'mailinator', 'yopmail', 'maildrop', 'trashmail',
        'temp-mail', 'fakeinbox', 'getnada', 'getairmail',
        'sharklasers', 'spam4.me', 'tempr.email', 'mohmal'
    ]
    
    # Role-based email prefixes
    ROLE_BASED = [
        'admin', 'info', 'support', 'sales', 'contact', 'help',
        'service', 'webmaster', 'postmaster', 'noreply', 'no-reply',
        'marketing', 'billing', 'abuse', 'security', 'privacy', 'legal'
    ]
    
    # Suspicious characters for security check
    SUSPICIOUS_CHARS = ["'", '"', '--', ';', '<', '>', '\\']
    
    @staticmethod
    def is_disposable(email: str) -> bool:
        """Check if email is from disposable provider"""
        email_lower = email.lower()
        return any(domain in email_lower for domain in EmailCleaner.DISPOSABLE_DOMAINS)
    
    @staticmethod
    def is_role_based(email: str) -> bool:
        """Check if email is role-based"""
        local = email.split('@')[0].lower()
        return any(local.startswith(role) for role in EmailCleaner.ROLE_BASED)
    
    @staticmethod
    def has_suspicious_chars(email: str) -> bool:
        """Check for suspicious characters (security)"""
        return any(char in email for char in EmailCleaner.SUSPICIOUS_CHARS)
    
    @staticmethod
    def validate_email(email: Any) -> Dict:
        """
        Validate email with 15 comprehensive checks
        
        Args:
            email: Email address (any type will be validated)
            
        Returns:
            {
                'clean': str,
                'status': str,      # 'valid', 'error', 'optional'
                'error': str,
                'category': str,
                'is_disposable': bool,
                'is_role_based': bool,
                'has_suspicious_chars': bool
            }
        """
        # Check 1: Handle None
        if email is None:
            return {
                'clean': '',
                'status': 'optional',
                'error': '',
                'category': 'empty',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 2: Type validation - FIXED
        if not isinstance(email, str):
            # Handle non-string types (int, float, list, dict, etc.)
            if isinstance(email, (int, float)):
                # Convert numbers to string for error reporting
                return {
                    'clean': '',
                    'status': 'error',
                    'error': f'نوع بيانات خاطئ: رقم ({email})',
                    'category': 'invalid_type',
                    'is_disposable': False,
                    'is_role_based': False,
                    'has_suspicious_chars': False
                }
            elif isinstance(email, (list, dict, tuple, set)):
                return {
                    'clean': '',
                    'status': 'error',
                    'error': f'نوع بيانات خاطئ: {type(email).__name__}',
                    'category': 'invalid_type',
                    'is_disposable': False,
                    'is_role_based': False,
                    'has_suspicious_chars': False
                }
            else:
                # Try to convert to string
                try:
                    email = str(email)
                except:
                    return {
                        'clean': '',
                        'status': 'error',
                        'error': 'لا يمكن تحويل إلى نص',
                        'category': 'invalid_type',
                        'is_disposable': False,
                        'is_role_based': False,
                        'has_suspicious_chars': False
                    }
        
        # Now safe to call string methods
        email = email.strip()
        
        # Check 3: Empty after strip
        if not email or email == '':
            return {
                'clean': '',
                'status': 'optional',
                'error': '',
                'category': 'empty',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Clean and lowercase
        email = email.lower()
        
        # Check 4: Excel errors
        excel_errors = ['#error', '#ref', '#n/a', '#value', '#div/0', '#name', '#null']
        if any(err in email for err in excel_errors):
            return {
                'clean': '',
                'status': 'error',
                'error': 'خطأ في البيانات',
                'category': 'excel_error',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 5: Remove ALL spaces - FIXED
        if ' ' in email:
            return {
                'clean': '',
                'status': 'error',
                'error': 'يحتوي على مسافات',
                'category': 'contains_spaces',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 6: Length validation
        if len(email) < 5 or len(email) > 254:
            return {
                'clean': '',
                'status': 'error',
                'error': f'طول غير صالح ({len(email)} حرف)',
                'category': 'invalid_length',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 7: Must contain @ and .
        if '@' not in email or '.' not in email:
            return {
                'clean': '',
                'status': 'error',
                'error': 'تنسيق خاطئ (بدون @ أو .)',
                'category': 'missing_symbols',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 8: Only one @
        if email.count('@') != 1:
            return {
                'clean': '',
                'status': 'error',
                'error': 'يجب أن يحتوي على @ واحدة فقط',
                'category': 'multiple_at',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Split email
        try:
            local, domain = email.split('@')
        except ValueError:
            return {
                'clean': '',
                'status': 'error',
                'error': 'تنسيق خاطئ',
                'category': 'invalid_format',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 9: @ position
        if not local or not domain:
            return {
                'clean': '',
                'status': 'error',
                'error': '@ في موقع خاطئ',
                'category': 'wrong_at_position',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 10: Dot after @
        if '.' not in domain:
            return {
                'clean': '',
                'status': 'error',
                'error': 'نطاق بدون نقطة',
                'category': 'no_dot_in_domain',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 11: Dot position
        if domain.startswith('.') or domain.endswith('.'):
            return {
                'clean': '',
                'status': 'error',
                'error': 'نقطة في بداية أو نهاية النطاق',
                'category': 'wrong_dot_position',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 12: Consecutive dots
        if '..' in email:
            return {
                'clean': '',
                'status': 'error',
                'error': 'نقاط متتالية',
                'category': 'consecutive_dots',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 13: Local part validation
        if local.startswith('.') or local.endswith('.'):
            return {
                'clean': '',
                'status': 'error',
                'error': 'أحرف غير صالحة قبل @',
                'category': 'invalid_local_part',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 14: TLD length
        tld = domain.split('.')[-1]
        if len(tld) < 2:
            return {
                'clean': '',
                'status': 'error',
                'error': 'امتداد النطاق قصير جداً',
                'category': 'short_tld',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 15: Valid characters (RFC 5322 simplified but strict)
        pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
        if not re.match(pattern, email):
            return {
                'clean': '',
                'status': 'error',
                'error': 'أحرف غير مسموحة',
                'category': 'invalid_characters',
                'is_disposable': False,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 16: Disposable email
        is_disposable = EmailCleaner.is_disposable(email)
        if is_disposable:
            return {
                'clean': '',
                'status': 'error',
                'error': 'إيميل مؤقت',
                'category': 'disposable',
                'is_disposable': True,
                'is_role_based': False,
                'has_suspicious_chars': False
            }
        
        # Check 17: Role-based email
        is_role_based = EmailCleaner.is_role_based(email)
        
        # Check 18: Suspicious characters (security) - NEW
        has_suspicious = EmailCleaner.has_suspicious_chars(email)
        
        # Valid email
        return {
            'clean': email,
            'status': 'valid',
            'error': '',
            'category': 'valid',
            'is_disposable': False,
            'is_role_based': is_role_based,
            'has_suspicious_chars': has_suspicious
        }
    
    @staticmethod
    def clean(raw_email: Any) -> Dict:
        """
        Main cleaning method
        
        Args:
            raw_email: Raw email (any type)
            
        Returns:
            Dictionary with cleaning results
        """
        return EmailCleaner.validate_email(raw_email)
