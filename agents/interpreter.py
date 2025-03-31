#ollama llm integration
#Critical for converting:


import ollama
from typing import Dict, Optional
import re

class BankingInterpreter:
    """Converts banking queries to SQL with PII protection"""
    
    def __init__(self, model: str = "llama2:13b"):
        self.model = model
        self.system_prompt = """You are a banking SQL expert. Rules:
        - Always join on Customer_ID
        - Tables: loans(customer_id,amount), transactions(customer_id,date,amount)
        - Never expose SSN/account numbers
        Output ONLY SQL, no explanations."""
    
    def _mask_pii(self, text: str) -> str:
        """Mask sensitive patterns"""
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)  # SSN
        return re.sub(r'\b[A-Z]{2}\d{4}[A-Z]{3}\b', '[ACCT]', text)  # Account numbers
    
    def to_sql(self, query: str) -> Dict[str, Optional[str]]:
        try:
            clean_query = self._mask_pii(query)
            response = ollama.generate(
                model=self.model,
                system=self.system_prompt,
                prompt=f"Convert to SQL: {clean_query}",
                options={'temperature': 0}  # Strict mode
            )
            sql = response['response'].strip()
            
            # Security check
            if any(s in sql.lower() for s in ['ssn', 'password', 'pin']):
                raise ValueError("PII access attempt")
                
            return {"sql": sql, "error": None}
            
        except Exception as e:
            return {"sql": None, "error": str(e)}