#PII /field requirements

BANKING_RULES = {
    # Data Product Requirements
    "required_fields": ["Customer_ID", "Tier", "Risk_Score"],
    "pii_fields": ["SSN", "Account_Number", "Email"],
    
    # Business Rules
    "tiers": ["platinum", "gold", "silver", "private"],
    "risk_categories": ["low", "medium", "high"],
    
    # Technical Standards
    "allowed_transformations": ["direct", "sum", "average", "count"],
    "required_documentation": [
        "source_systems",
        "field_mappings", 
        "refresh_schedule"
    ],
    
    # Security
    "encryption_required": True,
    "retention_period_days": 365,
    
    # Sample Target Schema
    "customer_360_schema": {
        "Customer_ID": {"type": "string", "source": "all"},
        "Total_Assets": {"type": "float", "sources": ["accounts", "investments"]},
        "Transaction_Count": {"type": "integer", "source": "transactions"},
        "Risk_Category": {"type": "string", "logic": "business_rules"}
    }
}