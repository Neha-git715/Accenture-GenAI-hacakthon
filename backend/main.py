from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import uvicorn
from pydantic import BaseModel

from agents.intelligent_orchestrator import IntelligentOrchestrator
from agents.use_case_interpreter import UseCaseInterpreterAgent
from agents.data_product_designer import DataProductDesignerAgent
from agents.source_system_mapper import SourceSystemMapperAgent
from agents.data_product_validator import DataProductValidatorAgent
from tools.schema_matcher import SchemaMatcherAI

app = FastAPI(
    title="Customer 360 Data Product Designer",
    description="AI-powered data product design and recommendation system",
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
orchestrator = IntelligentOrchestrator()
use_case_agent = UseCaseInterpreterAgent()
designer_agent = DataProductDesignerAgent()
mapper_agent = SourceSystemMapperAgent()
validator_agent = DataProductValidatorAgent()
schema_matcher = SchemaMatcherAI()

class UseCaseRequest(BaseModel):
    use_case: str
    context: Dict[str, Any] = {}

class SourceMappingRequest(BaseModel):
    data_product_id: str
    source_systems: list

@app.post("/api/analyze-use-case")
async def analyze_use_case(request: UseCaseRequest):
    """Analyze business use case and extract requirements"""
    try:
        # Process through orchestrator
        analysis = await orchestrator.process_with_memory(
            prompt=request.use_case,
            context=request.context
        )
        
        # Get detailed requirements through use case agent
        requirements = await use_case_agent.process({
            "use_case": request.use_case,
            "initial_analysis": analysis
        })
        
        return {
            "status": "success",
            "analysis": analysis,
            "requirements": requirements
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/design-data-product")
async def design_data_product(requirements: Dict[str, Any]):
    """Design data product structure based on requirements"""
    try:
        # Get design through designer agent
        design = await designer_agent.process({
            "requirements": requirements
        })
        
        return {
            "status": "success",
            "design": design
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/create-mappings")
async def create_mappings(request: SourceMappingRequest):
    """Create source system mappings"""
    try:
        # Get mappings through mapper agent
        mappings = await mapper_agent.process({
            "data_product_id": request.data_product_id,
            "source_systems": request.source_systems
        })
        
        # Enhance mappings with schema matcher
        enhanced_mappings = await schema_matcher.match_schemas(
            source_schema=mappings["source_schema"],
            target_schema=mappings["target_schema"]
        )
        
        return {
            "status": "success",
            "mappings": enhanced_mappings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validate-data-product")
async def validate_data_product(data_product: Dict[str, Any]):
    """Validate and certify data product"""
    try:
        # Get validation through validator agent
        validation = await validator_agent.process({
            "data_product": data_product
        })
        
        return {
            "status": "success",
            "validation": validation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/learning-stats")
async def get_learning_stats():
    """Get learning statistics from the orchestrator"""
    try:
        return orchestrator.get_learning_statistics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 