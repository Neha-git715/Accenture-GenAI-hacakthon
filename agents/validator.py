#rule based checks
#Ensures no PII leaks/compliance

import pandas as pd
from typing import Dict, List
from config.standards import BANKING_RULES

class BankingValidator:
    """Enhanced validator with complete banking compliance checks"""

    @staticmethod
    def generate_data_product_schema(source_tables: List[str]) -> Dict:
        """Generates schema based on available sources"""
        base_schema = {
            "Customer_ID": {
                "type": "string",
                "source": "all",
                "description": "Primary customer identifier",
                "required": True
            }
        }

        # Dynamic schema additions
        if 'accounts' in source_tables:
            base_schema["Total_Balance"] = {
                "type": "float",
                "sources": ["accounts"],
                "calculation": "sum(balance)",
                "description": "Sum of all account balances"
            }

        if 'transactions' in source_tables:
            base_schema["Transaction_Count"] = {
                "type": "integer",
                "sources": ["transactions"],
                "calculation": "count",
                "description": "Number of transactions"
            }

        return base_schema

    @staticmethod
    def validate_data_product(df: pd.DataFrame) -> Dict:
        """Comprehensive data product validation"""
        results = {
            "compliance": {
                "missing_fields": [],
                "pii_exposure": False,
                "data_quality": []
            },
            "business_rules": []
        }

        # Check required fields
        required = BANKING_RULES['required_fields']
        results["compliance"]["missing_fields"] = [
            field for field in required if field not in df.columns
        ]

        # PII check
        pii_fields = BANKING_RULES['pii_fields'] + ['Name', 'Email', 'Phone']
        results["compliance"]["pii_exposure"] = any(
            field in df.columns for field in pii_fields
        )

        # Data quality checks
        if 'Amount' in df.columns:
            if df['Amount'].min() < 0:
                results["compliance"]["data_quality"].append("Negative amounts found")
        
        return results