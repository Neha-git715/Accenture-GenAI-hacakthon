#fast api endpoints
# /design-product, /validate etc.

from fastapi import APIRouter, HTTPException
from agents.interpreter import BankingInterpreter
from agents.mapper import DataMapper

router = APIRouter()
interpreter = BankingInterpreter()

@router.post("/design-product")
async def design_product(query: str):
    result = interpreter.generate_sql(query)
    if result["error"]:
        raise HTTPException(400, detail=result["error"])
    
    if not DataMapper.validate_sql(result["sql"]):
        raise HTTPException(400, detail="Query violates banking rules")
    
    return {
        "sql": result["sql"],
        "sample_data": DataMapper.get_sample_data(),
        "schema": "customers(id,name,tier,account_type,balance)"
    }

@staticmethod
def validate_sql(sql: str) -> bool:
    """Check for forbidden operations"""
    banned = ['DROP', 'DELETE', 'UPDATE']
    return not any(cmd in sql.upper() for cmd in banned)

@staticmethod
def get_sample_data() -> list:
    """Return 3 rows from merged data for demo"""
    df = DataMapper.merge_tables("data/customers.csv", "data/loans.csv")
    return df.head(3).to_dict(orient='records')