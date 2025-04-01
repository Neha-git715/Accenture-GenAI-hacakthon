#pandas sql merging
#handles the actual data joins

import pandas as pd
from typing import Dict, List
from config.standards import BANKING_RULES

class DataProductMapper:
    """Complete data product mapper with banking-specific rules"""

    def __init__(self):
        self.sources = {
            'customers': 'data/customers.csv',
            'accounts': 'data/accounts.csv',
            'transactions': 'data/transactions.csv',
            'loans': 'data/loans.csv'
        }

    def identify_sources(self, requirements: str) -> Dict:
        """Smart source identification with keyword matching"""
        required_sources = {}
        
        requirements_lower = requirements.lower()
        
        if any(x in requirements_lower for x in ['customer', 'tier', 'name']):
            required_sources['customers'] = self.sources['customers']
            
        if any(x in requirements_lower for x in ['balance', 'account']):
            required_sources['accounts'] = self.sources['accounts']
            
        if any(x in requirements_lower for x in ['transaction', 'payment']):
            required_sources['transactions'] = self.sources['transactions']
            
        if any(x in requirements_lower for x in ['loan', 'mortgage']):
            required_sources['loans'] = self.sources['loans']
            
        return required_sources

    def create_mapping(self, sources: Dict, target_schema: Dict) -> List[Dict]:
        """Creates detailed field mappings"""
        mappings = []
        
        for target_field, config in target_schema.items():
            mapping = {
                "target": target_field,
                "description": config.get("description", ""),
                "sources": [],
                "transformations": [],
                "business_rules": []
            }
            
            # Customer ID mapping
            if target_field == "Customer_ID":
                mapping['sources'] = [{
                    "table": "customers",
                    "field": "Customer_ID",
                    "type": "direct"
                }]
                mapping['transformations'] = ["direct_copy"]
                
            # Balance calculations
            elif target_field == "Total_Balance":
                mapping['sources'] = [{
                    "table": "accounts",
                    "field": "Balance",
                    "type": "numeric"
                }]
                mapping['transformations'] = ["sum"]
                mapping['business_rules'] = ["ignore_negative_balances"]
                
            mappings.append(mapping)
            
        return mappings

    def execute_mapping(self, mappings: List[Dict]) -> pd.DataFrame:
        """Executes all mappings to create final data product"""
        # Load all source data
        loaded_data = {}
        for mapping in mappings:
            for source in mapping['sources']:
                if source['table'] not in loaded_data:
                    loaded_data[source['table']] = pd.read_csv(self.sources[source['table']])
        
        # Apply transformations
        result = pd.DataFrame()
        
        for mapping in mappings:
            target = mapping['target']
            
            if mapping['transformations'] == ["direct_copy"]:
                src = mapping['sources'][0]
                result[target] = loaded_data[src['table']][src['field']]
                
            elif "sum" in mapping['transformations']:
                sum_values = pd.Series(dtype='float64')
                for src in mapping['sources']:
                    if src['table'] in loaded_data:
                        if sum_values.empty:
                            sum_values = loaded_data[src['table']][src['field']]
                        else:
                            sum_values += loaded_data[src['table']][src['field']]
                result[target] = sum_values
                
        return result

    @staticmethod
    def safe_display(df: pd.DataFrame) -> pd.DataFrame:
        """Anonymizes data for display"""
        if 'Name' in df.columns:
            df['Name'] = 'CONFIDENTIAL'
        if 'Email' in df.columns:
            df['Email'] = '***@bank.com'
        return df