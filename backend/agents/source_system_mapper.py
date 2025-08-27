# from typing import Dict, Any, List
# import ollama
# import json
# from backend.agents.base_agent import BaseAgent
# from backend.models.schemas import AttributeMapping, SourceSystem

# class SourceSystemMapperAgent(BaseAgent):
#     def __init__(self):
#         super().__init__(
#             name="Source System Mapper",
#             description="Maps source system attributes to data product attributes"
#         )

#     def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
#         self.log_activity("Creating source system mappings")
        
#         data_product_id = input_data.get("data_product_id", "")
#         source_systems = input_data.get("source_systems", [])

#         if not data_product_id or not source_systems:
#             return self.format_response(
#                 data={},
#                 status="error",
#                 message="Missing data product ID or source systems"
#             )

#         try:
#             # Generate source system schemas
#             source_schema = self._generate_source_schema(source_systems)
#             target_schema = self._generate_target_schema(data_product_id)

#             # Generate mappings using Ollama
#             prompt = f"""
#             As a Banking Data Integration Specialist, create mappings between these schemas:

#             Source Systems:
#             {json.dumps(source_schema, indent=2)}
            
#             Target Schema:
#             {json.dumps(target_schema, indent=2)}

#             Provide a valid JSON mapping with these exact fields:
#             {{
#                 "mappings": [
#                     {{
#                         "source_system": "string",
#                         "source_entity": "string",
#                         "source_attribute": "string",
#                         "target_entity": "string",
#                         "target_attribute": "string",
#                         "transformation_rule": "string",
#                         "data_quality_checks": ["string"]
#                     }}
#                 ],
#                 "unmapped_sources": ["string"],
#                 "unmapped_targets": ["string"]
#             }}

#             Ensure all JSON is properly formatted with no trailing commas.
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
            
#             mappings_dict = json.loads(json_str)
            
#             result = {
#                 "source_schema": source_schema,
#                 "target_schema": target_schema,
#                 "mappings": mappings_dict.get("mappings", []),
#                 "unmapped_sources": mappings_dict.get("unmapped_sources", []),
#                 "unmapped_targets": mappings_dict.get("unmapped_targets", [])
#             }

#             self.log_activity("Successfully created source mappings")
#             return self.format_response(
#                 data=result,
#                 message="Source system mapping completed"
#             )

#         except json.JSONDecodeError as e:
#             self.log_activity(f"JSON parsing error: {str(e)}", "error")
#             return self.format_response(
#                 data={},
#                 status="error",
#                 message=f"Failed to parse JSON response: {str(e)}"
#             )
#         except Exception as e:
#             self.log_activity(f"Error creating mappings: {str(e)}", "error")
#             return self.format_response(
#                 data={},
#                 status="error",
#                 message=f"Failed to create mappings: {str(e)}"
#             )

#     def _generate_source_schema(self, source_systems: List[Dict]) -> Dict:
#         """Generate schema for source systems"""
#         schema = {}
#         for system in source_systems:
#             schema[system["name"]] = {
#                 "type": system.get("type", "unknown"),
#                 "entities": {}
#             }
#             for entity in system.get("entities", []):
#                 schema[system["name"]]["entities"][entity] = {
#                     "attributes": self._generate_sample_attributes(entity)
#                 }
#         return schema

#     def _generate_target_schema(self, data_product_id: str) -> Dict:
#         """Generate target schema based on data product ID"""
#         # This would typically come from a database or configuration
#         # For now, we'll generate a sample schema
#         return {
#             "customer": {
#                 "attributes": {
#                     "customer_id": {"type": "string", "is_pii": False},
#                     "full_name": {"type": "string", "is_pii": True},
#                     "email": {"type": "string", "is_pii": True},
#                     "phone": {"type": "string", "is_pii": True}
#                 }
#             },
#             "account": {
#                 "attributes": {
#                     "account_id": {"type": "string", "is_pii": False},
#                     "customer_id": {"type": "string", "is_pii": False},
#                     "account_type": {"type": "string", "is_pii": False},
#                     "balance": {"type": "decimal", "is_pii": True}
#                 }
#             },
#             "transaction": {
#                 "attributes": {
#                     "transaction_id": {"type": "string", "is_pii": False},
#                     "account_id": {"type": "string", "is_pii": False},
#                     "amount": {"type": "decimal", "is_pii": True},
#                     "timestamp": {"type": "datetime", "is_pii": False}
#                 }
#             }
#         }

#     def _generate_sample_attributes(self, entity: str) -> Dict:
#         """Generate sample attributes for an entity"""
#         common_attributes = {
#             "id": {"type": "string", "is_pii": False},
#             "created_at": {"type": "datetime", "is_pii": False},
#             "updated_at": {"type": "datetime", "is_pii": False}
#         }
        
#         entity_specific = {
#             "customer": {
#                 "name": {"type": "string", "is_pii": True},
#                 "email": {"type": "string", "is_pii": True}
#             },
#             "account": {
#                 "number": {"type": "string", "is_pii": True},
#                 "type": {"type": "string", "is_pii": False}
#             },
#             "transaction": {
#                 "amount": {"type": "decimal", "is_pii": True},
#                 "type": {"type": "string", "is_pii": False}
#             }
#         }
        
#         return {**common_attributes, **entity_specific.get(entity, {})} 



# In backend/agents/source_system_mapper.py

from crewai import Agent
from .base_agent import llm

source_system_mapper = Agent(
    role='Source System Mapping Specialist',
    goal='Identify the source systems and specific attributes required for the data product and generate a mapping file.',
    backstory=(
        "You have an encyclopedic knowledge of a typical retail bank's IT landscape. You know exactly "
        "which system holds which piece of customer data, from the core banking platform to the CRM."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)