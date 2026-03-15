"""
Unit tests for DataValidator
"""

import pandas as pd
import os
from pathlib import Path
from src.data.validator import DataValidator


def test_validator_with_valid_data():
    """Test validator accepts clean, valid CSV data"""
    
    # Setup: Create sample data
    sample_data = pd.DataFrame({
        'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'product': ['Milk', 'Strawberries', 'Bread'],
        'quantity': [45, 12, 25],
        'revenue': [179.55, 71.88, 62.50],
        'store': ['Store 1', 'Store 1', 'Store 1']
    })
    
    # Save to temp file
    test_file = 'test_valid_data.csv'
    sample_data.to_csv(test_file, index=False)
    
    try:
        # Test validation
        validator = DataValidator(
            required_columns=['date', 'product', 'quantity', 'revenue', 'store']
        )
        is_valid, report = validator.validate_csv(test_file)
        
        # Assertions
        assert is_valid == True, "Validation should pass for valid data"
        assert report['total_rows'] == 3, "Should have 3 rows"
        assert report['total_columns'] == 5, "Should have 5 columns"
        assert len(report['missing_columns']) == 0, "No columns should be missing"
        
        print("✅ test_validator_with_valid_data PASSED")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)


def test_validator_detects_missing_columns():
    """Test validator catches missing required columns"""
    
    # Setup: Data missing 'revenue' column
    sample_data = pd.DataFrame({
        'date': ['2024-01-01', '2024-01-02'],
        'product': ['Milk', 'Bread'],
        'quantity': [45, 25]
    })
    
    test_file = 'test_missing_cols.csv'
    sample_data.to_csv(test_file, index=False)
    
    try:
        validator = DataValidator(
            required_columns=['date', 'product', 'quantity', 'revenue']
        )
        is_valid, report = validator.validate_csv(test_file)
        
        # Assertions
        assert is_valid == False, "Validation should fail"
        assert 'revenue' in report['missing_columns'], "Should detect missing 'revenue' column"
        
        print("✅ test_validator_detects_missing_columns PASSED")
        
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_clean_data_removes_duplicates():
    """Test data cleaning removes duplicate rows"""
    
    # Setup: Data with duplicates
    sample_data = pd.DataFrame({
        'date': ['2024-01-01', '2024-01-01', '2024-01-02'],  # Duplicate row
        'product': ['Milk', 'Milk', 'Bread'],
        'quantity': [45, 45, 25],
        'revenue': [179.55, 179.55, 62.50]
    })
    
    test_file = 'test_duplicates.csv'
    sample_data.to_csv(test_file, index=False)
    
    try:
        validator = DataValidator(required_columns=['date', 'product', 'quantity', 'revenue'])
        validator.validate_csv(test_file)
        
        # Clean data
        cleaned = validator.clean_data(remove_duplicates=True)
        
        # Assertions
        assert len(cleaned) == 2, "Should have 2 rows after removing duplicate"
        assert validator.data.shape[0] == 3, "Original data should still have 3 rows"
        
        print("✅ test_clean_data_removes_duplicates PASSED")
        
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)


def test_validator_with_freshmart_sample():
    """Test with actual FreshMart sample data"""
    
    sample_file = 'data/samples/freshmart_store1.csv'
    
    # Check if sample file exists
    if not Path(sample_file).exists():
        print(f"⚠️  Sample file not found: {sample_file}")
        print("   Create it following Day 2 instructions")
        return
    
    validator = DataValidator(
        required_columns=['date', 'product', 'quantity', 'revenue', 'store']
    )
    
    is_valid, report = validator.validate_csv(sample_file)
    
    # Assertions
    assert is_valid == True, "FreshMart sample should be valid"
    assert report['total_rows'] == 10, "Sample has 10 rows"
    
    # Get summary statistics
    stats = validator.get_summary_statistics()
    assert 'quantity' in stats, "Should have quantity statistics"
    assert 'revenue' in stats, "Should have revenue statistics"
    
    print("✅ test_validator_with_freshmart_sample PASSED")
    print(f"   Validated {report['total_rows']} rows from FreshMart")


if __name__ == '__main__':
    """Run all tests"""
    print("🧪 Running Data Validator Tests...")
    print("=" * 50)
    
    test_validator_with_valid_data()
    test_validator_detects_missing_columns()
    test_clean_data_removes_duplicates()
    test_validator_with_freshmart_sample()
    
    print("=" * 50)
    print("✅ All tests passed!")