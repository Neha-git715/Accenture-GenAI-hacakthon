from typing import Dict, List, Any
import re
from datetime import datetime

class DataValidator:
    def __init__(self):
        self.pii_patterns = {
            "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            "phone": r'^\+?1?\d{9,15}$',
            "ssn": r'^\d{3}-?\d{2}-?\d{4}$',
            "credit_card": r'^\d{4}-?\d{4}-?\d{4}-?\d{4}$'
        }
        
    def validate_data_structure(self, structure: Dict) -> Dict[str, Any]:
        """Validate data product structure"""
        issues = []
        
        # Check for required fields
        required_fields = ["entities", "source_mappings", "refresh_frequency"]
        for field in required_fields:
            if field not in structure:
                issues.append({
                    "severity": "high",
                    "message": f"Missing required field: {field}"
                })
        
        # Validate entities
        if "entities" in structure:
            for entity in structure["entities"]:
                if "name" not in entity:
                    issues.append({
                        "severity": "high",
                        "message": f"Entity missing name field"
                    })
                if "attributes" not in entity:
                    issues.append({
                        "severity": "high",
                        "message": f"Entity {entity.get('name', 'Unknown')} missing attributes"
                    })
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    def validate_mappings(self, mappings: Dict) -> Dict[str, Any]:
        """Validate source to target mappings"""
        issues = []
        
        for source, mapping_list in mappings.items():
            for mapping in mapping_list:
                if "source_attribute" not in mapping:
                    issues.append({
                        "severity": "high",
                        "message": f"Mapping missing source_attribute in {source}"
                    })
                if "target_attribute" not in mapping:
                    issues.append({
                        "severity": "high",
                        "message": f"Mapping missing target_attribute in {source}"
                    })
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    def validate_pii_handling(self, data_product: Dict) -> Dict[str, Any]:
        """Validate PII data handling"""
        issues = []
        
        def check_pii_protection(entity: Dict):
            for attr in entity.get("attributes", []):
                if attr.get("is_pii", False):
                    if not attr.get("encryption_required", False):
                        issues.append({
                            "severity": "high",
                            "message": f"PII attribute {attr['name']} in {entity['name']} requires encryption"
                        })
                    if not attr.get("access_control", None):
                        issues.append({
                            "severity": "medium",
                            "message": f"PII attribute {attr['name']} in {entity['name']} missing access control"
                        })
        
        for entity in data_product.get("structure", {}).get("entities", []):
            check_pii_protection(entity)
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    def validate_data_quality(self, sample_data: Dict) -> Dict[str, Any]:
        """Validate data quality of sample data"""
        issues = []
        metrics = {
            "completeness": 0,
            "accuracy": 0,
            "consistency": 0
        }
        
        total_fields = 0
        complete_fields = 0
        
        def check_field_quality(value: Any, field_type: str):
            nonlocal total_fields, complete_fields
            
            total_fields += 1
            if value is not None and value != "":
                complete_fields += 1
                
                # Type validation
                if field_type == "date":
                    try:
                        datetime.strptime(str(value), "%Y-%m-%d")
                    except ValueError:
                        issues.append({
                            "severity": "medium",
                            "message": f"Invalid date format: {value}"
                        })
                elif field_type == "email":
                    if not re.match(self.pii_patterns["email"], str(value)):
                        issues.append({
                            "severity": "medium",
                            "message": f"Invalid email format: {value}"
                        })
        
        # Process sample data
        for entity, records in sample_data.items():
            for record in records:
                for field, value in record.items():
                    check_field_quality(value, field)
        
        # Calculate metrics
        metrics["completeness"] = (complete_fields / total_fields) * 100 if total_fields > 0 else 0
        metrics["accuracy"] = 100 - (len(issues) / total_fields * 100) if total_fields > 0 else 0
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "metrics": metrics
        } 