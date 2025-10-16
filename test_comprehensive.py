"""
Comprehensive Testing Suite - Full System Audit
Tests every component with edge cases, security checks, and stress tests
"""
import sys
import time
import traceback
from typing import Dict, List
import pandas as pd

# Import all components
from backend.core.cleaners import PhoneCleaner, EmailCleaner, NameCleaner, CompanyCleaner
from backend.core.detectors import ColumnDetector, DuplicateFinder
from backend.core.classifiers import GeographicClassifier, IndustryClassifier, SizeClassifier


class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.warnings = []
    
    def add_pass(self):
        self.passed += 1
    
    def add_fail(self, test_name: str, expected, actual, details=""):
        self.failed += 1
        self.errors.append({
            'test': test_name,
            'expected': expected,
            'actual': actual,
            'details': details
        })
    
    def add_warning(self, message: str):
        self.warnings.append(message)
    
    def summary(self):
        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0
        return f"✅ {self.passed}/{total} tests passed ({rate:.1f}%)"


results = TestResults()


def test_assert(condition: bool, test_name: str, expected, actual, details=""):
    """Custom assert with result tracking"""
    if condition:
        results.add_pass()
        print(f"  ✓ {test_name}")
    else:
        results.add_fail(test_name, expected, actual, details)
        print(f"  ✗ {test_name} - Expected: {expected}, Got: {actual}")


def print_section(title):
    """Print section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: PHONE CLEANER COMPREHENSIVE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_phone_cleaner_comprehensive():
    """Comprehensive PhoneCleaner tests"""
    print_section("TEST 1: PhoneCleaner - Comprehensive Test Suite")
    
    test_cases = [
        # Valid Saudi phones
        ("966501234567", "valid", "mobile", "السعودية"),
        ("00966501234567", "valid", "mobile", "السعودية"),
        ("+966501234567", "valid", "mobile", "السعودية"),
        ("0501234567", "valid", "mobile", "السعودية"),
        ("501234567", "valid", "mobile", "السعودية"),
        
        # Saudi landlines (should be rejected)
        ("966112345678", "error", "landline", "السعودية"),
        ("966212345678", "error", "landline", "السعودية"),
        
        # Other GCC countries
        ("971501234567", "valid", "mobile", "الإمارات"),
        ("96550123456", "valid", "mobile", "الكويت"),
        ("97433123456", "valid", "mobile", "قطر"),
        ("97336123456", "valid", "mobile", "البحرين"),
        ("96891234567", "valid", "mobile", "عمان"),
        
        # Egypt
        ("201012345678", "valid", "mobile", "مصر"),
        ("201112345678", "valid", "mobile", "مصر"),
        
        # USA/Canada (unified system)
        ("12025551234", "valid", "mobile", "الولايات المتحدة/كندا"),
        
        # UK
        ("447700900123", "valid", "mobile", "بريطانيا"),
        
        # Invalid cases
        ("", "error", "unknown", ""),
        ("123", "error", "unknown", ""),
        ("abcdefgh", "error", "unknown", ""),
        
        # Service numbers
        ("911", "error", "unknown", ""),
        ("999", "error", "unknown", ""),
        
        # Excel errors
        ("#ERROR", "error", "unknown", ""),
        ("#REF", "error", "unknown", ""),
        ("#N/A", "error", "unknown", ""),
        
        # Arabic numbers
        ("٩٦٦٥٠١٢٣٤٥٦٧", "valid", "mobile", "السعودية"),
        
        # With formatting
        ("966-50-123-4567", "valid", "mobile", "السعودية"),
        ("(966) 501234567", "valid", "mobile", "السعودية"),
        ("+966 50 123 4567", "valid", "mobile", "السعودية"),
        
        # Security - SQL Injection attempts
        ("'; DROP TABLE users; --", "error", "unknown", ""),
        ("1' OR '1'='1", "error", "unknown", ""),
        
        # Security - XSS attempts
        ("<script>alert('xss')</script>", "error", "unknown", ""),
        ("javascript:alert(1)", "error", "unknown", ""),
        
        # Edge cases
        (None, "error", "unknown", ""),
        (12345, "error", "unknown", ""),  # Number instead of string
        ([], "error", "unknown", ""),  # List
        ({}, "error", "unknown", ""),  # Dict
    ]
    
    print(f"\n📊 Running {len(test_cases)} test cases...")
    
    for i, (phone, expected_status, expected_type, expected_country) in enumerate(test_cases, 1):
        try:
            result = PhoneCleaner.clean(phone)
            
            # Test status
            test_assert(
                result['status'] == expected_status,
                f"Case {i}: Status for '{phone}'",
                expected_status,
                result['status'],
                f"Phone: {phone}"
            )
            
            # Test type
            test_assert(
                result['type'] == expected_type,
                f"Case {i}: Type for '{phone}'",
                expected_type,
                result['type']
            )
            
            # Test country (only for valid phones)
            if expected_status == 'valid' and expected_country:
                test_assert(
                    result['country'] == expected_country,
                    f"Case {i}: Country for '{phone}'",
                    expected_country,
                    result['country']
                )
        
        except Exception as e:
            results.add_fail(
                f"Case {i}: Exception for '{phone}'",
                "No exception",
                str(e),
                traceback.format_exc()
            )
            print(f"  ✗ Case {i}: Exception - {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: EMAIL CLEANER COMPREHENSIVE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_email_cleaner_comprehensive():
    """Comprehensive EmailCleaner tests"""
    print_section("TEST 2: EmailCleaner - 15 Checks Validation")
    
    test_cases = [
        # Valid emails
        ("test@example.com", "valid", False, False),
        ("user.name@company.co.uk", "valid", False, False),
        ("user+tag@example.com", "valid", False, False),
        ("TEST@EXAMPLE.COM", "valid", False, False),  # Should be lowercased
        
        # Empty (optional)
        ("", "optional", False, False),
        ("   ", "optional", False, False),
        
        # Missing @ or .
        ("notanemail", "error", False, False),
        ("missing@dot", "error", False, False),
        ("missing.at.com", "error", False, False),
        
        # Wrong @ position
        ("@example.com", "error", False, False),
        ("test@", "error", False, False),
        
        # Multiple @
        ("test@@example.com", "error", False, False),
        ("test@test@example.com", "error", False, False),
        
        # Dot issues
        ("test@.example.com", "error", False, False),
        ("test@example.com.", "error", False, False),
        (".test@example.com", "error", False, False),
        ("test.@example.com", "error", False, False),
        ("test..name@example.com", "error", False, False),
        
        # Short TLD
        ("test@example.c", "error", False, False),
        
        # Disposable emails
        ("temp@10minutemail.com", "error", True, False),
        ("fake@tempmail.com", "error", True, False),
        ("test@guerrillamail.com", "error", True, False),
        
        # Role-based emails
        ("admin@company.com", "valid", False, True),
        ("info@company.com", "valid", False, True),
        ("support@company.com", "valid", False, True),
        
        # Excel errors
        ("#ERROR", "error", False, False),
        ("#REF", "error", False, False),
        
        # With spaces (should be cleaned)
        ("test @ example.com", "error", False, False),
        ("test @example.com", "error", False, False),
        
        # Security - SQL Injection
        ("test'; DROP TABLE--@example.com", "error", False, False),
        ("admin'--@example.com", "error", False, False),
        
        # Security - XSS
        ("<script>@example.com", "error", False, False),
        ("test@<script>.com", "error", False, False),
        
        # Edge cases
        (None, "optional", False, False),
        (12345, "error", False, False),
        ([], "error", False, False),
    ]
    
    print(f"\n📊 Running {len(test_cases)} test cases...")
    
    for i, (email, expected_status, expected_disposable, expected_role) in enumerate(test_cases, 1):
        try:
            result = EmailCleaner.clean(email)
            
            test_assert(
                result['status'] == expected_status,
                f"Case {i}: Status for '{email}'",
                expected_status,
                result['status']
            )
            
            if expected_status == 'valid':
                # Check if lowercase
                if isinstance(email, str) and email:
                    test_assert(
                        result['clean'] == result['clean'].lower(),
                        f"Case {i}: Lowercase for '{email}'",
                        "lowercase",
                        result['clean']
                    )
            
            # Check flags
            test_assert(
                result['is_disposable'] == expected_disposable,
                f"Case {i}: Disposable flag for '{email}'",
                expected_disposable,
                result['is_disposable']
            )
            
            test_assert(
                result['is_role_based'] == expected_role,
                f"Case {i}: Role-based flag for '{email}'",
                expected_role,
                result['is_role_based']
            )
        
        except Exception as e:
            results.add_fail(
                f"Case {i}: Exception for '{email}'",
                "No exception",
                str(e),
                traceback.format_exc()
            )
            print(f"  ✗ Case {i}: Exception - {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3: COLUMN DETECTOR TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_column_detector():
    """Test ColumnDetector accuracy"""
    print_section("TEST 3: ColumnDetector - Automatic Detection")
    
    # Test DataFrame with Arabic columns
    test_data_ar = {
        'هاتف الشركة': ['966501234567', '966501234568', '966501234569'],
        'البريد الإلكتروني': ['test1@example.com', 'test2@example.com', 'test3@example.com'],
        'اسم الشركة': ['شركة الأولى', 'مؤسسة الثانية', 'مكتب الثالث'],
        'المدينة': ['الرياض', 'جدة', 'الدمام'],
        'النشاط': ['مقاولات', 'تجارة', 'خدمات'],
    }
    
    df_ar = pd.DataFrame(test_data_ar)
    detections_ar = ColumnDetector.detect_all_columns(df_ar)
    
    print("\n📊 Testing Arabic column detection...")
    
    test_assert(
        detections_ar['هاتف الشركة']['detected_type'] == 'phone',
        "Arabic phone column",
        'phone',
        detections_ar['هاتف الشركة']['detected_type']
    )
    
    test_assert(
        detections_ar['البريد الإلكتروني']['detected_type'] == 'email',
        "Arabic email column",
        'email',
        detections_ar['البريد الإلكتروني']['detected_type']
    )
    
    test_assert(
        detections_ar['اسم الشركة']['detected_type'] in ['company', 'name'],
        "Arabic company column",
        'company or name',
        detections_ar['اسم الشركة']['detected_type']
    )
    
    # Test DataFrame with English columns
    test_data_en = {
        'phone': ['966501234570', '966501234571', '966501234572'],
        'email': ['test4@example.com', 'test5@example.com', 'test6@example.com'],
        'company_name': ['Company A', 'Company B', 'Company C'],
        'city': ['Riyadh', 'Jeddah', 'Dammam'],
    }
    
    df_en = pd.DataFrame(test_data_en)
    detections_en = ColumnDetector.detect_all_columns(df_en)
    
    print("\n📊 Testing English column detection...")
    
    test_assert(
        detections_en['phone']['detected_type'] == 'phone',
        "English phone column",
        'phone',
        detections_en['phone']['detected_type']
    )
    
    test_assert(
        detections_en['email']['detected_type'] == 'email',
        "English email column",
        'email',
        detections_en['email']['detected_type']
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4: STRESS TEST - PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════════

def test_performance():
    """Test performance with different data sizes"""
    print_section("TEST 4: Performance & Stress Testing")
    
    test_sizes = [100, 1000, 10000]
    
    for size in test_sizes:
        print(f"\n📊 Testing with {size:,} rows...")
        
        # Generate test data
        test_phones = ['966501234567'] * size
        test_emails = ['test@example.com'] * size
        
        # Test phone cleaning speed
        start_time = time.time()
        for phone in test_phones:
            PhoneCleaner.clean(phone)
        phone_time = time.time() - start_time
        phone_speed = size / phone_time if phone_time > 0 else 0
        
        print(f"  📱 Phone: {phone_time:.2f}s ({phone_speed:.0f} rows/sec)")
        
        # Test email cleaning speed
        start_time = time.time()
        for email in test_emails:
            EmailCleaner.clean(email)
        email_time = time.time() - start_time
        email_speed = size / email_time if email_time > 0 else 0
        
        print(f"  📧 Email: {email_time:.2f}s ({email_speed:.0f} rows/sec)")
        
        # Performance assertions
        if size == 10000:
            test_assert(
                phone_speed > 500,
                f"Phone cleaning speed >= 500 rows/sec",
                ">= 500",
                f"{phone_speed:.0f}"
            )
            
            test_assert(
                email_speed > 500,
                f"Email cleaning speed >= 500 rows/sec",
                ">= 500",
                f"{email_speed:.0f}"
            )


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 5: GEOGRAPHIC CLASSIFIER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_geographic_classifier():
    """Test GeographicClassifier"""
    print_section("TEST 5: GeographicClassifier")
    
    print("\n📊 Testing country classification by phone code...")
    
    test_cases = [
        ('966', 'السعودية', 'Saudi Arabia'),
        ('971', 'الإمارات', 'UAE'),
        ('965', 'الكويت', 'Kuwait'),
        ('20', 'مصر', 'مصر'),
        ('1', 'الولايات المتحدة/كندا', 'الولايات المتحدة/كندا'),
    ]
    
    for code, expected_ar, expected_en in test_cases:
        result = GeographicClassifier.classify_by_phone(code)
        
        test_assert(
            result['country'] == expected_ar,
            f"Country name for code {code}",
            expected_ar,
            result['country']
        )
    
    print("\n📊 Testing Saudi region detection...")
    
    saudi_cities = [
        ('الرياض', 'الرياض'),
        ('جدة', 'مكة المكرمة'),
        ('الدمام', 'الشرقية'),
        ('أبها', 'عسير'),
    ]
    
    for city, expected_region in saudi_cities:
        region = GeographicClassifier.find_saudi_region(city)
        
        test_assert(
            region == expected_region,
            f"Region for {city}",
            expected_region,
            region
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 6: INDUSTRY CLASSIFIER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_industry_classifier():
    """Test IndustryClassifier"""
    print_section("TEST 6: IndustryClassifier")
    
    test_cases = [
        ('شركة المقاولات العامة', 'مقاولات', 'مقاولات', 'Construction'),
        ('مؤسسة التجارة والتسويق', 'تجارة', 'تجارة', 'Trading'),
        ('مصنع الأسمنت', '', 'مصانع', 'Manufacturing'),
        ('مطعم البيك', '', 'مطاعم', 'Restaurant'),
    ]
    
    for company, activity, expected_ar, expected_en in test_cases:
        result = IndustryClassifier.classify_by_name(company, activity)
        
        test_assert(
            result['industry'] == expected_ar,
            f"Industry for '{company}'",
            expected_ar,
            result['industry']
        )
        
        test_assert(
            result['industry_en'] == expected_en,
            f"Industry EN for '{company}'",
            expected_en,
            result['industry_en']
        )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN TEST RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Run all tests"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║                  🔬 COMPREHENSIVE SYSTEM AUDIT & TESTING                 ║")
    print("║                                                                          ║")
    print("║  Testing every component with edge cases, security checks, and stress   ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝")
    
    start_time = time.time()
    
    try:
        test_phone_cleaner_comprehensive()
        test_email_cleaner_comprehensive()
        test_column_detector()
        test_geographic_classifier()
        test_industry_classifier()
        test_performance()
    
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        print(traceback.format_exc())
    
    end_time = time.time()
    
    # Print results
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║                           📊 TEST RESULTS                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝")
    
    print(f"\n{results.summary()}")
    print(f"⏱️  Total time: {end_time - start_time:.2f} seconds")
    
    if results.failed > 0:
        print(f"\n❌ FAILED TESTS ({results.failed}):")
        for error in results.errors[:10]:  # Show first 10
            print(f"\n  Test: {error['test']}")
            print(f"  Expected: {error['expected']}")
            print(f"  Got: {error['actual']}")
            if error['details']:
                print(f"  Details: {error['details'][:200]}")
    
    if results.warnings:
        print(f"\n⚠️  WARNINGS ({len(results.warnings)}):")
        for warning in results.warnings[:10]:
            print(f"  - {warning}")
    
    print("\n")
    
    # Exit code
    sys.exit(0 if results.failed == 0 else 1)


if __name__ == "__main__":
    main()

