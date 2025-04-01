#ollama llm integration
#Critical for converting:


import ollama
from typing import Dict, Optional
import re
from config.standards import BANKING_RULES

class BankingInterpreter:
    """
    Converts natural language banking queries to SQL with:
    - PII masking
    - Compliance checks
    - Banking schema awareness
    """
    
    def __init__(self, model: str = "llama2"):
        self.model = model
        self._setup_prompt_templates()
    
    def _setup_prompt_templates(self):
        self.system_prompt = f"""You are a banking SQL expert. Rules:
        1. Available tables:
           - customers(Customer_ID,Name,Tier,Join_Date)
           - loans(Loan_ID,Customer_ID,Type,Amount,Issue_Date)
           - transactions(Transaction_ID,Customer_ID,Amount,Type,Date)
           - accounts(Account_ID,Customer_ID,Type,Balance)
        
        2. Always join on Customer_ID
        3. Never expose SSN/Account_Numbers (they don't exist in our tables)
        4. Required fields for compliance: {BANKING_RULES['required_fields']}
        5. Output ONLY SQL, no explanations"""
    
    def _mask_pii(self, text: str) -> str:
        """Redact sensitive patterns pre-processing"""
        patterns = {
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'Account': r'\b[A-Z]{2}\d{4,10}\b',
            'Phone': r'\b\d{3}-\d{3}-\d{4}\b'
        }
        for label, pattern in patterns.items():
            text = re.sub(pattern, f'[{label}_MASKED]', text)
        return text

    def generate_sql(self, natural_query: str) -> Dict[str, Optional[str]]:
        """
        Converts natural language to compliant SQL
        Returns: {'sql': str, 'error': Optional[str]}
        """
        try:
            # Step 1: PII Sanitization
            clean_query = self._mask_pii(natural_query)
            
            # Step 2: LLM Conversion
            response = ollama.generate(
                model=self.model,
                system=self.system_prompt,
                prompt=f"Convert to SQL: {clean_query}",
                options={'temperature': 0}  # Deterministic mode
            )
            sql = response['response'].strip()
            
            # Step 3: Compliance Validation
            if any(pii in sql.lower() for pii in ['ssn', 'password', 'pin']):
                raise ValueError("PII access attempt")
                
            if not all(field in sql.lower() for field in BANKING_RULES['required_fields']):
                raise ValueError(f"Query missing required fields: {BANKING_RULES['required_fields']}")
                
            return {'sql': sql, 'error': None}
        
            if any(cmd in sql.upper() for cmd in BANKING_RULES['SQL_BLACKLIST']):
                raise ValueError("Dangerous SQL operation detected")  
            
        except Exception as e:
            return {'sql': None, 'error': f"Compliance violation: {str(e)}"}

# Example usage
if __name__ == "__main__":
    interpreter = BankingInterpreter()
    test_query = "Show platinum customers with mortgages above $400K"
    result = interpreter.generate_sql(test_query)
    print(result)