"""
Data Cleaning Module for AI Business Assistant
Purpose: Clean and standardize data from multiple POS systems
Author: Aristides A. Morcillo.   
Date: 2026-02-22
"""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime


class DataCleaner:
    """
    Cleans and standardizes business data from various sources.
    
    Handles:
    - Date format inconsistencies
    - Product name variations
    - Missing values
    - Column name standardization
    
    Supports both Pandas and Polars (future-ready)
    """
    
    def __init__(self, engine: str = "pandas"):
        """
        Initialize data cleaner.
        
        Args:
            engine: "pandas" or "polars" (default: pandas)
        """
        self.engine = engine
        self.cleaning_report = {}
    
    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names across different POS systems.
        
        Business Context:
        - Square uses: date, product, quantity, revenue
        - Clover uses: Date, Item, Qty, Total
        - Shopify uses: transaction_date, product_name, units_sold, sale_amount
        """
        column_mapping = {
            # Date variations
            'Date': 'date',
            'transaction_date': 'date',
            'sale_date': 'date',
            'order_date': 'date',
            
            # Product variations
            'Item': 'product',
            'product_name': 'product',
            'item_name': 'product',
            'Product': 'product',
            
            # Quantity variations
            'Qty': 'quantity',
            'units_sold': 'quantity',
            'Quantity': 'quantity',
            'qty': 'quantity',
            
            # Revenue variations
            'Total': 'revenue',
            'sale_amount': 'revenue',
            'total_amount': 'revenue',
            'Revenue': 'revenue',
            'sales': 'revenue',
            
            # Store variations
            'Store': 'store',
            'store_id': 'store',
            'location': 'store'
        }
        
        df_renamed = df.rename(columns=column_mapping)
        df_renamed.columns = df_renamed.columns.str.lower()
        return df_renamed
    
    def clean_date_column(self, df: pd.DataFrame, date_column: str = 'date') -> pd.DataFrame:
        """Parse and standardize date formats."""
        if date_column not in df.columns:
            return df
        
        df_cleaned = df.copy()
        
        try:
            df_cleaned[date_column] = pd.to_datetime(
                df_cleaned[date_column],
                errors='coerce'
            )
            df_cleaned[date_column] = df_cleaned[date_column].dt.strftime('%Y-%m-%d')
            
            failed_dates = df_cleaned[date_column].isna().sum()
            if failed_dates > 0:
                print(f"⚠️  Warning: {failed_dates} dates could not be parsed")
        except Exception as e:
            print(f"❌ Error parsing dates: {str(e)}")
        
        return df_cleaned
    
    def standardize_product_names(self, df: pd.DataFrame, product_column: str = 'product') -> pd.DataFrame:
        """Standardize product names for consistency."""
        if product_column not in df.columns:
            return df
        
        df_cleaned = df.copy()
        
        # Convert to lowercase
        df_cleaned[product_column] = df_cleaned[product_column].str.lower()
        df_cleaned[product_column] = df_cleaned[product_column].str.strip()
        df_cleaned[product_column] = df_cleaned[product_column].str.replace(r'\s+', ' ', regex=True)
        
        # Business-specific mappings
        product_mapping = {
            'milk 1gal': 'milk',
            'milk - 1 gallon': 'milk',
            'whole milk': 'milk',
            '1 gallon milk': 'milk',
            'organic strawberries': 'strawberries',
            'strawberry': 'strawberries'
        }
        
        df_cleaned[product_column] = df_cleaned[product_column].replace(product_mapping)
        return df_cleaned
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
        """Handle missing values based on strategy."""
        df_cleaned = df.copy()
        
        if strategy == "drop":
            before_count = len(df_cleaned)
            df_cleaned = df_cleaned.dropna()
            after_count = len(df_cleaned)
            removed = before_count - after_count
            if removed > 0:
                print(f"✓ Removed {removed} rows with missing values")
        
        elif strategy == "fill_zero":
            numerical_cols = df_cleaned.select_dtypes(include=['int64', 'float64']).columns
            df_cleaned[numerical_cols] = df_cleaned[numerical_cols].fillna(0)
            print(f"✓ Filled missing numerical values with 0")
        
        elif strategy == "fill_mean":
            numerical_cols = df_cleaned.select_dtypes(include=['int64', 'float64']).columns
            for col in numerical_cols:
                mean_val = df_cleaned[col].mean()
                df_cleaned[col] = df_cleaned[col].fillna(mean_val)
            print(f"✓ Filled missing numerical values with column means")
        
        elif strategy == "drop_critical":
            critical_cols = ['date', 'product', 'quantity']
            existing_critical = [col for col in critical_cols if col in df_cleaned.columns]
            before_count = len(df_cleaned)
            df_cleaned = df_cleaned.dropna(subset=existing_critical)
            after_count = len(df_cleaned)
            removed = before_count - after_count
            if removed > 0:
                print(f"✓ Removed {removed} rows with missing critical values")
        
        return df_cleaned
    
    def clean_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Complete cleaning pipeline for FreshMart data.
        
        Steps:
        1. Standardize column names
        2. Clean dates
        3. Standardize product names
        4. Handle missing values
        5. Remove duplicates
        """
        print("\n🧹 Starting data cleaning pipeline...")
        print(f"   Input: {len(df)} rows, {len(df.columns)} columns")
        
        # Step 1: Standardize columns
        df_clean = self.standardize_column_names(df)
        print(f"✓ Step 1: Standardized column names")
        
        # Step 2: Clean dates
        if 'date' in df_clean.columns:
            df_clean = self.clean_date_column(df_clean)
            print(f"✓ Step 2: Cleaned date formats")
        
        # Step 3: Standardize product names
        if 'product' in df_clean.columns:
            df_clean = self.standardize_product_names(df_clean)
            print(f"✓ Step 3: Standardized product names")
        
        # Step 4: Handle missing values
        df_clean = self.handle_missing_values(df_clean, strategy="drop_critical")
        print(f"✓ Step 4: Handled missing values")
        
        # Step 5: Remove duplicates
        before_count = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        after_count = len(df_clean)
        removed = before_count - after_count
        if removed > 0:
            print(f"✓ Step 5: Removed {removed} duplicate rows")
        else:
            print(f"✓ Step 5: No duplicates found")
        
        print(f"\n✅ Cleaning complete!")
        print(f"   Output: {len(df_clean)} rows, {len(df_clean.columns)} columns")
        
        return df_clean