# Main FastAPI app

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from typing import List
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="BankGen 360 API",
    description="API for managing BankGen 360 data products",
    version="1.0.0"
)

# Create API router with version prefix
api_router = APIRouter(prefix="/api/v1")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs")

# Data Product Models
class DataProductCreate(BaseModel):
    name: str
    description: str
    status: str = "Draft"
    refresh_frequency: str

class DataProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    refresh_frequency: str | None = None

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
    }
]

@api_router.get("/data-products", response_model=List[DataProduct])
async def get_data_products():
    """Get all data products"""
    return data_products_db

@api_router.post("/data-products", response_model=DataProduct)
async def create_data_product(product: DataProductCreate):
    """Create a new data product"""
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

@api_router.put("/data-products/{product_id}", response_model=DataProduct)
async def update_data_product(product_id: int, product: DataProductUpdate):
    """Update an existing data product"""
    for i, p in enumerate(data_products_db):
        if p["id"] == product_id:
            for key, value in product.dict(exclude_unset=True).items():
                data_products_db[i][key] = value
            data_products_db[i]["last_updated"] = datetime.now()
            return data_products_db[i]
    raise HTTPException(status_code=404, detail=f"Data product with ID {product_id} not found")

@api_router.delete("/data-products/{product_id}")
async def delete_data_product(product_id: int):
    """Delete a data product"""
    for i, p in enumerate(data_products_db):
        if p["id"] == product_id:
            del data_products_db[i]
            return {"message": f"Data product with ID {product_id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Data product with ID {product_id} not found")

# Include the API router
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)