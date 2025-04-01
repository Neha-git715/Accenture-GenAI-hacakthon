#rule based checks
#Ensures no PII leaks/compliance

import pandas as pd
from config.banking_standards import BANKING_STANDARDS, BANKING_RULES
from typing import Dict, List, Optional
import ollama
from models.data_product import DataProduct, Attribute, DataQualityRule

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

class DataProductValidator:
    def __init__(self):
        self.model = "llama2"
        self.compliance_rules = BANKING_RULES['COMPLIANCE_RULES']
        self.data_quality_rules = BANKING_RULES['DATA_QUALITY_RULES']
        
    async def validate_data_product(self, data_product: DataProduct) -> Dict:
        """
        Validate data product design and ensure compliance
        """
        validation_results = {
            "is_valid": True,
            "issues": [],
            "recommendations": []
        }
        
        # Validate attributes
        for attribute in data_product.attributes:
            # Check PII compliance
            if attribute.is_pii:
                pii_validation = self._validate_pii_compliance(attribute)
                if not pii_validation["is_valid"]:
                    validation_results["is_valid"] = False
                    validation_results["issues"].extend(pii_validation["issues"])
                    validation_results["recommendations"].extend(pii_validation["recommendations"])
            
            # Check data quality rules
            quality_validation = self._validate_data_quality(attribute)
            if not quality_validation["is_valid"]:
                validation_results["is_valid"] = False
                validation_results["issues"].extend(quality_validation["issues"])
                validation_results["recommendations"].extend(quality_validation["recommendations"])
        
        # Validate source system mappings
        mapping_validation = self._validate_source_mappings(data_product)
        if not mapping_validation["is_valid"]:
            validation_results["is_valid"] = False
            validation_results["issues"].extend(mapping_validation["issues"])
            validation_results["recommendations"].extend(mapping_validation["recommendations"])
        
        return validation_results
    
    def _validate_pii_compliance(self, attribute: Attribute) -> Dict:
        """
        Validate PII compliance for an attribute
        """
        validation = {
            "is_valid": True,
            "issues": [],
            "recommendations": []
        }
        
        # Check if PII data has required security measures
        if attribute.is_pii:
            # Check GDPR compliance
            if self.compliance_rules['gdpr']['consent_required']:
                validation["issues"].append(f"PII attribute {attribute.attribute_name} requires GDPR consent")
                validation["recommendations"].append("Add consent tracking for PII data")
                validation["is_valid"] = False
            
            # Check PCI DSS compliance for payment data
            if attribute.attribute_name.lower() in ['credit_card', 'bank_account']:
                if self.compliance_rules['pci_dss']['card_data_encryption']:
                    validation["issues"].append(f"Payment data {attribute.attribute_name} requires encryption")
                    validation["recommendations"].append("Implement encryption for payment data")
                    validation["is_valid"] = False
        
        return validation
    
    def _validate_data_quality(self, attribute: Attribute) -> Dict:
        """
        Validate data quality rules for an attribute
        """
        validation = {
            "is_valid": True,
            "issues": [],
            "recommendations": []
        }
        
        # Check required fields
        if attribute.is_required:
            if not any(rule.rule_name == "not_null" for rule in attribute.data_quality_rules):
                validation["issues"].append(f"Required attribute {attribute.attribute_name} missing not_null rule")
                validation["recommendations"].append("Add not_null rule for required field")
                validation["is_valid"] = False
        
        # Check data type specific rules
        if attribute.attribute_type == "string":
            # Check format rules
            format_rules = BANKING_STANDARDS['VALIDATION_RULES']['format_rules']
            if attribute.attribute_name.lower() in format_rules:
                if not any(rule.rule_name == "format_check" for rule in attribute.data_quality_rules):
                    validation["issues"].append(f"String attribute {attribute.attribute_name} missing format check")
                    validation["recommendations"].append(f"Add format check rule for {attribute.attribute_name}")
                    validation["is_valid"] = False
        
        # Check specific data quality rules
        if attribute.attribute_name.lower() in self.data_quality_rules:
            rules = self.data_quality_rules[attribute.attribute_name.lower()]
            for rule_name, rule_value in rules.items():
                if rule_value and not any(rule.rule_name == rule_name for rule in attribute.data_quality_rules):
                    validation["issues"].append(f"Attribute {attribute.attribute_name} missing {rule_name} rule")
                    validation["recommendations"].append(f"Add {rule_name} rule for {attribute.attribute_name}")
                    validation["is_valid"] = False
        
        return validation
    
    def _validate_source_mappings(self, data_product: DataProduct) -> Dict:
        """
        Validate source system mappings
        """
        validation = {
            "is_valid": True,
            "issues": [],
            "recommendations": []
        }
        
        # Check if all attributes have source mappings
        for attribute in data_product.attributes:
            if not attribute.source_system:
                validation["issues"].append(f"Attribute {attribute.attribute_name} missing source system mapping")
                validation["recommendations"].append("Map attribute to appropriate source system")
                validation["is_valid"] = False
        
        return validation
    
    async def recommend_data_quality_rules(self, attribute: Attribute) -> List[DataQualityRule]:
        """
        Recommend data quality rules for an attribute
        """
        prompt = f"""
        Recommend data quality rules for the following attribute:
        
        Attribute: {attribute.attribute_name}
        Type: {attribute.attribute_type}
        Is PII: {attribute.is_pii}
        Is Required: {attribute.is_required}
        
        Please provide:
        1. List of recommended data quality rules
        2. Rule expressions
        3. Severity levels
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {
                    "role": "system",
                    "content": "You are a data quality expert specializing in Customer 360 solutions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ])
            
            # Parse the response and create DataQualityRule objects
            rules = self._parse_quality_rules(response['message']['content'])
            return rules
            
        except Exception as e:
            raise Exception(f"Error recommending data quality rules: {str(e)}")
    
    def _parse_quality_rules(self, response: str) -> List[DataQualityRule]:
        """
        Parse the LLM response into DataQualityRule objects
        """
        rules = []
        sections = response.split("\n\n")
        
        for section in sections:
            if "rules" in section.lower():
                rule_lines = section.split("\n")
                for line in rule_lines:
                    if line.strip().startswith("-"):
                        rule_info = line.strip("- ").strip()
                        # Create DataQualityRule object
                        rule = DataQualityRule(
                            rule_id=f"RULE{len(rules)+1:03d}",
                            rule_name=rule_info.split(":")[0].strip(),
                            rule_type="validation",
                            rule_expression=rule_info.split(":")[1].strip() if ":" in rule_info else "",
                            severity="error" if "error" in rule_info.lower() else "warning",
                            description=rule_info.split(":")[2].strip() if len(rule_info.split(":")) > 2 else ""
                        )
                        rules.append(rule)
        
        return rules