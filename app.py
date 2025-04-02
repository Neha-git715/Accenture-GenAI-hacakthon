# Main FastAPI app

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime  # Added import for datetime
from models.customer import Customer
from models.data_product import DataProduct as ModelDataProduct
from models.data_product import Attribute, SourceSystem
from agents.interpreter import UseCaseInterpreter
from agents.mapper import DataProductMapper
from agents.validator import DataProductValidator

# Define request models
class UseCaseRequest(BaseModel):
    use_case_description: str

app = FastAPI(
    title="BankGen 360 API",
    description="API for managing BankGen 360 data products and recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
interpreter = UseCaseInterpreter()
mapper = DataProductMapper()
validator = DataProductValidator()

@app.post("/analyze-requirements")
async def analyze_requirements(request: UseCaseRequest):
    """
    Analyze business requirements and recommend data product structure
    """
    try:
        requirements = await interpreter.analyze_requirements(request.use_case_description)
        return requirements
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/design-data-product")
async def design_data_product(requirements: dict):
    """
    Design data product structure based on requirements
    """
    try:
        data_product = await mapper.design_data_product(requirements)
        return data_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate-data-product")
async def validate_data_product(data_product: ModelDataProduct):
    """
    Validate data product design and ensure compliance
    """
    try:
        validation_result = await validator.validate_data_product(data_product)
        return validation_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommend-attributes")
async def recommend_attributes(use_case: str):
    """
    Recommend attributes based on use case
    """
    try:
        attributes = await mapper.recommend_attributes(use_case)
        return attributes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/source-systems")
async def get_source_systems():
    """
    Get available source systems
    """
    try:
        systems = await mapper.get_source_systems()
        return systems
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/map-attributes")
async def map_attributes(
    attributes: List[Attribute],
    source_systems: List[SourceSystem]
):
    """
    Map attributes to source systems
    """
    try:
        mappings = await mapper.map_attributes(attributes, source_systems)
        return mappings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Data Product Models for API endpoints
class DataProductCreate(BaseModel):
    name: str
    description: str
    status: str = "Draft"
    refresh_frequency: str

class DataProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    refresh_frequency: Optional[str] = None

class DataProduct(BaseModel):
    id: int
    name: str
    description: str
    status: str
    last_updated: datetime
    refresh_frequency: str

# Mock database - replace with actual database in production
data_products_db = [
    {
        "id": 1,
        "name": "Customer Profile Data",
        "description": "Comprehensive customer information including demographics and preferences",
        "status": "Active",
        "last_updated": datetime.now(),
        "refresh_frequency": "Daily"
    },
    {
        "id": 2,
        "name": "Transaction History",
        "description": "Historical record of all customer transactions and account activities",
        "status": "Active",
        "last_updated": datetime.now(),
        "refresh_frequency": "Real-time"
    },
    {
        "id": 3,
        "name": "Account Balance Analytics",
        "description": "Analytical insights into account balances and trends",
        "status": "Draft",
        "last_updated": datetime.now(),
        "refresh_frequency": "Hourly"
    }
]

@app.get("/data-products", response_model=List[DataProduct])
async def get_data_products():
    """
    Get all data products
    """
    return data_products_db

@app.post("/data-products", response_model=DataProduct)
async def create_data_product(product: DataProductCreate):
    """
    Create a new data product
    """
    new_product = {
        "id": len(data_products_db) + 1,
        "name": product.name,
        "description": product.description,
        "status": product.status,
        "last_updated": datetime.now(),
        "refresh_frequency": product.refresh_frequency
    }
    data_products_db.append(new_product)
    return new_product

@app.put("/data-products/{product_id}", response_model=DataProduct)
async def update_data_product(product_id: int, product: DataProductUpdate):
    """
    Update an existing data product
    """
    for i, p in enumerate(data_products_db):
        if p["id"] == product_id:
            for key, value in product.dict(exclude_unset=True).items():
                data_products_db[i][key] = value
            data_products_db[i]["last_updated"] = datetime.now()
            return data_products_db[i]
    raise HTTPException(status_code=404, detail=f"Data product with ID {product_id} not found")

@app.delete("/data-products/{product_id}")
async def delete_data_product(product_id: int):
    """
    Delete a data product
    """
    for i, p in enumerate(data_products_db):
        if p["id"] == product_id:
            del data_products_db[i]
            return {"message": f"Data product with ID {product_id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Data product with ID {product_id} not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)