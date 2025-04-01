#rule based checks
#Ensures no PII leaks/compliance

import pandas as pd
from config.standards import BANKING_RULES
from typing import Dict, List

class BankingValidator:
    """Handles banking-specific data validation"""

    @staticmethod
    def detect_aml_risks(df: pd.DataFrame) -> Dict[str, List]:
        """
        Flags transactions requiring AML review
        Returns: {'high_risk': [tx_ids], 'suspicious': [tx_ids]}
        """
        risks = {
            'high_risk': [],
            'suspicious': []
        }
        
        if 'Amount' in df.columns:
            # Large transactions
            large_tx = df[df['Amount'] > BANKING_RULES['AML_THRESHOLD']]
            risks['high_risk'].extend(large_tx.get('Transaction_ID', []))
            
            # Rapid fire transactions
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')
                time_diff = df['Date'].diff().dt.total_seconds()
                rapid = df[(time_diff < 3600) & (df['Amount'] > 5000)]
                risks['suspicious'].extend(rapid.get('Transaction_ID', []))
        
        return risks

    @staticmethod
    def validate_pii(df: pd.DataFrame) -> bool:
        """Check for accidental PII exposure"""
        pii_fields = BANKING_RULES['pii_fields'] + ['Name', 'Email']
        return not any(col.lower() in df.columns for col in pii_fields)

    @staticmethod
    def check_sql_injection(sql: str) -> bool:
        """Prevent malicious SQL"""
        banned = BANKING_RULES['SQL_BLACKLIST'] + [';--', 'xp_', 'exec']
        return not any(cmd in sql.upper() for cmd in banned)