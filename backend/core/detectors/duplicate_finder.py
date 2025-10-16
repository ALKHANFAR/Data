"""
Duplicate Finder
"""
from typing import List, Dict
import pandas as pd


class DuplicateFinder:
    """Smart Duplicate Finder"""
    
    @staticmethod
    def find_exact_duplicates(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Find exact duplicates based on specified columns"""
        return df[df.duplicated(subset=columns, keep=False)]
    
    @staticmethod
    def find_fuzzy_duplicates(values: List[str], threshold: int = 85) -> List[Dict]:
        """
        Find fuzzy duplicates in a list of values
        
        Args:
            values: List of strings to compare
            threshold: Similarity threshold (0-100)
            
        Returns:
            List of duplicate groups
        """
        try:
            from fuzzywuzzy import fuzz
        except ImportError:
            # Fallback to simple comparison if fuzzywuzzy not available
            return DuplicateFinder._simple_fuzzy_duplicates(values)
        
        duplicates = []
        checked = set()
        
        for i, val1 in enumerate(values):
            if i in checked:
                continue
            
            group = [val1]
            checked.add(i)
            
            for j, val2 in enumerate(values[i+1:], start=i+1):
                if j in checked:
                    continue
                
                similarity = fuzz.ratio(str(val1).lower(), str(val2).lower())
                
                if similarity >= threshold:
                    group.append(val2)
                    checked.add(j)
            
            if len(group) > 1:
                duplicates.append({
                    'group': group,
                    'count': len(group)
                })
        
        return duplicates
    
    @staticmethod
    def _simple_fuzzy_duplicates(values: List[str]) -> List[Dict]:
        """Simple fuzzy matching without fuzzywuzzy"""
        duplicates = []
        checked = set()
        
        for i, val1 in enumerate(values):
            if i in checked:
                continue
            
            group = [val1]
            checked.add(i)
            
            for j, val2 in enumerate(values[i+1:], start=i+1):
                if j in checked:
                    continue
                
                # Simple similarity: check if one contains the other
                if str(val1).lower() in str(val2).lower() or str(val2).lower() in str(val1).lower():
                    group.append(val2)
                    checked.add(j)
            
            if len(group) > 1:
                duplicates.append({
                    'group': group,
                    'count': len(group)
                })
        
        return duplicates
    
    @staticmethod
    def mark_duplicates(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Add duplicate marker column"""
        df['is_duplicate'] = df.duplicated(subset=columns, keep='first')
        return df

