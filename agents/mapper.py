#pandas sql merging
#handles the actual data joins

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from config.standards import BANKING_RULES
from agents.validator import BankingValidator

class DataMapper:
    """
    Handles secure banking data operations with:
    - Schema-aware merging
    - PII anonymization
    - AML/compliance checks
    - SQL injection prevention
    """

    @staticmethod
    def load_data(file_path: str) -> pd.DataFrame:
        """
        Loads banking CSV with validation
        Args:
            file_path: Path to CSV (e.g., 'data/loans.csv')
        Returns:
            pd.DataFrame: Validated banking data
        Raises:
            ValueError: If required columns missing
        """
        # Validate file type
        if not file_path.endswith('.csv'):
            raise ValueError("Only CSV files supported")

        df = pd.read_csv(file_path)
        
        # Check required columns
        required_columns = {
            'customers.csv': ['Customer_ID', 'Tier'],
            'loans.csv': ['Customer_ID', 'Type', 'Amount'],
            'transactions.csv': ['Customer_ID', 'Amount', 'Date'],
            'accounts.csv': ['Customer_ID', 'Type', 'Balance']
        }
        
        filename = file_path.split('/')[-1]
        if filename in required_columns:
            missing = [col for col in required_columns[filename] 
                      if col not in df.columns]
            if missing:
                raise ValueError(f"Missing required columns in {filename}: {missing}")
        
        # Convert date fields
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            
        return df

    @staticmethod
    def merge_tables(left_path: str, right_path: str, 
                    on: str = "Customer_ID") -> pd.DataFrame:
        """
        Banking-safe table joining with compliance checks
        Args:
            left_path: Path to first CSV
            right_path: Path to second CSV
            on: Join column (default: Customer_ID)
        Returns:
            pd.DataFrame: Merged data with PII removed
        """
        # Validate join column
        if on not in BANKING_STANDARDS['approved_joins']:
            raise ValueError(f"Joining on {on} violates banking standards")
        
        left = DataMapper.load_data(left_path)
        right = DataMapper.load_data(right_path)
        
        # Inner join for data integrity
        merged = pd.merge(
            left, 
            right, 
            on=on,
            how='inner',
            validate='one_to_many'  # Ensures no duplicate joins
        )
        
        # Apply banking rules
        if 'Amount' in merged.columns:
            merged = merged[
                merged['Amount'] >= BANKING_STANDARDS['amount_checks']['min_transaction']
            ]
            
        if 'Balance' in merged.columns:
            merged['Balance'] = merged['Balance'].apply(
                lambda x: max(float(x), 0)  # No negative balances
            )
        
        # Anonymize before returning
        return DataMapper.anonymize(merged).drop_duplicates()

    @staticmethod
    def anonymize(df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes/masks PII from banking data
        Args:
            df: Input DataFrame
        Returns:
            pd.DataFrame: Anonymized data
        """
        # Mask direct identifiers
        if 'Name' in df.columns:
            df['Name'] = 'CONFIDENTIAL'
        if 'Email' in df.columns:
            df['Email'] = df['Email'].apply(
                lambda x: x.split('@')[0][:2] + '****@bank.com'
            )
        
        # Remove unused PII
        pii_cols = [col for col in df.columns 
                   if any(pii in col.lower() 
                         for pii in BANKING_STANDARDS['pii_fields'])]
        return df.drop(columns=pii_cols, errors='ignore')

    @staticmethod
    def validate_sql(sql: str) -> bool:
        """
        Checks for dangerous SQL operations
        Args:
            sql: SQL query string
        Returns:
            bool: True if query is safe
        """
        banned = BANKING_STANDARDS['SQL_BLACKLIST'] + [';--', 'xp_', 'exec']
        return not any(cmd in sql.upper() for cmd in banned)

    @staticmethod
    def get_sample_data(query: str = None) -> List[Dict]:
        """
        Generates compliant sample data for API responses
        Args:
            query: Optional natural language query
        Returns:
            List[Dict]: Sample records (anonymized)
        """
        # Default join for demo purposes
        df = DataMapper.merge_tables(
            "data/customers.csv", 
            "data/loans.csv"
        )
        
        # Filter based on query if provided
        if query and "mortgage" in query.lower():
            df = df[df['Type'] == 'Mortgage']
        elif query and "gold" in query.lower():
            df = df[df['Tier'] == 'Gold']
        
        return BankingValidator().filter_risks(df).head(3).to_dict(orient='records')
    

# Example usage
if __name__ == "__main__":
    try:
        # Test merge
        sample = DataMapper.merge_tables(
            "data/customers.csv",
            "data/transactions.csv"
        )
        print("Sample merged data:\n", sample.head(2))
        
        # Test validation
        print("SQL validation:", 
              DataMapper.validate_sql("SELECT * FROM customers"))
              
    except Exception as e:
        print(f"Banking data error: {str(e)}")