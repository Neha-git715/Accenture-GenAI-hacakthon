from fastapi import FastAPI, HTTPException, APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import ollama
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BankGen 360 API",
    description="API for managing BankGen 360 data products with GenAI capabilities",
    version="1.0.0"
)

# Create API router with version prefix
api_router = APIRouter(prefix="/api/v1")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('bankgen360.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Draft',
            structure TEXT,
            source_mappings TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            refresh_frequency TEXT,
            certification_status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Data Product Models
class DataProductCreate(BaseModel):
    name: str
    description: str
    status: Optional[str] = "Draft"
    refresh_frequency: str
    use_case: Optional[str] = None

class DataProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    refresh_frequency: Optional[str] = None
    certification_status: Optional[str] = None

class DataProduct(BaseModel):
    id: int
    name: str
    description: str
    status: str
    structure: Optional[dict] = None
    source_mappings: Optional[dict] = None
    last_updated: datetime
    refresh_frequency: str
    certification_status: str

# GenAI Service
class GenAIService:
    @staticmethod
    def generate_data_product_structure(use_case: str):
        try:
            prompt = f"""
            As a Banking Data Product Designer, create a comprehensive data structure for:
            {use_case}
            
            Output JSON format with:
            - entities (required customer data entities)
            - attributes (key fields per entity)
            - relationships (how entities connect)
            - recommended_refresh_frequency
            """
            
            response = ollama.generate(
                model='mistral',
                prompt=prompt,
                format='json',
                options={'temperature': 0.3}
            )
            
            return json.loads(response['response'])
        except Exception as e:
            logger.error(f"GenAI generation failed: {str(e)}")
            raise HTTPException(status_code=500, detail="AI generation failed")

# Database operations
def get_db_connection():
    conn = sqlite3.connect('bankgen360.db')
    conn.row_factory = sqlite3.Row
    return conn

# API Endpoints
@app.get("/")
async def root():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs")

@api_router.get("/data-products", response_model=List[DataProduct])
async def get_data_products():
    """Get all data products"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data_products")
    products = cursor.fetchall()
    conn.close()
    return [dict(product) for product in products]

@api_router.post("/data-products", response_model=DataProduct)
async def create_data_product(product: DataProductCreate):
    """Create a new data product with optional AI generation"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    product_data = {
        "name": product.name,
        "description": product.description,
        "status": product.status,
        "refresh_frequency": product.refresh_frequency,
        "structure": None  # Initialize structure to None by default
    }
    
    # Generate structure with AI if use_case provided
    if product.use_case:
        try:
            ai_service = GenAIService()
            structure = ai_service.generate_data_product_structure(product.use_case)
            product_data["structure"] = json.dumps(structure)
            product_data["refresh_frequency"] = structure.get("recommended_refresh_frequency", 
                                                          product.refresh_frequency)
        except Exception as e:
            logger.warning(f"AI generation skipped: {str(e)}")
    
    cursor.execute(
        """
        INSERT INTO data_products (name, description, status, refresh_frequency, structure)
        VALUES (:name, :description, :status, :refresh_frequency, :structure)
        """,
        product_data
    )
    conn.commit()
    product_id = cursor.lastrowid
    
    # Fetch the created product to return complete object
    cursor.execute("SELECT * FROM data_products WHERE id = ?", (product_id,))
    created_product = dict(cursor.fetchone())
    conn.close()
    
    return created_product

@api_router.put("/data-products/{product_id}", response_model=DataProduct)
async def update_data_product(product_id: int, product: DataProductUpdate):
    """Update an existing data product"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    update_fields = {k: v for k, v in product.dict().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    set_clause = ", ".join(f"{key} = ?" for key in update_fields.keys())
    values = list(update_fields.values())
    values.append(product_id)
    
    cursor.execute(
        f"UPDATE data_products SET {set_clause} WHERE id = ?",
        values
    )
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Data product not found")
    
    conn.commit()
    cursor.execute("SELECT * FROM data_products WHERE id = ?", (product_id,))
    updated_product = cursor.fetchone()
    conn.close()
    
    return dict(updated_product)

@api_router.delete("/data-products/{product_id}")
async def delete_data_product(product_id: int):
    """Delete a data product"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM data_products WHERE id = ?", (product_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Data product not found")
    
    conn.commit()
    conn.close()
    return {"message": "Data product deleted successfully"}

@api_router.post("/data-products/{product_id}/generate-mappings")
async def generate_source_mappings(product_id: int):
    """Generate source system mappings for a data product using AI"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT structure FROM data_products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        raise HTTPException(status_code=404, detail="Data product not found")
    
    try:
        structure = json.loads(product['structure'])
        prompt = f"""
        As a Banking Data Architect, create source-to-target mappings for:
        {json.dumps(structure, indent=2)}
        
        Output JSON with:
        - source_system (core banking, CRM, etc.)
        - source_fields
        - transformation_rules
        - data_quality_checks
        """
        
        response = ollama.generate(
            model='mistral',
            prompt=prompt,
            format='json',
            options={'temperature': 0.2}
        )
        
        mappings = json.loads(response['response'])
        cursor.execute(
            "UPDATE data_products SET source_mappings = ? WHERE id = ?",
            (json.dumps(mappings), product_id)
        )
        conn.commit()
        conn.close()
        
        return mappings
    except Exception as e:
        logger.error(f"Mapping generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="AI mapping generation failed")

# Include the API router
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)