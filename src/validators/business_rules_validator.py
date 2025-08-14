"""Business rules validation for data pipelines"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class BusinessRulesValidator:
    """Validates ETL outputs against business rules"""
    
    def __init__(self, rules_config: Dict[str, Any]):
        self.rules = rules_config
        self.validation_results = []
    
    def validate_completeness(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Validate data completeness rules"""
        results = {}
        
        # Check required columns exist
        required_cols = self.rules.get('required_columns', [])
        for col in required_cols:
            results[f'has_column_{col}'] = col in df.columns
        
        # Check minimum row count
        min_rows = self.rules.get('min_row_count', 0)
        results['meets_min_row_count'] = len(df) >= min_rows
        
        # Check for null values in critical columns
        critical_cols = self.rules.get('critical_columns', [])
        for col in critical_cols:
            if col in df.columns:
                null_percentage = (df[col].isnull().sum() / len(df)) * 100
                max_null_percent = self.rules.get('max_null_percentage', {}).get(col, 0)
                results[f'{col}_null_check'] = null_percentage <= max_null_percent
        
        return results
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Validate data quality rules"""
        results = {}
        
        # Validate data ranges
        range_rules = self.rules.get('value_ranges', {})
        for col, (min_val, max_val) in range_rules.items():
            if col in df.columns:
                within_range = df[col].between(min_val, max_val, inclusive='both').all()
                results[f'{col}_range_check'] = within_range
        
        # Validate uniqueness constraints
        unique_cols = self.rules.get('unique_columns', [])
        for col in unique_cols:
            if col in df.columns:
                is_unique = not df[col].duplicated().any()
                results[f'{col}_uniqueness_check'] = is_unique
        
        return results