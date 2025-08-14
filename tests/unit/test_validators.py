"""Unit tests for validators"""
import pytest
import pandas as pd
import numpy as np
from src.validators.business_rules_validator import BusinessRulesValidator

@pytest.mark.unit
class TestBusinessRulesValidator:
    """Test suite for business rules validation"""
    
    def test_validate_completeness_success(self, business_rules_config, sample_customer_data):
        """Test successful completeness validation"""
        validator = BusinessRulesValidator(business_rules_config)
        results = validator.validate_completeness(sample_customer_data)
        
        # Check that required columns are present
        for col in business_rules_config['required_columns']:
            assert results[f'has_column_{col}'], f"Required column {col} should be present"
        
        # Check minimum row count
        assert results['meets_min_row_count'], "Should meet minimum row count"
    
    def test_validate_data_quality_success(self, business_rules_config, sample_customer_data):
        """Test successful data quality validation"""
        validator = BusinessRulesValidator(business_rules_config)
        results = validator.validate_data_quality(sample_customer_data)
        
        # Check range validations
        assert results['age_range_check'], "Age should be within valid range"
        assert results['total_spent_range_check'], "Total spent should be within valid range"
        
        # Check uniqueness
        assert results['customer_id_uniqueness_check'], "Customer ID should be unique"
        assert results['email_uniqueness_check'], "Email should be unique"
    
    def test_validate_missing_columns(self, business_rules_config):
        """Test validation with missing required columns"""
        # Create data missing required columns
        incomplete_data = pd.DataFrame({
            'name': ['Test User'],
            'age': [25]
        })
        
        validator = BusinessRulesValidator(business_rules_config)
        results = validator.validate_completeness(incomplete_data)
        
        # Should fail for missing columns
        assert not results['has_column_customer_id'], "Should detect missing customer_id"
        assert not results['has_column_email'], "Should detect missing email"
    
    def test_validate_data_ranges_failure(self, business_rules_config):
        """Test validation failure for out-of-range values"""
        # Create data with invalid ranges
        invalid_data = pd.DataFrame({
            'customer_id': [1, 2, 3],
            'name': ['User 1', 'User 2', 'User 3'],
            'email': ['user1@test.com', 'user2@test.com', 'user3@test.com'],
            'age': [150, 25, 30],  # 150 is out of range
            'total_spent': [100, 200, 60000]  # 60000 is out of range
        })
        
        validator = BusinessRulesValidator(business_rules_config)
        results = validator.validate_data_quality(invalid_data)
        
        # Should fail range checks
        assert not results['age_range_check'], "Should detect age out of range"
        assert not results['total_spent_range_check'], "Should detect total_spent out of range"
