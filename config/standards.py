#PII /field requirements

BANKING_RULES= {
    # Field Requirements
    "required_fields": ["Customer_ID", "Tier"],
    "pii_fields": ["SSN", "Account_Number"],
    
    # Business Rules
    "tiers": ["platinum", "gold", "silver"],
    "min_investment": 100000,
    "amount_checks": {
        "min_transaction": 1,  # Reject $0 transactions
        "max_single_deposit": 10000
    },
    
    # Security
    "SQL_BLACKLIST": ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE"],
    "AML_THRESHOLD": 10000,  # Transactions >$10K need review
    
    # Schema
    "approved_joins": ["Customer_ID", "Account_ID"]
}