"""
Main Cleaning Service - The Heart of the System
"""
import pandas as pd
from typing import Dict, List
import logging
from datetime import datetime

from backend.core.cleaners import PhoneCleaner, EmailCleaner, NameCleaner, CompanyCleaner
from backend.core.detectors import ColumnDetector, DuplicateFinder
from backend.core.classifiers import GeographicClassifier, IndustryClassifier, SizeClassifier

logger = logging.getLogger(__name__)


class CleaningService:
    """Main Data Cleaning Service"""
    
    def __init__(self, settings: Dict):
        """
        Initialize cleaning service
        
        Args:
            settings: Cleaning settings dictionary
        """
        self.settings = settings
        self.stats = {
            'total_rows': 0,
            'processed_rows': 0,
            'valid_rows': 0,
            'error_rows': 0,
            'duplicate_rows': 0,
            'start_time': None,
            'end_time': None
        }
    
    def load_file(self, file_path: str) -> pd.DataFrame:
        """Load file into DataFrame - Optimized for large files"""
        logger.info(f"Loading file: {file_path}")
        
        try:
            if file_path.endswith('.csv'):
                # Use efficient CSV reading with low_memory option
                df = pd.read_csv(file_path, low_memory=False)
            elif file_path.endswith(('.xlsx', '.xls')):
                # For Excel, read with optimal engine
                df = pd.read_excel(file_path, engine='openpyxl' if file_path.endswith('.xlsx') else None)
            else:
                raise ValueError(f"Unsupported file type: {file_path}")
            
            rows, cols = len(df), len(df.columns)
            logger.info(f"✅ Successfully loaded {rows:,} rows, {cols} columns")
            
            # ✅ CONVERT ALL NON-SERIALIZABLE TYPES TO STRINGS
            logger.info("Converting all data types to JSON-serializable format...")
            for col in df.columns:
                # Check if column has datetime/timedelta types
                if df[col].dtype == 'datetime64[ns]' or df[col].dtype == 'timedelta64[ns]':
                    df[col] = df[col].astype(str).replace('NaT', '')
                elif df[col].dtype == 'object':
                    # Convert any remaining datetime/timedelta objects
                    df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) and not isinstance(x, (str, int, float, bool)) else x)
            
            # Replace NaN with empty strings
            df = df.fillna('')
            logger.info("✅ Data types converted successfully")
            
            # Validate row count
            max_rows = self.settings.get('max_rows_limit', 100000)
            if rows > max_rows:
                logger.warning(f"⚠️ File has {rows:,} rows, exceeding limit of {max_rows:,}. Processing first {max_rows:,} rows.")
                df = df.head(max_rows)
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Failed to load file: {str(e)}")
            raise
    
    def detect_columns(self, df: pd.DataFrame) -> Dict:
        """Detect column types automatically"""
        logger.info("Detecting column types...")
        
        if not self.settings.get('detect_columns', True):
            return {}
        
        detections = ColumnDetector.detect_all_columns(df)
        
        # Log detections
        for col, info in detections.items():
            logger.info(
                f"Column '{col}' detected as '{info['detected_type']}' "
                f"(confidence: {info['confidence']:.2f}, method: {info['method']})"
            )
        
        return detections
    
    def clean_phones(self, df: pd.DataFrame, phone_columns: List[str]) -> pd.DataFrame:
        """Clean phone numbers"""
        if not self.settings.get('clean_phones', True):
            return df
        
        logger.info(f"Cleaning phone numbers in {len(phone_columns)} columns...")
        
        for col in phone_columns:
            if col not in df.columns:
                continue
            
            # Create result columns
            df[f'{col}_clean'] = ''
            df[f'{col}_country'] = ''
            df[f'{col}_status'] = ''
            df[f'{col}_type'] = ''
            df[f'{col}_error'] = ''
            
            # Clean each phone
            for idx, phone in df[col].items():
                result = PhoneCleaner.clean(phone)
                
                df.at[idx, f'{col}_clean'] = result.get('clean', '')
                df.at[idx, f'{col}_country'] = result.get('country', '')
                df.at[idx, f'{col}_status'] = result.get('status', '')
                df.at[idx, f'{col}_type'] = result.get('type', '')
                df.at[idx, f'{col}_error'] = result.get('error', '')
            
            logger.info(f"Cleaned column: {col}")
        
        return df
    
    def clean_emails(self, df: pd.DataFrame, email_columns: List[str]) -> pd.DataFrame:
        """Clean email addresses"""
        if not self.settings.get('clean_emails', True):
            return df
        
        logger.info(f"Cleaning emails in {len(email_columns)} columns...")
        
        for col in email_columns:
            if col not in df.columns:
                continue
            
            # Create result columns
            df[f'{col}_clean'] = ''
            df[f'{col}_status'] = ''
            df[f'{col}_error'] = ''
            df[f'{col}_is_disposable'] = False
            df[f'{col}_is_role_based'] = False
            
            # Clean each email
            for idx, email in df[col].items():
                result = EmailCleaner.clean(email)
                
                df.at[idx, f'{col}_clean'] = result.get('clean', '')
                df.at[idx, f'{col}_status'] = result.get('status', '')
                df.at[idx, f'{col}_error'] = result.get('error', '')
                df.at[idx, f'{col}_is_disposable'] = result.get('is_disposable', False)
                df.at[idx, f'{col}_is_role_based'] = result.get('is_role_based', False)
            
            logger.info(f"Cleaned column: {col}")
        
        return df
    
    def clean_names(self, df: pd.DataFrame, name_columns: List[str]) -> pd.DataFrame:
        """Clean names"""
        if not self.settings.get('clean_names', False):
            return df
        
        logger.info(f"Cleaning names in {len(name_columns)} columns...")
        
        for col in name_columns:
            if col not in df.columns:
                continue
            
            df[f'{col}_clean'] = ''
            df[f'{col}_status'] = ''
            
            for idx, name in df[col].items():
                result = NameCleaner.clean(name)
                df.at[idx, f'{col}_clean'] = result.get('clean', '')
                df.at[idx, f'{col}_status'] = result.get('status', '')
            
            logger.info(f"Cleaned column: {col}")
        
        return df
    
    def clean_companies(self, df: pd.DataFrame, company_columns: List[str]) -> pd.DataFrame:
        """Clean company names"""
        if not self.settings.get('clean_companies', False):
            return df
        
        logger.info(f"Cleaning companies in {len(company_columns)} columns...")
        
        for col in company_columns:
            if col not in df.columns:
                continue
            
            df[f'{col}_clean'] = ''
            df[f'{col}_type'] = ''
            
            for idx, company in df[col].items():
                result = CompanyCleaner.clean(company)
                df.at[idx, f'{col}_clean'] = result.get('clean', '')
                df.at[idx, f'{col}_type'] = result.get('type', '')
            
            logger.info(f"Cleaned column: {col}")
        
        return df
    
    def classify_geographic(self, df: pd.DataFrame, detections: Dict) -> pd.DataFrame:
        """Classify geographic information"""
        if not self.settings.get('classify_geographic', True):
            return df
        
        logger.info("Classifying geographic information...")
        
        # Find relevant columns
        phone_cols = [col for col, info in detections.items() 
                      if info['detected_type'] == 'phone']
        city_cols = [col for col, info in detections.items() 
                     if info['detected_type'] == 'city']
        region_cols = [col for col, info in detections.items() 
                       if info['detected_type'] == 'region']
        
        # Add classification columns
        df['geo_country'] = ''
        df['geo_country_en'] = ''
        df['geo_country_code'] = ''
        df['geo_region'] = ''
        df['geo_city'] = ''
        
        for idx in df.index:
            # Get country code from phone
            country_code = ''
            if phone_cols:
                phone_col = phone_cols[0]
                if f'{phone_col}_clean' in df.columns:
                    phone = df.at[idx, f'{phone_col}_clean']
                    if phone:
                        # Extract country code
                        from backend.core.cleaners.phone_cleaner import PhoneCleaner
                        country_code = PhoneCleaner.detect_country_code(phone)
            
            # Get city and region
            city = df.at[idx, city_cols[0]] if city_cols else None
            region = df.at[idx, region_cols[0]] if region_cols else None
            
            # Classify
            result = GeographicClassifier.classify_location(
                city=city,
                region=region,
                country_code=country_code
            )
            
            df.at[idx, 'geo_country'] = result.get('country', '')
            df.at[idx, 'geo_country_en'] = result.get('country_en', '')
            df.at[idx, 'geo_country_code'] = result.get('country_code', '')
            df.at[idx, 'geo_region'] = result.get('region', '')
            df.at[idx, 'geo_city'] = result.get('city', '')
        
        logger.info("Geographic classification completed")
        return df
    
    def classify_industry(self, df: pd.DataFrame, detections: Dict) -> pd.DataFrame:
        """Classify industry/activity"""
        if not self.settings.get('classify_industry', False):
            return df
        
        logger.info("Classifying industry...")
        
        # Find company and activity columns
        company_cols = [col for col, info in detections.items() 
                        if info['detected_type'] == 'company']
        activity_cols = [col for col, info in detections.items() 
                         if info['detected_type'] == 'activity']
        
        df['industry'] = ''
        df['industry_en'] = ''
        df['industry_category'] = ''
        df['industry_confidence'] = 0.0
        
        for idx in df.index:
            company = df.at[idx, company_cols[0]] if company_cols else ''
            activity = df.at[idx, activity_cols[0]] if activity_cols else ''
            
            result = IndustryClassifier.classify_by_name(company, activity)
            
            df.at[idx, 'industry'] = result.get('industry', '')
            df.at[idx, 'industry_en'] = result.get('industry_en', '')
            df.at[idx, 'industry_category'] = result.get('category', '')
            df.at[idx, 'industry_confidence'] = result.get('confidence', 0.0)
        
        logger.info("Industry classification completed")
        return df
    
    def remove_duplicates(self, df: pd.DataFrame, key_columns: List[str]) -> pd.DataFrame:
        """Remove duplicate rows"""
        if not self.settings.get('remove_duplicates', True):
            return df
        
        logger.info("Removing duplicates...")
        
        initial_count = len(df)
        
        # Mark duplicates
        df = DuplicateFinder.mark_duplicates(df, key_columns)
        
        duplicate_count = df['is_duplicate'].sum()
        
        logger.info(f"Found {duplicate_count} duplicates out of {initial_count} rows")
        
        self.stats['duplicate_rows'] = duplicate_count
        
        return df
    
    def calculate_quality_score(self, df: pd.DataFrame) -> float:
        """Calculate overall quality score"""
        scores = []
        
        # Check phone quality
        phone_status_cols = [col for col in df.columns if col.endswith('_status') and 'phone' in col.lower()]
        for col in phone_status_cols:
            valid_count = (df[col] == 'valid').sum()
            total_count = len(df)
            if total_count > 0:
                scores.append(valid_count / total_count * 100)
        
        # Check email quality
        email_status_cols = [col for col in df.columns if col.endswith('_status') and 'email' in col.lower()]
        for col in email_status_cols:
            valid_count = (df[col] == 'valid').sum()
            optional_count = (df[col] == 'optional').sum()
            total_count = len(df) - optional_count
            if total_count > 0:
                scores.append(valid_count / total_count * 100)
        
        # Calculate average
        if scores:
            return sum(scores) / len(scores)
        else:
            return 0.0
    
    def process(self, file_path: str, progress_callback=None) -> Dict:
        """
        Main processing method
        
        Args:
            file_path: Path to file
            progress_callback: Function to call with progress updates
            
        Returns:
            Dictionary with results
        """
        self.stats['start_time'] = datetime.now()
        
        try:
            # Step 1: Load file
            if progress_callback:
                progress_callback(0.05, "تحميل الملف...")
            df = self.load_file(file_path)
            self.stats['total_rows'] = len(df)
            
            # Step 2: Detect columns
            if progress_callback:
                progress_callback(0.10, "الكشف التلقائي للأعمدة...")
            detections = self.detect_columns(df)
            
            # Step 3: Clean phones
            if progress_callback:
                progress_callback(0.20, "تنظيف الأرقام...")
            phone_cols = [col for col, info in detections.items() 
                          if info['detected_type'] == 'phone']
            df = self.clean_phones(df, phone_cols)
            
            # Step 4: Clean emails
            if progress_callback:
                progress_callback(0.40, "تنظيف الإيميلات...")
            email_cols = [col for col, info in detections.items() 
                          if info['detected_type'] == 'email']
            df = self.clean_emails(df, email_cols)
            
            # Step 5: Clean names
            if progress_callback:
                progress_callback(0.55, "تنظيف الأسماء...")
            name_cols = [col for col, info in detections.items() 
                         if info['detected_type'] == 'name']
            df = self.clean_names(df, name_cols)
            
            # Step 6: Clean companies
            if progress_callback:
                progress_callback(0.60, "تنظيف أسماء الشركات...")
            company_cols = [col for col, info in detections.items() 
                            if info['detected_type'] == 'company']
            df = self.clean_companies(df, company_cols)
            
            # Step 7: Geographic classification
            if progress_callback:
                progress_callback(0.75, "التصنيف الجغرافي...")
            df = self.classify_geographic(df, detections)
            
            # Step 8: Industry classification
            if progress_callback:
                progress_callback(0.85, "تصنيف الأنشطة...")
            df = self.classify_industry(df, detections)
            
            # Step 9: Remove duplicates
            if progress_callback:
                progress_callback(0.90, "إزالة التكرارات...")
            key_columns = phone_cols + email_cols
            if key_columns:
                df = self.remove_duplicates(df, key_columns)
            
            # Step 10: Calculate quality
            if progress_callback:
                progress_callback(0.95, "حساب الجودة...")
            quality_score = self.calculate_quality_score(df)
            
            # Final stats
            self.stats['end_time'] = datetime.now()
            self.stats['processed_rows'] = len(df)
            self.stats['quality_score'] = quality_score
            
            # Count valid/error rows
            if phone_cols:
                phone_col = phone_cols[0]
                if f'{phone_col}_status' in df.columns:
                    self.stats['valid_rows'] = (df[f'{phone_col}_status'] == 'valid').sum()
                    self.stats['error_rows'] = (df[f'{phone_col}_status'] == 'error').sum()
            
            if progress_callback:
                progress_callback(1.0, "اكتمل!")
            
            logger.info("Processing completed successfully")
            logger.info(f"Quality Score: {quality_score:.2f}%")
            
            return {
                'success': True,
                'dataframe': df,
                'stats': self.stats,
                'detections': detections
            }
            
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'stats': self.stats
            }

