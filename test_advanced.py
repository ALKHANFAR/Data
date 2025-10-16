"""
Test Advanced Features: Detectors & Classifiers
"""
import pandas as pd
from backend.core.detectors import ColumnDetector, DuplicateFinder
from backend.core.classifiers import GeographicClassifier, IndustryClassifier, SizeClassifier


def print_section(title):
    """Print section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_column_detector():
    """Test Column Detector"""
    print_section("اختبار Column Detector - كشف تلقائي")
    
    # Create sample dataframe
    data = {
        'رقم الجوال': ['966501234567', '966551234567', '966501111111'],
        'البريد الإلكتروني': ['user1@example.com', 'user2@test.com', 'user3@demo.com'],
        'اسم الشركة': ['شركة النجاح', 'مؤسسة البناء', 'مكتب الاستشارات'],
        'المدينة': ['الرياض', 'جدة', 'الدمام'],
        'النشاط': ['مقاولات', 'تجارة', 'خدمات']
    }
    
    df = pd.DataFrame(data)
    
    # Detect all columns
    results = ColumnDetector.detect_all_columns(df)
    
    print("\n📊 نتائج الكشف التلقائي:")
    for col, info in results.items():
        print(f"\n   🔍 عمود: {col}")
        print(f"      النوع: {info['detected_type']}")
        print(f"      الثقة: {info['confidence']:.1%}")
        print(f"      الطريقة: {info['method']}")


def test_duplicate_finder():
    """Test Duplicate Finder"""
    print_section("اختبار Duplicate Finder - كشف التكرارات")
    
    # Sample data with duplicates
    data = {
        'phone': ['966501234567', '966501234567', '966551111111', '966501234567'],
        'name': ['أحمد علي', 'محمد سعيد', 'أحمد علي', 'خالد أحمد']
    }
    
    df = pd.DataFrame(data)
    
    # Find exact duplicates
    duplicates = DuplicateFinder.find_exact_duplicates(df, ['phone'])
    
    print(f"\n📊 عدد التكرارات: {len(duplicates)}")
    print("\n   التكرارات المكتشفة:")
    for idx, row in duplicates.iterrows():
        print(f"   {idx+1}. {row['phone']} - {row['name']}")
    
    # Mark duplicates
    df_marked = DuplicateFinder.mark_duplicates(df, ['phone'])
    
    print(f"\n📊 بعد التمييز:")
    for idx, row in df_marked.iterrows():
        status = "❌ مكرر" if row['is_duplicate'] else "✅ أصلي"
        print(f"   {idx+1}. {row['phone']} - {status}")


def test_geographic_classifier():
    """Test Geographic Classifier"""
    print_section("اختبار Geographic Classifier - تصنيف جغرافي")
    
    test_cases = [
        ('966', 'السعودية'),
        ('971', 'الإمارات'),
        ('965', 'الكويت'),
        ('20', 'مصر'),
        ('1', 'أمريكا'),
    ]
    
    print("\n🌍 تصنيف حسب كود الدولة:")
    for code, name in test_cases:
        result = GeographicClassifier.classify_by_phone(code)
        print(f"\n   {name} ({code}):")
        print(f"      الاسم: {result['country']}")
        print(f"      English: {result['country_en']}")
        if result.get('cities'):
            cities = result['cities'][:3]  # Show first 3
            print(f"      المدن: {', '.join(cities)}")
    
    # Test Saudi region detection
    print("\n\n🏙️ كشف المنطقة من المدينة (السعودية):")
    saudi_cities = ['الرياض', 'جدة', 'الدمام', 'أبها', 'تبوك']
    
    for city in saudi_cities:
        region = GeographicClassifier.find_saudi_region(city)
        print(f"   {city} → {region}")
    
    # Test complete location
    print("\n\n📍 تصنيف موقع كامل:")
    location = GeographicClassifier.classify_location(
        city='الرياض',
        country_code='966'
    )
    print(f"   الدولة: {location['country']}")
    print(f"   المنطقة: {location['region']}")
    print(f"   المدينة: {location['city']}")
    print(f"   الثقة: {location['confidence']:.1%}")


def test_industry_classifier():
    """Test Industry Classifier"""
    print_section("اختبار Industry Classifier - تصنيف القطاع")
    
    test_cases = [
        ('شركة المقاولات العامة', 'مقاولات بناء'),
        ('مؤسسة التجارة والتسويق', 'استيراد وتصدير'),
        ('مطعم البيك للمأكولات', ''),
        ('مكتب الاستشارات الإدارية', 'دراسات'),
        ('مصنع الأسمنت', 'إنتاج'),
        ('شركة التقنية الحديثة', 'برمجة تطبيقات'),
    ]
    
    print("\n🏭 تصنيف القطاعات:")
    for company, activity in test_cases:
        result = IndustryClassifier.classify_by_name(company, activity)
        print(f"\n   📋 {company}")
        if activity:
            print(f"      النشاط: {activity}")
        print(f"      القطاع: {result['industry']}")
        print(f"      English: {result['industry_en']}")
        print(f"      التصنيف: {result['category']}")
        print(f"      الثقة: {result['confidence']:.1%}")
        if result['matched_keywords']:
            print(f"      الكلمات: {', '.join(result['matched_keywords'])}")


def test_size_classifier():
    """Test Size Classifier"""
    print_section("اختبار Size Classifier - تصنيف الحجم")
    
    test_cases = [
        (3, 'متناهية الصغر'),
        (25, 'صغيرة'),
        (150, 'متوسطة'),
        (500, 'كبيرة'),
    ]
    
    print("\n📏 تصنيف حسب عدد الموظفين:")
    for employees, expected in test_cases:
        result = SizeClassifier.classify_by_data(employees=employees)
        print(f"\n   👥 {employees} موظف")
        print(f"      الحجم: {result['size']}")
        print(f"      English: {result['size_en']}")
        print(f"      التصنيف: {result['category']}")
        print(f"      الثقة: {result['confidence']:.1%}")


def test_integrated_workflow():
    """Test integrated workflow"""
    print_section("اختبار سير العمل المتكامل")
    
    # Create sample data
    data = {
        'الهاتف': ['966501234567', '971501234567', '965501234567'],
        'الإيميل': ['company1@example.com', 'company2@test.com', 'company3@demo.com'],
        'الشركة': ['شركة المقاولات الكبرى', 'مؤسسة التجارة الدولية', 'مكتب الاستشارات'],
        'المدينة': ['الرياض', 'دبي', 'الكويت'],
        'النشاط': ['مقاولات بناء', 'تجارة استيراد', 'استشارات إدارية'],
        'الموظفين': [200, 45, 15]
    }
    
    df = pd.DataFrame(data)
    
    print("\n🔄 معالجة متكاملة لقاعدة البيانات:")
    print(f"\n   📊 عدد السجلات: {len(df)}")
    
    # Detect columns
    print("\n   🔍 كشف الأعمدة:")
    column_detection = ColumnDetector.detect_all_columns(df)
    for col, info in column_detection.items():
        print(f"      • {col}: {info['detected_type']} ({info['confidence']:.0%})")
    
    # Process each row
    print("\n   📋 معالجة السجلات:")
    for idx, row in df.iterrows():
        print(f"\n   ═══ سجل {idx + 1} ═══")
        
        # Extract country code from phone
        phone = str(row['الهاتف'])
        if phone.startswith('966'):
            country_code = '966'
        elif phone.startswith('971'):
            country_code = '971'
        elif phone.startswith('965'):
            country_code = '965'
        else:
            country_code = None
        
        # Geographic classification
        if country_code:
            geo = GeographicClassifier.classify_by_phone(country_code)
            print(f"      🌍 الدولة: {geo['country']}")
        
        # Industry classification
        industry = IndustryClassifier.classify_by_name(
            row['الشركة'],
            row['النشاط']
        )
        print(f"      🏭 القطاع: {industry['industry']}")
        
        # Size classification
        size = SizeClassifier.classify_by_data(employees=row['الموظفين'])
        print(f"      📏 الحجم: {size['size']}")


def main():
    """Run all tests"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║       🧪 اختبار المميزات المتقدمة - Detectors & Classifiers    ║")
    print("║                                                                  ║")
    print("║  🔍 Column Detector - كشف تلقائي للأعمدة                        ║")
    print("║  🔄 Duplicate Finder - كشف التكرارات                           ║")
    print("║  🌍 Geographic Classifier - تصنيف جغرافي                        ║")
    print("║  🏭 Industry Classifier - تصنيف القطاعات                       ║")
    print("║  📏 Size Classifier - تصنيف الحجم                              ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    test_column_detector()
    test_duplicate_finder()
    test_geographic_classifier()
    test_industry_classifier()
    test_size_classifier()
    test_integrated_workflow()
    
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                    ✅ اكتمل الاختبار بنجاح                      ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print("\n")


if __name__ == "__main__":
    main()

