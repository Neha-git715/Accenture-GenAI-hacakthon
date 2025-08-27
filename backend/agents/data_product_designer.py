# from typing import Dict, Any, List
# import ollama
# import json
# from backend.agents.base_agent import BaseAgent
# from backend.models.schemas import DataEntity, DataAttribute, DataProductStructure

# class DataProductDesignerAgent(BaseAgent):
#     def __init__(self):
#         super().__init__(
#             name="Data Product Designer",
#             description="Designs optimal data product structure based on requirements"
#         )

#     def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
#         self.log_activity("Designing data product structure")
        
#         requirements = input_data.get("requirements", {})
#         if not requirements:
#             return self.format_response(
#                 data={},
#                 status="error",
#                 message="No requirements provided"
#             )

#         try:
#             # Generate data product structure using Ollama
#             prompt = f"""
#             As a Banking Data Architect, design a comprehensive data product structure for these requirements:
#             {json.dumps(requirements, indent=2)}

#             Provide a valid JSON structure with these exact fields:
#             {{
#                 "entities": [
#                     {{
#                         "name": "string",
#                         "description": "string",
#                         "attributes": [
#                             {{
#                                 "name": "string",
#                                 "data_type": "string",
#                                 "description": "string",
#                                 "is_pii": boolean,
#                                 "is_required": boolean
#                             }}
#                         ],
#                         "primary_key": ["string"]
#                     }}
#                 ],
#                 "relationships": [
#                     {{
#                         "from_entity": "string",
#                         "to_entity": "string",
#                         "type": "string",
#                         "description": "string"
#                     }}
#                 ],
#                 "refresh_frequency": "string",
#                 "data_quality_rules": {{
#                     "completeness": ["string"],
#                     "accuracy": ["string"],
#                     "consistency": ["string"]
#                 }}
#             }}

#             Example of a valid JSON:
#             {{
#                 "entities": [
#                     {{
#                         "name": "Customer",
#                         "description": "Customer details",
#                         "attributes": [
#                             {{
#                                 "name": "first_name",
#                                 "data_type": "string",
#                                 "description": "First name of the customer",
#                                 "is_pii": true,
#                                 "is_required": true
#                             }}
#                         ],
#                         "primary_key": ["customer_id"]
#                     }}
#                 ],
#                 "relationships": [],
#                 "refresh_frequency": "daily",
#                 "data_quality_rules": {{
#                     "completeness": ["All fields must be filled"],
#                     "accuracy": ["Data must be verified"],
#                     "consistency": ["Data must be consistent across systems"]
#                 }}
#             }}

#             Ensure all JSON is properly formatted with no trailing commas and all objects and arrays are closed properly.
#             """

#             response = ollama.generate(
#                 model='tinyllama',  # Using mistral for better JSON handling
#                 prompt=prompt,
#                 format='json',
#                 options={
#                     'temperature': 0.1,  # Lower temperature for more focused responses
#                     'top_p': 0.5,  # Lower top_p for faster sampling
#                     'context_window': 2048,  # Reduced context window
#                     'num_predict': 500,  # Reduced token prediction
#                     'num_ctx': 1024,  # Reduced context size
#                     'num_thread': 4  # Using more threads for faster processing
#                 }
#             )

#             # Clean and parse JSON response
#             json_str = response['response'].strip()
#             if not json_str.startswith('{'): 
#                 json_str = json_str[json_str.find('{'):]
#             if not json_str.endswith('}'):
#                 json_str = json_str[:json_str.rfind('}')+1]
            
#             structure_dict = json.loads(json_str)
            
#             # Convert to proper data structure
#             entities = []
#             for entity_dict in structure_dict.get("entities", []):
#                 attributes = [
#                     DataAttribute(**attr) 
#                     for attr in entity_dict.pop("attributes", [])
#                 ]
#                 entity = DataEntity(**entity_dict, attributes=attributes)
#                 entities.append(entity)

#             data_product_structure = DataProductStructure(
#                 entities=entities,
#                 source_mappings={},  # Will be filled by mapper agent
#                 refresh_frequency=structure_dict.get("refresh_frequency", "daily"),
#                 data_quality_rules=structure_dict.get("data_quality_rules", {})
#             )

#             self.log_activity("Successfully designed data product structure")
#             return self.format_response(
#                 data=data_product_structure.dict(),
#                 message="Data product structure design completed"
#             )

#         except json.JSONDecodeError as e:
#             self.log_activity(f"JSON parsing error: {str(e)}", "error")
#             return self.format_response(
#                 data={},
#                 status="error",
#                 message=f"Failed to parse JSON response: {str(e)}"
#             )
#         except Exception as e:
#             self.log_activity(f"Error designing data product: {str(e)}", "error")
#             return self.format_response(
#                 data={},
#                 status="error",
#                 message=f"Failed to design data product: {str(e)}"
#             ) 

# In backend/agents/data_product_designer.py

from crewai import Agent
from .base_agent import llm

data_product_designer = Agent(
    role='Data Product Designer',
    goal='Design a comprehensive and scalable JSON schema for the customer 360 data product.',
    backstory=(
        "You are a seasoned data architect who specializes in designing robust data products. "
        "Your schemas are legendary for their clarity, scalability, and alignment with business goals."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)