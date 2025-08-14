"""Pytest configuration and fixtures"""
import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pathlib import Path
import json

@pytest.fixture(scope="session")
def test_config():
    """Load test configuration"""
    config_path = Path(__file__).parent.parent / "configs" / "test_config.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

@pytest.fixture(scope="session")
def sample_customer_data():
    """Generate sample customer data for testing"""
    np.random.seed(42)
    
    # Generate base data
    data = pd.DataFrame({
        'customer_id': range(1, 1001),
        'name': [f'Customer {i}' for i in range(1, 1001)],
        'email': [f'customer{i}@example.com' for i in range(1, 1001)],
        'created_date': pd.date_range('2023-01-01', periods=1000, freq='D'),
        'country': np.random.choice(['US', 'CA', 'UK', 'DE', 'FR'], 1000),
        'age': np.random.randint(18, 80, 1000),
        'status': np.random.choice(['ACTIVE', 'INACTIVE', 'PENDING'], 1000)
    })
    
    # Generate total_spent within valid range [0, 50000]
    # Use a more controlled distribution to ensure values are within range
    base_spent = np.random.normal(500, 200, 1000)
    # Clip values to ensure they're within the valid range
    data['total_spent'] = np.clip(base_spent, 0, 10000).round(2)
    
    return data

@pytest.fixture(scope="session")
def business_rules_config():
    """Load business rules configuration"""
    return {
        'required_columns': ['customer_id', 'name', 'email'],
        'critical_columns': ['customer_id', 'email'],
        'min_row_count': 100,
        'max_null_percentage': {
            'customer_id': 0,
            'name': 1,
            'email': 2
        },
        'value_ranges': {
            'age': [18, 120],
            'total_spent': [0, 50000]  # Wide range to accommodate test data
        },
        'unique_columns': ['customer_id', 'email']
    }
