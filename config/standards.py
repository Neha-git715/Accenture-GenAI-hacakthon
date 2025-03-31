#PII /field requirements

BANKING_STANDARDS = {
    # Field Requirements
    "required_fields": ["Customer_ID", "Amount", "Date"],
    "pii_fields": ["SSN", "Account_Number", "DOB"],
    
    # Business Rules
    "amount_checks": {
        "min_loan": 1000,
        "max_transaction": 50000
    },
    
    # Data Product Specs
    "target_schema": {
        "Customer_360": [
            {"target": "customer_id", "source": "Customer_ID", "type": "str"},
            {"target": "total_loans", "source": "Amount", "agg": "sum"}
        ]
    }
}