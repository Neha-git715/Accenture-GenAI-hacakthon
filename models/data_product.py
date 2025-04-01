from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class DataProductType(str, Enum):
    CUSTOMER_360 = "customer_360"
    TRANSACTION = "transaction"
    BEHAVIORAL = "behavioral"

class AttributeType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    JSON = "json"

class DataQualityRule(BaseModel):
    rule_id: str
    rule_name: str
    rule_type: str
    rule_expression: str
    severity: str
    description: str

class SourceSystem(BaseModel):
    system_id: str
    system_name: str
    system_type: str
    connection_details: Dict[str, str]
    last_sync: Optional[datetime] = None

class Attribute(BaseModel):
    attribute_id: str
    attribute_name: str
    attribute_type: AttributeType
    description: str
    is_pii: bool = False
    is_required: bool = True
    source_system: str
    source_field: str
    transformation_rule: Optional[str] = None
    data_quality_rules: List[DataQualityRule] = Field(default_factory=list)

class DataProduct(BaseModel):
    product_id: str
    product_name: str
    product_type: DataProductType
    description: str
    version: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    attributes: List[Attribute] = Field(default_factory=list)
    source_systems: List[SourceSystem] = Field(default_factory=list)
    refresh_frequency: str
    retention_period: str
    owner: str
    status: str = "draft"
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "DP001",
                "product_name": "Customer 360 View",
                "product_type": "customer_360",
                "description": "Comprehensive view of customer information and interactions",
                "version": "1.0.0",
                "attributes": [
                    {
                        "attribute_id": "ATTR001",
                        "attribute_name": "customer_id",
                        "attribute_type": "string",
                        "description": "Unique identifier for the customer",
                        "is_pii": False,
                        "is_required": True,
                        "source_system": "core_banking",
                        "source_field": "cust_id",
                        "data_quality_rules": [
                            {
                                "rule_id": "RULE001",
                                "rule_name": "NotNull",
                                "rule_type": "validation",
                                "rule_expression": "NOT NULL",
                                "severity": "error",
                                "description": "Customer ID cannot be null"
                            }
                        ]
                    }
                ],
                "source_systems": [
                    {
                        "system_id": "SYS001",
                        "system_name": "Core Banking System",
                        "system_type": "mainframe",
                        "connection_details": {
                            "host": "mainframe.example.com",
                            "port": "1433",
                            "database": "core_banking"
                        }
                    }
                ],
                "refresh_frequency": "daily",
                "retention_period": "7 years",
                "owner": "Data Governance Team"
            }
        } 