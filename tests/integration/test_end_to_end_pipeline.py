"""End-to-end pipeline integration tests"""
import pytest
import pandas as pd
from src.validators.business_rules_validator import BusinessRulesValidator

@pytest.mark.integration
@pytest.mark.pipeline
class TestEndToEndPipeline:
    """Test complete pipeline end-to-end"""
    
    def test_customer_data_pipeline(self, sample_customer_data, business_rules_config):
        """Test complete customer data processing pipeline"""
        
        # Step 1: Extract (simulated)
        raw_data = sample_customer_data.copy()
        assert len(raw_data) > 0, "Should have extracted data"
        
        # Step 2: Transform (simulated)
        # Add some calculated fields that ETL might create
        transformed_data = raw_data.copy()
        transformed_data['customer_segment'] = pd.cut(
            transformed_data['total_spent'],
            bins=[0, 100, 500, 1000, float('inf')],
            labels=['Bronze', 'Silver', 'Gold', 'Platinum']
        )
        transformed_data['age_group'] = pd.cut(
            transformed_data['age'],
            bins=[0, 25, 45, 65, float('inf')],
            labels=['Young', 'Adult', 'Middle-aged', 'Senior']
        )
        
        # Step 3: Validate (this is our test)
        validator = BusinessRulesValidator(business_rules_config)
        
        completeness_results = validator.validate_completeness(transformed_data)
        quality_results = validator.validate_data_quality(transformed_data)
        
        # Assert all validations pass
        for check, passed in completeness_results.items():
            assert passed, f"Completeness check failed: {check}"
            
        for check, passed in quality_results.items():
            assert passed, f"Quality check failed: {check}"
        
        # Step 4: Load validation (simulated)
        # In real scenario, this would validate data was loaded correctly
        assert 'customer_segment' in transformed_data.columns, "Derived field should be present"
        assert 'age_group' in transformed_data.columns, "Derived field should be present"
        
        print(f"✅ Pipeline processed {len(transformed_data)} records successfully")
