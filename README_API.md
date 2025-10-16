# 🚀 Data Cleaning System - Complete API Documentation

## نظام تنظيف البيانات الشامل - توثيق API كامل

---

## 📋 المحتويات

1. [نظرة عامة](#نظرة-عامة)
2. [التثبيت والتشغيل](#التثبيت-والتشغيل)
3. [هيكل المشروع](#هيكل-المشروع)
4. [API Endpoints](#api-endpoints)
5. [أمثلة الاستخدام](#أمثلة-الاستخدام)
6. [قاعدة البيانات](#قاعدة-البيانات)

---

## 🎯 نظرة عامة

نظام متكامل لتنظيف وتصنيف البيانات مع واجهة API احترافية

### المميزات الرئيسية

#### 🧹 Data Cleaners
- ✅ **Phone Cleaner**: 78 دولة، فصل جوال/أرضي
- ✅ **Email Cleaner**: 15 فحص شامل
- ✅ **Name Cleaner**: عربي + إنجليزي
- ✅ **Company Cleaner**: كشف نوع الشركة

#### 🔍 Smart Detectors
- ✅ **Column Detector**: كشف تلقائي للأعمدة
- ✅ **Duplicate Finder**: كشف التكرارات

#### 🏷️ Classifiers
- ✅ **Geographic**: تصنيف جغرافي (دول، مناطق، مدن)
- ✅ **Industry**: تصنيف القطاعات (10 قطاعات)
- ✅ **Size**: تصنيف حجم الشركات

#### 🌐 REST API
- ✅ FastAPI Framework
- ✅ Authentication & Authorization
- ✅ File Upload (Excel, CSV, Google Sheets)
- ✅ Background Processing
- ✅ Real-time Progress Tracking
- ✅ Multiple Export Formats

---

## 🚀 التثبيت والتشغيل

### المتطلبات

```bash
Python 3.9+
pip
```

### خطوات التثبيت

```bash
# 1. Clone المشروع
cd /path/to/project

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. نسخ ملف البيئة
cp .env.example .env

# 4. تعديل إعدادات .env حسب الحاجة

# 5. إنشاء قاعدة البيانات
python -c "from backend.db.session import init_db; init_db()"

# 6. تشغيل السيرفر
python main.py
```

### الوصول للتطبيق

```
API: http://localhost:8000
Docs: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

---

## 📁 هيكل المشروع

```
data/
├── backend/
│   ├── config/
│   │   ├── countries.py       # 78 دولة
│   │   └── settings.py        # إعدادات التطبيق
│   ├── core/
│   │   ├── cleaners/          # منظفات البيانات
│   │   │   ├── phone_cleaner.py
│   │   │   ├── email_cleaner.py
│   │   │   ├── name_cleaner.py
│   │   │   └── company_cleaner.py
│   │   ├── detectors/         # كاشفات ذكية
│   │   │   ├── column_detector.py
│   │   │   └── duplicate_finder.py
│   │   └── classifiers/       # مصنفات
│   │       ├── geographic.py
│   │       ├── industry.py
│   │       └── size.py
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── upload.py
│   │       │   ├── cleaning.py
│   │       │   ├── results.py
│   │       │   └── export.py
│   │       └── router.py
│   └── db/
│       ├── base.py
│       ├── session.py
│       └── models/
│           ├── user.py
│           ├── file.py
│           └── job.py
├── main.py                    # FastAPI App
├── test_cleaners.py           # اختبار المنظفات
├── test_advanced.py           # اختبار المميزات المتقدمة
├── test_api.py                # اختبار API
└── requirements.txt
```

---

## 🌐 API Endpoints

### Root & Health

#### GET `/`
```json
{
  "app": "Data Cleaning System",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "api": "/api/v1"
}
```

#### GET `/health`
```json
{
  "status": "healthy",
  "app": "Data Cleaning System",
  "version": "1.0.0"
}
```

---

### 🔐 Authentication

#### POST `/api/v1/auth/register`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "strongpassword123",
  "name": "أحمد محمد"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### POST `/api/v1/auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET `/api/v1/auth/me`

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "أحمد محمد"
}
```

---

### 📤 Upload

#### POST `/api/v1/upload/file`

**Request:** Multipart Form Data
```
file: companies.xlsx
```

**Response:**
```json
{
  "file_id": "a1b2c3d4-e5f6-4789-a1b2-c3d4e5f67890",
  "filename": "companies.xlsx",
  "size": 1048576,
  "rows": 50000,
  "columns": 8,
  "uploaded_at": "2024-01-15T10:30:00",
  "status": "uploaded"
}
```

#### POST `/api/v1/upload/google-sheets`

**Request:**
```json
{
  "url": "https://docs.google.com/spreadsheets/d/ABC123/edit"
}
```

**Response:**
```json
{
  "file_id": "x1y2z3a4-b5c6-7890-x1y2-z3a4b5c67890",
  "filename": "google_sheets_import.csv",
  "size": 2097152,
  "rows": 75000,
  "columns": 10,
  "uploaded_at": "2024-01-15T10:35:00",
  "status": "uploaded"
}
```

---

### 🧹 Cleaning

#### POST `/api/v1/clean/start`

**Request:**
```json
{
  "file_id": "a1b2c3d4-e5f6-4789-a1b2-c3d4e5f67890",
  "settings": {
    "clean_phones": true,
    "clean_emails": true,
    "clean_names": false,
    "clean_companies": false,
    "classify_geographic": true,
    "classify_industry": true,
    "classify_size": false,
    "remove_duplicates": true,
    "detect_columns": true
  }
}
```

**Response:**
```json
{
  "job_id": "j1k2l3m4-n5o6-7890-j1k2-l3m4n5o67890",
  "file_id": "a1b2c3d4-e5f6-4789-a1b2-c3d4e5f67890",
  "status": "processing",
  "started_at": "2024-01-15T10:40:00",
  "estimated_time": 300
}
```

#### GET `/api/v1/clean/progress/{job_id}`

**Response:**
```json
{
  "job_id": "j1k2l3m4-n5o6-7890-j1k2-l3m4n5o67890",
  "status": "processing",
  "progress": 0.65,
  "current_step": "تنظيف الإيميلات",
  "processed_rows": 32500,
  "total_rows": 50000,
  "speed": 1250.5,
  "estimated_time_remaining": 14,
  "errors_count": 3420,
  "valid_count": 29080,
  "duplicate_count": 850
}
```

#### POST `/api/v1/clean/cancel/{job_id}`

**Response:**
```json
{
  "message": "Job cancelled successfully",
  "job_id": "j1k2l3m4-n5o6-7890-j1k2-l3m4n5o67890"
}
```

---

### 📊 Results

#### GET `/api/v1/results/{job_id}/summary`

**Response:**
```json
{
  "job_id": "j1k2l3m4-n5o6-7890-j1k2-l3m4n5o67890",
  "total_rows": 50000,
  "valid_rows": 42350,
  "error_rows": 6500,
  "duplicate_rows": 1150,
  "quality_score": 94.2,
  "processing_time": 245,
  "completed_at": "2024-01-15T10:44:05"
}
```

#### GET `/api/v1/results/{job_id}/preview?page=1&page_size=50`

**Response:**
```json
{
  "job_id": "j1k2l3m4-n5o6-7890-j1k2-l3m4n5o67890",
  "total_rows": 50000,
  "data": [
    {
      "index": 0,
      "data": {
        "name": "شركة النجاح للمقاولات",
        "phone": "966501234567",
        "email": "info@najah.com",
        "country": "السعودية",
        "city": "الرياض",
        "industry": "مقاولات"
      },
      "status": "valid",
      "errors": []
    },
    {
      "index": 1,
      "data": {
        "name": "مؤسسة البناء",
        "phone": "966112345678",
        "email": "contact@albinaa.com"
      },
      "status": "error",
      "errors": ["رقم أرضي (يبدأ بـ 11)"]
    }
  ],
  "page": 1,
  "page_size": 50,
  "has_more": true
}
```

#### GET `/api/v1/results/{job_id}/stats`

**Response:**
```json
{
  "job_id": "j1k2l3m4-n5o6-7890-j1k2-l3m4n5o67890",
  "total_records": 50000,
  "quality_breakdown": {
    "excellent": 32710,
    "good": 9640,
    "medium": 4285,
    "poor": 3365
  },
  "error_categories": {
    "invalid_phone": 2710,
    "invalid_email": 1910,
    "missing_data": 730,
    "duplicate": 1150
  },
  "country_distribution": {
    "السعودية": 32500,
    "الإمارات": 10000,
    "الكويت": 5000,
    "قطر": 2500
  },
  "phone_types": {
    "mobile": 41000,
    "landline": 4000,
    "invalid": 5000
  }
}
```

---

### 📥 Export

#### POST `/api/v1/export/`

**Request:**
```json
{
  "job_id": "j1k2l3m4-n5o6-7890-j1k2-l3m4n5o67890",
  "format": "xlsx",
  "filter_status": "valid",
  "include_stats": true
}
```

**Response:**
```json
{
  "export_id": "e1f2g3h4-i5j6-7890-e1f2-g3h4i5j67890",
  "download_url": "/api/v1/export/e1f2g3h4-i5j6-7890-e1f2-g3h4i5j67890/download",
  "format": "xlsx",
  "size": 2548736,
  "expires_at": "2024-01-16T10:44:05"
}
```

#### GET `/api/v1/export/{job_id}/channel/{channel}`

Channels: `email`, `whatsapp`, `call`

**Response:**
```json
{
  "job_id": "j1k2l3m4-n5o6-7890-j1k2-l3m4n5o67890",
  "channel": "whatsapp",
  "records": 42350,
  "download_url": "/api/v1/export/j1k2l3m4-n5o6-7890-j1k2-l3m4n5o67890/channel/whatsapp/download"
}
```

---

## 💡 أمثلة الاستخدام

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Upload file
with open('companies.xlsx', 'rb') as f:
    files = {'file': f}
    response = requests.post(f"{BASE_URL}/upload/file", files=files)
    file_id = response.json()['file_id']

# 2. Start cleaning
cleaning_request = {
    "file_id": file_id,
    "settings": {
        "clean_phones": True,
        "clean_emails": True,
        "classify_geographic": True,
        "remove_duplicates": True
    }
}
response = requests.post(f"{BASE_URL}/clean/start", json=cleaning_request)
job_id = response.json()['job_id']

# 3. Check progress
import time
while True:
    response = requests.get(f"{BASE_URL}/clean/progress/{job_id}")
    progress = response.json()
    print(f"Progress: {progress['progress']:.0%}")
    
    if progress['status'] == 'completed':
        break
    
    time.sleep(5)

# 4. Get results
response = requests.get(f"{BASE_URL}/results/{job_id}/summary")
print(response.json())

# 5. Export
export_request = {
    "job_id": job_id,
    "format": "xlsx",
    "filter_status": "valid"
}
response = requests.post(f"{BASE_URL}/export/", json=export_request)
download_url = response.json()['download_url']
print(f"Download: {BASE_URL}{download_url}")
```

---

## 🗄️ قاعدة البيانات

### Models

#### User
```python
- id: Integer
- email: String (unique)
- hashed_password: String
- name: String
- is_active: Boolean
- is_superuser: Boolean
- created_at: DateTime
- updated_at: DateTime
```

#### UploadedFile
```python
- id: Integer
- file_id: String (unique)
- user_id: ForeignKey(User)
- filename: String
- file_path: String
- file_size: BigInteger
- rows_count: Integer
- columns_count: Integer
- status: String
- created_at: DateTime
```

#### CleaningJob
```python
- id: Integer
- job_id: String (unique)
- file_id: ForeignKey(UploadedFile)
- user_id: ForeignKey(User)
- status: String
- progress: Float
- current_step: String
- settings: JSON
- total_rows: Integer
- processed_rows: Integer
- valid_rows: Integer
- error_rows: Integer
- duplicate_rows: Integer
- quality_score: Float
- started_at: DateTime
- completed_at: DateTime
- processing_time: Integer
- created_at: DateTime
- updated_at: DateTime
```

---

## 🧪 الاختبار

```bash
# اختبار المنظفات الأساسية
python test_cleaners.py

# اختبار المميزات المتقدمة
python test_advanced.py

# اختبار API (يجب تشغيل السيرفر أولاً)
python main.py &
python test_api.py
```

---

## 📝 ملاحظات

1. **الأمان**: غيّر `SECRET_KEY` في production
2. **Database**: استخدم PostgreSQL في production بدلاً من SQLite
3. **Background Tasks**: استخدم Celery + Redis للمعالجة الثقيلة
4. **File Storage**: استخدم S3 أو Cloud Storage في production
5. **Rate Limiting**: أضف rate limiting في production

---

## 🚀 Deployment

### Using Docker

```bash
# Build
docker build -t data-cleaning-api .

# Run
docker run -p 8000:8000 data-cleaning-api
```

### Using Docker Compose

```bash
docker-compose up -d
```

---

**صُنع بـ ❤️ | FastAPI + SQLAlchemy + Pandas**

