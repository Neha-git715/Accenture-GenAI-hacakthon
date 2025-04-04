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

# Helper function to convert DB row to dict with proper JSON decoding
def row_to_product(row: sqlite3.Row) -> dict:
    product = dict(row)
    # Convert structure from JSON string to dict, if present
    if product.get("structure"):
        try:
            product["structure"] = json.loads(product["structure"])
        except Exception:
            product["structure"] = None
    # Convert source_mappings from JSON string to dict, if present
    if product.get("source_mappings"):
        try:
            product["source_mappings"] = json.loads(product["source_mappings"])
        except Exception:
            product["source_mappings"] = None
    return product

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
                model='tinyllama',
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
    rows = cursor.fetchall()
    conn.close()
    return [row_to_product(row) for row in rows]

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
            structure = GenAIService.generate_data_product_structure(product.use_case)
            product_data["structure"] = json.dumps(structure)
            product_data["refresh_frequency"] = structure.get("recommended_refresh_frequency", product.refresh_frequency)
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
    row = cursor.fetchone()
    conn.close()
    
    return row_to_product(row)

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
    row = cursor.fetchone()
    conn.close()
    
    return row_to_product(row)

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
    cursor.execute("SELECT * FROM data_products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Data product not found")
    
    product_dict = dict(row)
    
    # If the structure is missing, try to generate one using the product description as a fallback.
    if not product_dict.get('structure'):
        if product_dict.get('description'):
            try:
                structure = GenAIService.generate_data_product_structure(product_dict['description'])
                product_dict["structure"] = json.dumps(structure)
                cursor.execute(
                    "UPDATE data_products SET structure = ? WHERE id = ?",
                    (json.dumps(structure), product_id)
                )
                conn.commit()
            except Exception as e:
                conn.close()
                raise HTTPException(status_code=500, detail="Failed to generate structure for data product")
        else:
            conn.close()
            raise HTTPException(status_code=400, detail="Data product has no structure defined and no description available to generate one")
    
    try:
        structure = json.loads(product_dict["structure"])
    except json.JSONDecodeError as je:
        conn.close()
        raise HTTPException(status_code=500, detail="Invalid JSON structure format")
    
    prompt = f"""
    As a Banking Data Architect, create source-to-target mappings for:
    {json.dumps(structure, indent=2)}
    
    Output JSON with:
    - source_system (core banking, CRM, etc.)
    - source_fields
    - transformation_rules
    - data_quality_checks
    
    Ensure your response is valid JSON format.
    """
    
    try:
        response = ollama.generate(
            model='tinyllama',
            prompt=prompt,
            format='json',
            options={'temperature': 0.2}
        )
    except Exception as e:
        logger.error(f"Ollama API error: {str(e)}")
        conn.close()
        raise HTTPException(status_code=500, detail=f"AI model call failed: {str(e)}")
    
    try:
        if not response or 'response' not in response:
            raise ValueError("Empty or invalid response from Ollama API")
            
        mappings = json.loads(response['response'])
        
        if not isinstance(mappings, dict):
            raise ValueError("Generated mappings is not a valid JSON object")
        
        required_fields = ['source_system', 'source_fields', 'transformation_rules', 'data_quality_checks']
        missing_fields = [field for field in required_fields if field not in mappings]
        
        if missing_fields:
            logger.warning(f"Generated mappings missing fields: {', '.join(missing_fields)}")
            for field in missing_fields:
                mappings[field] = "Unknown" if field == 'source_system' else []
        
        cursor.execute(
            "UPDATE data_products SET source_mappings = ? WHERE id = ?",
            (json.dumps(mappings), product_id)
        )
        conn.commit()
        conn.close()
        
        return mappings
        
    except json.JSONDecodeError as je:
        logger.error(f"Failed to parse LLM response as JSON: {str(je)}")
        conn.close()
        raise HTTPException(status_code=500, detail="AI generated invalid JSON. Try again or use a different model.")
    except Exception as e:
        logger.error(f"Mapping generation failed: {str(e)}")
        conn.close()
        raise HTTPException(status_code=500, detail=f"AI mapping generation failed: {str(e)}")

@api_router.post("/data-products/{product_id}/validate")
async def validate_data_product(product_id: int):
    """Validate a data product's structure and source mappings"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data_products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Data product not found")
    
    product_dict = row_to_product(row)
    validation_result = {
        "id": product_dict["id"],
        "name": product_dict["name"],
        "is_valid": True,
        "issues": [],
        "warnings": [],
        "recommendations": []
    }
    
    # Validate structure
    if not product_dict["structure"]:
        validation_result["is_valid"] = False
        validation_result["issues"].append("Missing data structure definition")
    else:
        try:
            structure = product_dict["structure"]
            if "entities" not in structure:
                validation_result["issues"].append("Missing 'entities' in structure")
                validation_result["is_valid"] = False
            elif not structure["entities"]:
                validation_result["warnings"].append("Empty entities list in structure")
            
            if "attributes" not in structure:
                validation_result["issues"].append("Missing 'attributes' in structure")
                validation_result["is_valid"] = False
            
            if "relationships" not in structure:
                validation_result["warnings"].append("Missing 'relationships' in structure")
            
            if "entities" in structure and "attributes" in structure:
                for entity in structure.get("entities", []):
                    entity_name = entity.get("name", "")
                    if not any(attr.get("entity") == entity_name for attr in structure.get("attributes", [])):
                        validation_result["warnings"].append(f"Entity '{entity_name}' has no associated attributes")
        
        except Exception:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Invalid JSON in structure field")
    
    # Validate source mappings
    if not product_dict["source_mappings"]:
        validation_result["warnings"].append("Missing source mappings")
    else:
        try:
            mappings = product_dict["source_mappings"]
            if not mappings.get("source_system"):
                validation_result["warnings"].append("No source systems defined in mappings")
            if "source_fields" not in mappings:
                validation_result["warnings"].append("Missing 'source_fields' in mappings")
            if "transformation_rules" not in mappings:
                validation_result["warnings"].append("Missing 'transformation_rules' in mappings")
            if "data_quality_checks" not in mappings:
                validation_result["warnings"].append("Missing 'data_quality_checks' in mappings")
                validation_result["recommendations"].append("Add data quality checks to ensure data integrity")
        
        except Exception:
            validation_result["warnings"].append("Invalid JSON in source_mappings field")
    
    # Generate AI-based recommendations if needed
    if not validation_result["is_valid"] or validation_result["warnings"]:
        try:
            prompt = f"""
            As a Banking Data Quality Expert, provide 3 concise recommendations to improve this data product:
            
            Product Name: {product_dict["name"]}
            Description: {product_dict["description"]}
            Issues: {validation_result["issues"]}
            Warnings: {validation_result["warnings"]}
            
            Output JSON with array of recommendations (max 3).
            """
            response = ollama.generate(
                model='tinyllama',
                prompt=prompt,
                format='json',
                options={'temperature': 0.3}
            )
            ai_recommendations = json.loads(response['response'])
            if "recommendations" in ai_recommendations:
                validation_result["recommendations"].extend(ai_recommendations["recommendations"])
        except Exception as e:
            logger.warning(f"AI recommendations generation skipped: {str(e)}")
    
    conn.close()
    return validation_result

# Include the API router
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
