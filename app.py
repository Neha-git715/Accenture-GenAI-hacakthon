# Main FastAPI app

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from models.customer import Customer
from models.data_product import DataProduct, Attribute, SourceSystem
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
async def validate_data_product(data_product: DataProduct):
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)