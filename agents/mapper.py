#pandas sql merging
#handles the actual data joins

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from config.banking_standards import BANKING_STANDARDS, BANKING_RULES, SOURCE_SYSTEMS, DATA_PRODUCT_TEMPLATES
from agents.validator import BankingValidator
import ollama
from models.data_product import DataProduct, Attribute, SourceSystem

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

class DataProductMapper:
    def __init__(self):
        self.model = "tinyllama"
        self.source_systems = self._initialize_source_systems()
        
    def _initialize_source_systems(self) -> List[SourceSystem]:
        """
        Initialize available source systems from standards
        """
        return [
            SourceSystem(**system_config)
            for system_config in SOURCE_SYSTEMS.values()
        ]
    
    async def design_data_product(self, requirements: Dict) -> DataProduct:
        """
        Design data product structure based on requirements
        """
        prompt = f"""
        Design a BankGen 360 data product based on the following requirements:
        
        Requirements: {requirements}
        
        Please provide:
        1. Data product name and description
        2. List of attributes with their types and descriptions
        3. Source system mappings for each attribute
        4. Data quality rules
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {
                    "role": "system",
                    "content": "You are a data product designer specializing in BankGen 360 solutions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ])
            
            # Parse the response and create a DataProduct object
            product_structure = self._parse_product_structure(response['message']['content'])
            return product_structure
            
        except Exception as e:
            raise Exception(f"Error designing data product: {str(e)}")
    
    async def recommend_attributes(self, use_case: str) -> List[Attribute]:
        """
        Recommend attributes based on use case
        """
        prompt = f"""
        Recommend attributes for the following use case:
        
        Use Case: {use_case}
        
        Please provide:
        1. List of recommended attributes
        2. Data types for each attribute
        3. Whether each attribute is PII
        4. Whether each attribute is required
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {
                    "role": "system",
                    "content": "You are a data modeling expert specializing in BankGen 360 solutions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ])
            
            # Parse the response and create Attribute objects
            attributes = self._parse_attributes(response['message']['content'])
            return attributes
            
        except Exception as e:
            raise Exception(f"Error recommending attributes: {str(e)}")
    
    async def map_attributes(self, attributes: List[Attribute], source_systems: List[SourceSystem]) -> Dict:
        """
        Map attributes to source systems
        """
        prompt = f"""
        Map the following attributes to appropriate source systems:
        
        Attributes: {[attr.attribute_name for attr in attributes]}
        Source Systems: {[sys.system_name for sys in source_systems]}
        
        Please provide:
        1. Source system mapping for each attribute
        2. Source field name mapping
        3. Any transformation rules needed
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {
                    "role": "system",
                    "content": "You are a data mapping expert specializing in BankGen 360 solutions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ])
            
            # Parse the response and create mappings
            mappings = self._parse_mappings(response['message']['content'], attributes, source_systems)
            return mappings
            
        except Exception as e:
            raise Exception(f"Error mapping attributes: {str(e)}")
    
    def _parse_product_structure(self, response: str) -> DataProduct:
        """
        Parse the LLM response into a DataProduct object
        """
        # This is a simplified implementation - in production, you'd want more robust parsing
        sections = response.split("\n\n")
        
        # Use template as base
        template = DATA_PRODUCT_TEMPLATES['customer_360']
        
        # Create attributes list
        attributes = []
        for section in sections:
            if "attributes" in section.lower():
                attribute_lines = section.split("\n")
                for line in attribute_lines:
                    if line.strip().startswith("-"):
                        attr_info = line.strip("- ").strip()
                        # Create Attribute object with standards
                        attribute = Attribute(
                            attribute_id=f"ATTR{len(attributes)+1:03d}",
                            attribute_name=attr_info.split(":")[0].strip(),
                            attribute_type=BANKING_STANDARDS['DATA_TYPES'].get(
                                attr_info.split(":")[0].strip().lower(),
                                {'type': 'string', 'format': None, 'description': ''}
                            )['type'],
                            description=attr_info.split(":")[1].strip() if ":" in attr_info else "",
                            is_pii=attr_info.split(":")[0].strip().lower() in BANKING_STANDARDS['VALIDATION_RULES']['required_fields'],
                            is_required=attr_info.split(":")[0].strip().lower() in BANKING_STANDARDS['VALIDATION_RULES']['required_fields'],
                            source_system="core_banking",  # default
                            source_field=attr_info.split(":")[0].strip().lower()
                        )
                        attributes.append(attribute)
        
        # Create DataProduct object
        return DataProduct(
            product_id="DP001",
            product_name=template['name'],
            product_type="customer_360",
            description=template['description'],
            version="1.0.0",
            attributes=attributes,
            source_systems=self.source_systems,
            refresh_frequency=template['refresh_frequency'],
            retention_period=template['retention_period'],
            owner="Data Governance Team"
        )
    
    def _parse_attributes(self, response: str) -> List[Attribute]:
        """
        Parse the LLM response into Attribute objects
        """
        attributes = []
        sections = response.split("\n\n")
        
        for section in sections:
            if "attributes" in section.lower():
                attribute_lines = section.split("\n")
                for line in attribute_lines:
                    if line.strip().startswith("-"):
                        attr_info = line.strip("- ").strip()
                        # Create Attribute object with standards
                        attribute = Attribute(
                            attribute_id=f"ATTR{len(attributes)+1:03d}",
                            attribute_name=attr_info.split(":")[0].strip(),
                            attribute_type=BANKING_STANDARDS['DATA_TYPES'].get(
                                attr_info.split(":")[0].strip().lower(),
                                {'type': 'string', 'format': None, 'description': ''}
                            )['type'],
                            description=attr_info.split(":")[1].strip() if ":" in attr_info else "",
                            is_pii=attr_info.split(":")[0].strip().lower() in BANKING_STANDARDS['VALIDATION_RULES']['required_fields'],
                            is_required=attr_info.split(":")[0].strip().lower() in BANKING_STANDARDS['VALIDATION_RULES']['required_fields'],
                            source_system="core_banking",  # default
                            source_field=attr_info.split(":")[0].strip().lower()
                        )
                        attributes.append(attribute)
        
        return attributes
    
    def _parse_mappings(self, response: str, attributes: List[Attribute], source_systems: List[SourceSystem]) -> Dict:
        """
        Parse the LLM response into attribute mappings
        """
        mappings = {}
        sections = response.split("\n\n")
        
        for section in sections:
            if "mapping" in section.lower():
                mapping_lines = section.split("\n")
                for line in mapping_lines:
                    if line.strip().startswith("-"):
                        mapping_info = line.strip("- ").strip()
                        # Parse mapping information
                        attr_name = mapping_info.split("->")[0].strip()
                        sys_name = mapping_info.split("->")[1].strip() if "->" in mapping_info else "core_banking"
                        
                        # Find the attribute and source system
                        attribute = next((attr for attr in attributes if attr.attribute_name == attr_name), None)
                        system = next((sys for sys in source_systems if sys.system_name == sys_name), None)
                        
                        if attribute and system:
                            mappings[attribute.attribute_id] = {
                                "source_system": system.system_id,
                                "source_field": attribute.attribute_name.lower(),
                                "transformation_rule": None  # Will be populated by validator
                            }
        
        return mappings
    
    async def get_source_systems(self) -> List[SourceSystem]:
        """
        Get available source systems
        """
        return self.source_systems