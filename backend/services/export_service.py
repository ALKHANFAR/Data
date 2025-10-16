"""
Export Service
"""
import pandas as pd
from typing import Dict
import os
from datetime import datetime

from backend.config.settings import settings


class ExportService:
    """Export Service"""
    
    @staticmethod
    def export_excel(df: pd.DataFrame, filename: str, stats: Dict = None) -> str:
        """
        Export to Excel with multiple sheets
        
        Returns:
            Path to exported file
        """
        export_dir = getattr(settings, 'EXPORT_DIR', './exports')
        os.makedirs(export_dir, exist_ok=True)
        
        filepath = os.path.join(export_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='البيانات الكاملة', index=False)
            
            # Valid data only
            if 'is_duplicate' in df.columns:
                valid_df = df[df['is_duplicate'] == False]
                valid_df.to_excel(writer, sheet_name='البيانات النظيفة', index=False)
            
            # Statistics sheet
            if stats:
                stats_df = pd.DataFrame([stats])
                stats_df.to_excel(writer, sheet_name='الإحصائيات', index=False)
        
        return filepath
    
    @staticmethod
    def export_csv(df: pd.DataFrame, filename: str) -> str:
        """Export to CSV"""
        export_dir = getattr(settings, 'EXPORT_DIR', './exports')
        os.makedirs(export_dir, exist_ok=True)
        
        filepath = os.path.join(export_dir, filename)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        return filepath
    
    @staticmethod
    def export_by_channel(df: pd.DataFrame, channel: str, filename: str) -> str:
        """
        Export formatted for marketing channel
        
        Args:
            df: DataFrame
            channel: 'email', 'whatsapp', 'call'
            filename: Output filename
        """
        export_dir = getattr(settings, 'EXPORT_DIR', './exports')
        os.makedirs(export_dir, exist_ok=True)
        
        if channel == 'email':
            # Email: only valid emails
            email_cols = [col for col in df.columns if 'email' in col.lower() and col.endswith('_clean')]
            if email_cols:
                email_col = email_cols[0]
                status_col = email_col.replace('_clean', '_status')
                
                filtered_df = df[df[status_col] == 'valid'][[email_col]]
                filtered_df.columns = ['Email']
            else:
                filtered_df = df
        
        elif channel == 'whatsapp':
            # WhatsApp: only valid mobile numbers
            phone_cols = [col for col in df.columns if 'phone' in col.lower() and col.endswith('_clean')]
            if phone_cols:
                phone_col = phone_cols[0]
                type_col = phone_col.replace('_clean', '_type')
                status_col = phone_col.replace('_clean', '_status')
                
                filtered_df = df[
                    (df[status_col] == 'valid') & 
                    (df[type_col] == 'mobile')
                ][[phone_col]]
                filtered_df.columns = ['Phone']
            else:
                filtered_df = df
        
        elif channel == 'call':
            # Call: valid mobile numbers with best time info
            phone_cols = [col for col in df.columns if 'phone' in col.lower() and col.endswith('_clean')]
            if phone_cols:
                phone_col = phone_cols[0]
                status_col = phone_col.replace('_clean', '_status')
                
                filtered_df = df[df[status_col] == 'valid'][[phone_col]]
                filtered_df.columns = ['Phone']
                filtered_df['Best Time'] = '10:00 AM - 8:00 PM'
            else:
                filtered_df = df
        
        else:
            filtered_df = df
        
        filepath = os.path.join(export_dir, filename)
        filtered_df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        return filepath

