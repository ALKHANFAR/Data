"""
Test Script for All Data Cleaners
"""
from backend.core.cleaners import PhoneCleaner, EmailCleaner, NameCleaner, CompanyCleaner


def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_phone_cleaner():
    """Test Phone Cleaner"""
    print_section("اختبار Phone Cleaner - 78 دولة")
    
    test_cases = [
        # Saudi Arabia
        ("966501234567", "السعودية - جوال"),
        ("00966501234567", "السعودية - مع 00"),
        ("+966501234567", "السعودية - مع +"),
        ("0501234567", "السعودية - محلي"),
        ("966112345678", "السعودية - أرضي"),
        
        # UAE
        ("971501234567", "الإمارات - جوال"),
        ("0501234567", "الإمارات - محلي"),
        ("971212345678", "الإمارات - أرضي"),
        
        # Egypt
        ("201012345678", "مصر - جوال"),
        ("01012345678", "مصر - محلي"),
        ("20212345678", "مصر - أرضي"),
        
        # Kuwait
        ("96550123456", "الكويت - جوال"),
        ("96522345678", "الكويت - أرضي"),
        
        # USA
        ("12025551234", "أمريكا"),
        
        # UK
        ("447700900123", "بريطانيا - جوال"),
        ("442071234567", "بريطانيا - أرضي"),
        
        # Errors
        ("123", "قصير جداً"),
        ("", "فارغ"),
        ("911", "رقم طوارئ"),
        ("abc123xyz", "مع حروف"),
        ("٠١٠١٢٣٤٥٦٧٨", "أرقام عربية"),
    ]
    
    for phone, description in test_cases:
        result = PhoneCleaner.clean(phone)
        print(f"\n📱 {description}")
        print(f"   المدخل: {phone}")
        print(f"   النتيجة: {result['status']}")
        if result['status'] == 'valid':
            print(f"   ✅ نظيف: {result['clean']}")
            print(f"   🌍 الدولة: {result['country']}")
            print(f"   📞 النوع: {result['type']}")
        else:
            print(f"   ❌ خطأ: {result['error']}")
            print(f"   📂 التصنيف: {result['category']}")


def test_email_cleaner():
    """Test Email Cleaner"""
    print_section("اختبار Email Cleaner - 15 فحص")
    
    test_cases = [
        ("user@example.com", "إيميل صحيح"),
        ("User@Example.COM", "إيميل بأحرف كبيرة"),
        ("user.name@example.co.uk", "إيميل مركب"),
        ("user+tag@example.com", "إيميل مع +"),
        ("", "فارغ"),
        ("invalid", "بدون @"),
        ("invalid@", "@ في النهاية"),
        ("@invalid.com", "@ في البداية"),
        ("user@@example.com", "@ مكررة"),
        ("user@.com", "نقطة في البداية"),
        ("user@example.", "نقطة في النهاية"),
        ("user..name@example.com", "نقاط متتالية"),
        ("user@tempmail.com", "إيميل مؤقت"),
        ("info@example.com", "إيميل وظيفي"),
        ("user@e.c", "امتداد قصير"),
    ]
    
    for email, description in test_cases:
        result = EmailCleaner.clean(email)
        print(f"\n📧 {description}")
        print(f"   المدخل: {email}")
        print(f"   النتيجة: {result['status']}")
        if result['status'] == 'valid':
            print(f"   ✅ نظيف: {result['clean']}")
            if result['is_role_based']:
                print(f"   ⚠️  تنبيه: إيميل وظيفي")
        else:
            if result['status'] == 'error':
                print(f"   ❌ خطأ: {result['error']}")
                print(f"   📂 التصنيف: {result['category']}")


def test_name_cleaner():
    """Test Name Cleaner"""
    print_section("اختبار Name Cleaner")
    
    test_cases = [
        ("ahmed ali", "اسم بالإنجليزية"),
        ("أحمد علي", "اسم بالعربية"),
        ("AHMED ALI", "أحرف كبيرة"),
        ("ahmed123ali", "مع أرقام"),
        ("ahmed   ali", "مسافات زائدة"),
        ("a", "قصير جداً"),
        ("", "فارغ"),
        ("#ERROR", "خطأ في البيانات"),
    ]
    
    for name, description in test_cases:
        result = NameCleaner.clean(name)
        print(f"\n👤 {description}")
        print(f"   المدخل: {name}")
        print(f"   النتيجة: {result['status']}")
        if result['status'] == 'valid':
            print(f"   ✅ نظيف: {result['clean']}")
        elif result['status'] == 'error':
            print(f"   ❌ خطأ: {result['error']}")


def test_company_cleaner():
    """Test Company Cleaner"""
    print_section("اختبار Company Cleaner")
    
    test_cases = [
        ("شركة النجاح للتجارة", "شركة عربية"),
        ("مؤسسة البناء للمقاولات", "مؤسسة"),
        ("مكتب الاستشارات", "مكتب"),
        ("شركة   النجاح", "مسافات زائدة"),
        ("شركة النجاح....", "نقاط زائدة"),
        ("", "فارغ"),
        ("#ERROR", "خطأ في البيانات"),
    ]
    
    for company, description in test_cases:
        result = CompanyCleaner.clean(company)
        print(f"\n🏢 {description}")
        print(f"   المدخل: {company}")
        print(f"   النتيجة: {result['status']}")
        if result['status'] == 'valid':
            print(f"   ✅ نظيف: {result['clean']}")
            if result['type']:
                print(f"   🏷️  النوع: {result['type']}")
        elif result['status'] == 'error':
            print(f"   ❌ خطأ: {result['error']}")


def test_statistics():
    """Test and show statistics"""
    print_section("إحصائيات شاملة")
    
    # Phone statistics
    phones = [
        "966501234567", "971501234567", "201012345678",
        "96550123456", "12025551234", "447700900123",
        "966112345678", "123", "", "911"
    ]
    
    phone_stats = {'valid': 0, 'error': 0, 'mobile': 0, 'landline': 0}
    
    for phone in phones:
        result = PhoneCleaner.clean(phone)
        if result['status'] == 'valid':
            phone_stats['valid'] += 1
            if result['type'] == 'mobile':
                phone_stats['mobile'] += 1
        else:
            phone_stats['error'] += 1
            if result['type'] == 'landline':
                phone_stats['landline'] += 1
    
    print(f"\n📊 إحصائيات الهواتف:")
    print(f"   ✅ صحيح: {phone_stats['valid']}")
    print(f"   📱 جوال: {phone_stats['mobile']}")
    print(f"   📞 أرضي: {phone_stats['landline']}")
    print(f"   ❌ خطأ: {phone_stats['error']}")
    
    # Email statistics
    emails = [
        "user@example.com", "invalid", "info@example.com",
        "user@tempmail.com", "", "user@@example.com"
    ]
    
    email_stats = {'valid': 0, 'error': 0, 'optional': 0, 'role_based': 0}
    
    for email in emails:
        result = EmailCleaner.clean(email)
        email_stats[result['status']] += 1
        if result.get('is_role_based'):
            email_stats['role_based'] += 1
    
    print(f"\n📊 إحصائيات الإيميلات:")
    print(f"   ✅ صحيح: {email_stats['valid']}")
    print(f"   ⚠️  وظيفي: {email_stats['role_based']}")
    print(f"   ❌ خطأ: {email_stats['error']}")
    print(f"   ⭕ اختياري: {email_stats['optional']}")


def main():
    """Run all tests"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║          🧪 اختبار نظام تنظيف البيانات الشامل             ║")
    print("║                                                            ║")
    print("║  📱 Phone Cleaner - 78 دولة                               ║")
    print("║  📧 Email Cleaner - 15 فحص                                ║")
    print("║  👤 Name Cleaner                                          ║")
    print("║  🏢 Company Cleaner                                       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    test_phone_cleaner()
    test_email_cleaner()
    test_name_cleaner()
    test_company_cleaner()
    test_statistics()
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                    ✅ اكتمل الاختبار                       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n")


if __name__ == "__main__":
    main()

