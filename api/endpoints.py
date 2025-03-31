#fast api endpoints
# /design-product, /validate etc.

from fastapi import APIRouter, HTTPException
from agents.interpreter import BankingInterpreter
from agents.mapper import DataMapper

router = APIRouter()
interpreter = BankingInterpreter()

@router.post("/design-product")
async def design_product(query: str):
    # Step 1: Convert to SQL
    result = interpreter.to_sql(query)
    if result["error"]:
        raise HTTPException(400, detail=result["error"])
    
    # Step 2: Execute Mapping
    try:
        df = DataMapper.merge_data(
            "data/loans_sample.csv",
            "data/transactions_sample.csv"
        )
        return {
            "sql": result["sql"],
            "sample_data": df.head(3).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))