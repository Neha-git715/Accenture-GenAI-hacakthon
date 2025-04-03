from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class DataProductStatus(str, Enum):
    DRAFT = "Draft"
    IN_REVIEW = "In Review"
    ACTIVE = "Active"
    DEPRECATED = "Deprecated"

class CertificationStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    CERTIFIED = "Certified"
    FAILED = "Failed"

class DataAttribute(BaseModel):
    name: str
    data_type: str
    description: str
    is_pii: bool = False
    is_required: bool = True
    validation_rules: Optional[Dict] = None

class DataEntity(BaseModel):
    name: str
    description: str
    attributes: List[DataAttribute]
    primary_key: List[str]
    relationships: Optional[Dict[str, str]] = None

class SourceSystem(BaseModel):
    name: str
    system_type: str
    connection_details: Dict
    available_entities: List[str]

class AttributeMapping(BaseModel):
    source_attribute: str
    target_attribute: str
    transformation_rule: Optional[str] = None
    data_quality_checks: Optional[List[str]] = None

class DataProductStructure(BaseModel):
    entities: List[DataEntity]
    source_mappings: Dict[str, List[AttributeMapping]]
    refresh_frequency: str
    data_quality_rules: Dict[str, List[str]]

class DataProduct(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    status: DataProductStatus = DataProductStatus.DRAFT
    structure: Optional[DataProductStructure] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    certification_status: CertificationStatus = CertificationStatus.PENDING
    owner: str
    version: str = "1.0.0"
    tags: List[str] = [] 