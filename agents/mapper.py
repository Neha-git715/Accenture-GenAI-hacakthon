#pandas sql merging
#handles the actual data joins

import pandas as pd
from config.standards import BANKING_STANDARDS

class DataMapper:
    @staticmethod
    def merge_data(loans_path: str, transactions_path: str) -> pd.DataFrame:
        """Merges banking data with validation"""
        loans = pd.read_csv(loans_path)
        transactions = pd.read_csv(transactions_path)
        
        # Check required fields
        for field in BANKING_STANDARDS["required_fields"]:
            if field not in loans.columns or field not in transactions.columns:
                raise ValueError(f"Missing required field: {field}")
        
        return pd.merge(
            loans, 
            transactions, 
            on="Customer_ID",
            how="inner"
        ).drop_duplicates()