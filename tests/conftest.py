import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import json

# Fix imports for GitHub Actions
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

@pytest.fixture(scope="session")
def test_config():
    """Load test configuration"""
    config_path = Path(__file__).parent / "configs" / "test_config.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {"validation_thresholds": {"data_quality_minimum": 0.95}}

@pytest.fixture(scope="session")
def sample_customer_data():
    """Generate sample customer data for testing"""
    np.random.seed(42)
    
    data = pd.DataFrame({
        'customer_id': range(1, 1001),
        'name': [f'Customer {i}' for i in range(1, 1001)],
        'email': [f'customer{i}@example.com' for i in range(1, 1001)],
        'created_date': pd.date_range('2023-01-01', periods=1000, freq='D'),
        'country': np.random.choice(['US', 'CA', 'UK', 'DE', 'FR'], 1000),
        'age': np.random.randint(18, 80, 1000),
        'status': np.random.choice(['ACTIVE', 'INACTIVE', 'PENDING'], 1000)
    })
    
    # Ensure values are within range
    data['total_spent'] = np.random.uniform(10, 8000, 1000).round(2)
    return data

@pytest.fixture(scope="session") 
def business_rules_config():
    """Business rules configuration"""
    return {
        'required_columns': ['customer_id', 'name', 'email'],
        'critical_columns': ['customer_id', 'email'],
        'min_row_count': 100,
        'max_null_percentage': {'customer_id': 0, 'name': 1, 'email': 2},
        'value_ranges': {'age': [18, 120], 'total_spent': [0, 50000]},
        'unique_columns': ['customer_id', 'email']
    }