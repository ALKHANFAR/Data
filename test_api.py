"""
Test API Endpoints
"""
import requests
import json


BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"


def print_section(title):
    """Print section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_root():
    """Test root endpoint"""
    print_section("اختبار Root Endpoint")
    
    response = requests.get(f"{BASE_URL}/")
    print(f"\n✅ الحالة: {response.status_code}")
    print(f"📄 النتيجة: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_health():
    """Test health endpoint"""
    print_section("اختبار Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"\n✅ الحالة: {response.status_code}")
    print(f"📄 النتيجة: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_auth():
    """Test authentication endpoints"""
    print_section("اختبار Authentication")
    
    # Register
    print("\n🔐 تسجيل مستخدم جديد:")
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }
    response = requests.post(f"{API_URL}/auth/register", json=register_data)
    print(f"   الحالة: {response.status_code}")
    print(f"   النتيجة: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Login
    print("\n🔐 تسجيل دخول:")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{API_URL}/auth/login", json=login_data)
    print(f"   الحالة: {response.status_code}")
    print(f"   النتيجة: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Get current user
    print("\n👤 معلومات المستخدم الحالي:")
    response = requests.get(f"{API_URL}/auth/me")
    print(f"   الحالة: {response.status_code}")
    print(f"   النتيجة: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_cleaning_flow():
    """Test complete cleaning workflow"""
    print_section("اختبار سير العمل الكامل")
    
    # Start cleaning
    print("\n🧹 بدء عملية التنظيف:")
    cleaning_data = {
        "file_id": "test-file-123",
        "settings": {
            "clean_phones": True,
            "clean_emails": True,
            "clean_names": False,
            "clean_companies": False,
            "classify_geographic": True,
            "classify_industry": False,
            "classify_size": False,
            "remove_duplicates": True,
            "detect_columns": True
        }
    }
    response = requests.post(f"{API_URL}/clean/start", json=cleaning_data)
    print(f"   الحالة: {response.status_code}")
    result = response.json()
    print(f"   النتيجة: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    job_id = result.get("job_id")
    
    # Get progress
    print(f"\n📊 تتبع التقدم (Job ID: {job_id}):")
    response = requests.get(f"{API_URL}/clean/progress/{job_id}")
    print(f"   الحالة: {response.status_code}")
    print(f"   النتيجة: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_results():
    """Test results endpoints"""
    print_section("اختبار Results Endpoints")
    
    job_id = "test-job-123"
    
    # Summary
    print(f"\n📊 ملخص النتائج (Job ID: {job_id}):")
    response = requests.get(f"{API_URL}/results/{job_id}/summary")
    print(f"   الحالة: {response.status_code}")
    print(f"   النتيجة: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Preview
    print(f"\n👁️ معاينة البيانات:")
    response = requests.get(f"{API_URL}/results/{job_id}/preview?page=1&page_size=5")
    print(f"   الحالة: {response.status_code}")
    result = response.json()
    print(f"   عدد الصفوف: {len(result['data'])}")
    print(f"   الصفحة: {result['page']}")
    
    # Stats
    print(f"\n📈 إحصائيات تفصيلية:")
    response = requests.get(f"{API_URL}/results/{job_id}/stats")
    print(f"   الحالة: {response.status_code}")
    print(f"   النتيجة: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_export():
    """Test export endpoints"""
    print_section("اختبار Export Endpoints")
    
    # Create export
    print("\n📤 إنشاء ملف تصدير:")
    export_data = {
        "job_id": "test-job-123",
        "format": "xlsx",
        "filter_status": "valid",
        "include_stats": True
    }
    response = requests.post(f"{API_URL}/export/", json=export_data)
    print(f"   الحالة: {response.status_code}")
    print(f"   النتيجة: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Export by channel
    print("\n📱 تصدير حسب القناة (WhatsApp):")
    response = requests.get(f"{API_URL}/export/test-job-123/channel/whatsapp")
    print(f"   الحالة: {response.status_code}")
    print(f"   النتيجة: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def main():
    """Run all API tests"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║              🧪 اختبار API - نظام تنظيف البيانات                ║")
    print("║                                                                  ║")
    print("║  ملاحظة: تأكد من تشغيل السيرفر أولاً:                          ║")
    print("║  python main.py                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    try:
        test_root()
        test_health()
        test_auth()
        test_cleaning_flow()
        test_results()
        test_export()
        
        print("\n")
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║                    ✅ اكتمل الاختبار بنجاح                      ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print("\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ خطأ: السيرفر غير متصل!")
        print("   قم بتشغيل السيرفر أولاً: python main.py")
    except Exception as e:
        print(f"\n❌ خطأ: {str(e)}")


if __name__ == "__main__":
    main()

