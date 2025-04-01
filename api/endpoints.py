#fast api endpoints
# /design-product, /validate etc.

from fastapi import APIRouter, HTTPException, Body
from agents.interpreter import BankingInterpreter
from agents.validator import BankingValidator
from agents.mapper import DataProductMapper
from typing import Dict, List
import pandas as pd

router = APIRouter()
interpreter = BankingInterpreter()
validator = BankingValidator()
mapper = DataProductMapper()

@router.post("/design-product")
async def design_product(
    requirements: str = Body(..., embed=True, example="Create customer 360 view")
) -> Dict:
    """End-to-end data product creation flow with:
    - Source identification
    - Schema generation
    - Data mapping
    - Compliance certification
    """
    try:
        # Step 1: Identify relevant data sources
        sources = mapper.identify_sources(requirements)
        if not sources:
            raise ValueError("No relevant data sources found for these requirements")

        # Step 2: Generate target schema
        schema = validator.generate_data_product_schema(list(sources.keys()))
        
        # Step 3: Create field mappings
        mappings = mapper.create_mapping(sources, schema)
        
        # Step 4: Execute transformations
        data_product = mapper.execute_mapping(mappings)
        
        # Step 5: Validate and certify
        certification = validator.validate_data_product(data_product)
        
        # Prepare sample data (anonymized)
        sample_data = DataMapper.safe_display(data_product.head(3)).to_dict(orient='records')

        return {
            "schema": schema,
            "mappings": mappings,
            "sample_data": sample_data,
            "certification": certification,
            "source_tables": sources,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": str(e),
                "status": "failed",
                "suggestion": "Try more specific requirements like 'Create view with customer balances and risk scores'"
            }
        )