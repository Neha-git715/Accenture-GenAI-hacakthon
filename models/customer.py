from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class CustomerType(str, Enum):
    RETAIL = "retail"
    BUSINESS = "business"
    PREMIUM = "premium"

class Address(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    address_type: str = Field(default="primary")

class ContactInfo(BaseModel):
    email: str
    phone: str
    preferred_contact_method: str = Field(default="email")
    is_opt_in: bool = Field(default=False)

class AccountInfo(BaseModel):
    account_number: str
    account_type: str
    balance: float
    currency: str
    status: str
    opened_date: datetime
    last_activity_date: Optional[datetime] = None

class Customer(BaseModel):
    customer_id: str = Field(..., description="Unique identifier for the customer")
    customer_type: CustomerType
    first_name: str
    last_name: str
    date_of_birth: datetime
    addresses: List[Address] = Field(default_factory=list)
    contact_info: ContactInfo
    accounts: List[AccountInfo] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, str] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": "CUST123456",
                "customer_type": "retail",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-01-01T00:00:00",
                "addresses": [
                    {
                        "street": "123 Main St",
                        "city": "New York",
                        "state": "NY",
                        "postal_code": "10001",
                        "country": "USA",
                        "address_type": "primary"
                    }
                ],
                "contact_info": {
                    "email": "john.doe@example.com",
                    "phone": "+1-555-555-5555",
                    "preferred_contact_method": "email",
                    "is_opt_in": True
                },
                "accounts": [
                    {
                        "account_number": "ACC123456",
                        "account_type": "checking",
                        "balance": 1000.00,
                        "currency": "USD",
                        "status": "active",
                        "opened_date": "2023-01-01T00:00:00"
                    }
                ]
            }
        } 