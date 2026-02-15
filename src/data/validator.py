"""
Data Validation Module for AI Business Assistant
Purpose: Validate and clean business CSV data from multiple sources
Author: [Aristides A. Morcillo]
Date: Day 2
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class DataValidator:
    """
    Validates business data uploads from various POS systems.
    Ensures data quality before ML processing.
    
    Business Context:
    - FreshMart uploads CSV files from Square, Clover, Shopify POS
    - Files have different formats, missing values, duplicates
    - Validator ensures clean data → accurate forecasts
    """
    
    def __init__(self, required_columns: List[str]):
        """
        Initialize validator with required column names.
        
        Args:
            required_columns: List of mandatory column names
            
        Example:
            validator = DataValidator(['date', 'product', 'quantity', 'revenue'])
        """
        self.required_columns = required_columns
        self.validation_report = {}
        self.data = None
    
    def validate_csv(self, file_path: str) -> Tuple[bool, Dict]:
        """
        Validates CSV file structure and content.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Tuple of (is_valid, report_dict)
            
        Business Impact:
            Prevents bad data from breaking ML models
            Saves time by catching errors early
        """
        try:
            # Check if file exists
            if not Path(file_path).exists():
                return False, {'error': f'File not found: {file_path}'}
            
            # Read CSV file
            self.data = pd.read_csv(file_path)
            
            # Validation checks
            is_empty = self.data.empty
            missing_cols = set(self.required_columns) - set(self.data.columns)
            total_rows = len(self.data)
            total_cols = len(self.data.columns)
            
            # Check for missing values per column
            missing_values = self.data.isnull().sum().to_dict()
            
            # Check for duplicate rows
            duplicate_count = self.data.duplicated().sum()
            
            # Check data types (basic validation)
            data_types = self.data.dtypes.to_dict()
            
            # Build validation report
            self.validation_report = {
                'file_path': file_path,
                'total_rows': total_rows,
                'total_columns': total_cols,
                'columns_found': list(self.data.columns),
                'missing_columns': list(missing_cols),
                'missing_values_per_column': missing_values,
                'duplicate_rows': int(duplicate_count),
                'data_types': {k: str(v) for k, v in data_types.items()},
                'is_empty': is_empty
            }
            
            # Determine if validation passed
            is_valid = (
                len(missing_cols) == 0 and  # All required columns present
                not is_empty and             # Data is not empty
                total_rows > 0               # Has at least one row
            )
            
            return is_valid, self.validation_report
            
        except pd.errors.EmptyDataError:
            return False, {'error': 'CSV file is empty'}
        except pd.errors.ParserError as e:
            return False, {'error': f'CSV parsing error: {str(e)}'}
        except Exception as e:
            return False, {'error': f'Unexpected error: {str(e)}'}
    
    def clean_data(self, 
                   remove_duplicates: bool = True,
                   drop_empty_rows: bool = True) -> pd.DataFrame:
        """
        Performs basic data cleaning operations.
        
        Args:
            remove_duplicates: Remove duplicate rows
            drop_empty_rows: Remove rows where ALL values are missing
            
        Returns:
            Cleaned DataFrame
            
        Business Impact:
            FreshMart example: Removes duplicate POS transactions
            Prevents double-counting sales in forecasts
        """
        if self.data is None:
            raise ValueError("No data loaded. Run validate_csv() first.")
        
        cleaned_data = self.data.copy()
        
        # Remove duplicate rows
        if remove_duplicates:
            before_count = len(cleaned_data)
            cleaned_data = cleaned_data.drop_duplicates()
            after_count = len(cleaned_data)
            removed = before_count - after_count
            if removed > 0:
                print(f"✓ Removed {removed} duplicate rows")
        
        # Remove rows where ALL values are missing
        if drop_empty_rows:
            before_count = len(cleaned_data)
            cleaned_data = cleaned_data.dropna(how='all')
            after_count = len(cleaned_data)
            removed = before_count - after_count
            if removed > 0:
                print(f"✓ Removed {removed} completely empty rows")
        
        return cleaned_data
    
    def get_summary_statistics(self) -> Dict:
        """
        Generate summary statistics for numerical columns.
        
        Returns:
            Dictionary with statistics
            
        Business Use:
            Quick sanity check on data ranges
            Detect outliers (e.g., negative sales)
        """
        if self.data is None:
            raise ValueError("No data loaded. Run validate_csv() first.")
        
        # Get only numerical columns
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        
        summary = {}
        for col in numerical_cols:
            summary[col] = {
                'mean': float(self.data[col].mean()),
                'min': float(self.data[col].min()),
                'max': float(self.data[col].max()),
                'std': float(self.data[col].std())
            }
        
        return summary


# Business-to-Tech Connection:
# This validator is the first line of defense against bad data.
# In FreshMart's case:
# - Prevents the $1,140 strawberry waste disaster
# - Catches format inconsistencies from 3 different POS systems
# - Ensures ML model trains on quality data → 87% accuracy