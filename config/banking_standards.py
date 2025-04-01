"""
Consolidated banking standards and rules configuration
"""

# Banking data standards
BANKING_STANDARDS = {
    'DATA_TYPES': {
        'customer_id': {
            'type': 'string',
            'format': '^[A-Z0-9]{10}$',
            'description': 'Unique customer identifier'
        },
        'account_number': {
            'type': 'string',
            'format': '^[0-9]{12}$',
            'description': 'Bank account number'
        },
        'balance': {
            'type': 'decimal',
            'precision': '18,2',
            'description': 'Account balance'
        },
        'transaction_amount': {
            'type': 'decimal',
            'precision': '18,2',
            'description': 'Transaction amount'
        }
    },
    
    'VALIDATION_RULES': {
        'required_fields': [
            'customer_id',
            'account_number',
            'balance'
        ],
        'format_rules': {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?[1-9]\d{1,14}$',
            'postal_code': r'^[0-9]{5,10}$'
        }
    }
}

# Banking compliance rules
BANKING_RULES = {
    'SQL_BLACKLIST': [
        'DROP',
        'DELETE',
        'UPDATE',
        'INSERT',
        'TRUNCATE',
        'ALTER',
        'CREATE',
        'GRANT',
        'REVOKE'
    ],
    
    'PII_FIELDS': [
        'ssn',
        'tax_id',
        'passport_number',
        'drivers_license',
        'bank_account',
        'credit_card'
    ],
    
    'COMPLIANCE_RULES': {
        'gdpr': {
            'data_retention': '7 years',
            'consent_required': True,
            'right_to_access': True,
            'right_to_erasure': True
        },
        'pci_dss': {
            'card_data_encryption': True,
            'access_control': True,
            'audit_logging': True
        }
    },
    
    'DATA_QUALITY_RULES': {
        'balance': {
            'not_null': True,
            'positive_value': True,
            'precision': '18,2'
        },
        'transaction': {
            'not_null': True,
            'valid_amount': True,
            'valid_date': True
        }
    }
}

# Source system mappings
SOURCE_SYSTEMS = {
    'core_banking': {
        'system_id': 'SYS001',
        'system_name': 'Core Banking System',
        'system_type': 'mainframe',
        'connection_details': {
            'host': 'mainframe.example.com',
            'port': '1433',
            'database': 'core_banking'
        }
    },
    'crm': {
        'system_id': 'SYS002',
        'system_name': 'CRM System',
        'system_type': 'relational',
        'connection_details': {
            'host': 'crm.example.com',
            'port': '5432',
            'database': 'crm_db'
        }
    },
    'digital_banking': {
        'system_id': 'SYS003',
        'system_name': 'Digital Banking Platform',
        'system_type': 'nosql',
        'connection_details': {
            'host': 'digital.example.com',
            'port': '27017',
            'database': 'digital_banking'
        }
    }
}

# Data product templates
DATA_PRODUCT_TEMPLATES = {
    'customer_360': {
        'name': 'BankGen 360',
        'description': 'Comprehensive view of customer information for retail banking',
        'refresh_frequency': 'daily',
        'retention_period': '7 years',
        'required_attributes': [
            'customer_id',
            'account_number',
            'balance',
            'transaction_amount',
            'customer_name',
            'email',
            'phone',
            'address',
            'tier',
            'risk_score'
        ]
    }
} 