"""Regression tests for data consistency"""
import pytest
import pandas as pd
import numpy as np

@pytest.mark.regression
class TestDataConsistency:
    """Test data consistency across pipeline runs"""
    
    def test_output_deterministic(self, sample_customer_data):
        """Test that processing produces deterministic output"""
        
        def process_data(data):
            """Simulate data processing"""
            processed = data.copy()
            # Add deterministic transformations
            processed['customer_score'] = (
                processed['total_spent'] * 0.1 + 
                processed['age'] * 0.5
            ).round(2)
            return processed
        
        # Process same data twice
        result1 = process_data(sample_customer_data)
        result2 = process_data(sample_customer_data)
        
        # Results should be identical
        pd.testing.assert_frame_equal(result1, result2, "Results should be deterministic")
    
    def test_data_volume_consistency(self, sample_customer_data):
        """Test that data volumes remain consistent"""
        
        # Baseline expectations
        expected_row_count = 1000
        expected_columns = {'customer_id', 'name', 'email', 'created_date', 
                          'country', 'age', 'total_spent', 'status'}
        
        # Validate current data matches expectations
        assert len(sample_customer_data) == expected_row_count,             f"Expected {expected_row_count} rows, got {len(sample_customer_data)}"
        
        actual_columns = set(sample_customer_data.columns)
        assert actual_columns == expected_columns,             f"Column mismatch. Expected: {expected_columns}, Got: {actual_columns}"
