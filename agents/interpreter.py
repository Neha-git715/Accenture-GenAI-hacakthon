#ollama llm integration
#Critical for converting:


import ollama
from typing import Dict, Optional, List
import re
from config.banking_standards import BANKING_STANDARDS, BANKING_RULES
from models.data_product import DataProduct, Attribute

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

class UseCaseInterpreter:
    def __init__(self):
        self.model = "llama2"  # Using Llama 2 model for analysis
        
    async def analyze_requirements(self, use_case_description: str) -> Dict:
        """
        Analyze business requirements and extract key data requirements
        """
        prompt = f"""
        Analyze the following business use case and extract key data requirements:
        
        Use Case: {use_case_description}
        
        Please provide:
        1. Key data attributes needed
        2. Data quality requirements
        3. Compliance requirements
        4. Source systems that might be needed
        5. Data refresh frequency
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {
                    "role": "system",
                    "content": "You are a data requirements analyst specializing in Customer 360 data products."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ])
            
            # Parse the response and structure it
            analysis = self._parse_analysis(response['message']['content'])
            return analysis
            
        except Exception as e:
            raise Exception(f"Error analyzing requirements: {str(e)}")
    
    def _parse_analysis(self, response: str) -> Dict:
        """
        Parse the LLM response into structured format
        """
        # This is a simplified parser - in production, you'd want more robust parsing
        sections = response.split("\n\n")
        analysis = {
            "data_attributes": [],
            "data_quality": [],
            "compliance": [],
            "source_systems": [],
            "refresh_frequency": "daily"  # default
        }
        
        for section in sections:
            if "Key data attributes" in section:
                analysis["data_attributes"] = self._extract_list_items(section)
            elif "Data quality" in section:
                analysis["data_quality"] = self._extract_list_items(section)
            elif "Compliance" in section:
                analysis["compliance"] = self._extract_list_items(section)
            elif "Source systems" in section:
                analysis["source_systems"] = self._extract_list_items(section)
            elif "Data refresh" in section:
                analysis["refresh_frequency"] = self._extract_refresh_frequency(section)
        
        return analysis
    
    def _extract_list_items(self, section: str) -> List[str]:
        """
        Extract list items from a section of text
        """
        items = []
        lines = section.split("\n")
        for line in lines:
            if line.strip().startswith("-") or line.strip().startswith("*"):
                items.append(line.strip("-* ").strip())
        return items
    
    def _extract_refresh_frequency(self, section: str) -> str:
        """
        Extract refresh frequency from text
        """
        # Default to daily if not specified
        return "daily"
    
    async def recommend_data_product_structure(self, requirements: Dict) -> DataProduct:
        """
        Recommend data product structure based on analyzed requirements
        """
        prompt = f"""
        Based on the following requirements, recommend a data product structure:
        
        Requirements: {requirements}
        
        Please provide:
        1. Data product name and description
        2. List of attributes with their types
        3. Source system mappings
        4. Data quality rules
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {
                    "role": "system",
                    "content": "You are a data product designer specializing in Customer 360 solutions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ])
            
            # Parse the response and create a DataProduct object
            product_structure = self._parse_product_structure(response['message']['content'])
            return product_structure
            
        except Exception as e:
            raise Exception(f"Error recommending data product structure: {str(e)}")
    
    def _parse_product_structure(self, response: str) -> DataProduct:
        """
        Parse the LLM response into a DataProduct object
        """
        # This is a simplified implementation - in production, you'd want more robust parsing
        sections = response.split("\n\n")
        
        # Extract basic product information
        name = "BankGen 360"  # default
        description = "Comprehensive view of customer information"
        version = "1.0.0"
        
        # Create attributes list
        attributes = []
        for section in sections:
            if "attributes" in section.lower():
                attribute_lines = section.split("\n")
                for line in attribute_lines:
                    if line.strip().startswith("-"):
                        attr_info = line.strip("- ").strip()
                        # Create Attribute object
                        attribute = Attribute(
                            attribute_id=f"ATTR{len(attributes)+1:03d}",
                            attribute_name=attr_info.split(":")[0].strip(),
                            attribute_type="string",  # default type
                            description=attr_info.split(":")[1].strip() if ":" in attr_info else "",
                            is_pii=False,
                            is_required=True,
                            source_system="core_banking",  # default
                            source_field=attr_info.split(":")[0].strip().lower()
                        )
                        attributes.append(attribute)
        
        # Create DataProduct object
        return DataProduct(
            product_id="DP001",
            product_name=name,
            product_type="customer_360",
            description=description,
            version=version,
            attributes=attributes,
            source_systems=[],  # Will be populated by mapper
            refresh_frequency="daily",
            retention_period="7 years",
            owner="Data Governance Team"
        )

# Example usage
if __name__ == "__main__":
    interpreter = BankingInterpreter()
    test_query = "Show platinum customers with mortgages above $400K"
    result = interpreter.generate_sql(test_query)
    print(result)