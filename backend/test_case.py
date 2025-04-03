import json
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.intelligent_orchestrator import IntelligentOrchestrator
from backend.agents.use_case_interpreter import UseCaseInterpreterAgent
from backend.agents.data_product_designer import DataProductDesignerAgent
from backend.agents.source_system_mapper import SourceSystemMapperAgent
from backend.agents.data_product_validator import DataProductValidatorAgent
from backend.tools.schema_matcher import SchemaMatcherAI

def run_test():
    # Initialize components
    orchestrator = IntelligentOrchestrator()
    use_case_agent = UseCaseInterpreterAgent()
    designer_agent = DataProductDesignerAgent()
    mapper_agent = SourceSystemMapperAgent()
    validator_agent = DataProductValidatorAgent()
    schema_matcher = SchemaMatcherAI()

    # Test use case
    use_case = """
    We need a Customer 360 data product for our retail banking division that will:
    1. Provide a complete view of customer information including personal details, accounts, and transactions
    2. Include real-time account balances and transaction history
    3. Track customer interactions across channels (mobile, web, branch)
    4. Monitor product holdings and identify cross-sell opportunities
    5. Ensure compliance with data privacy regulations for PII data
    """

    print("\n1. Analyzing use case...")
    analysis = orchestrator.process_with_memory(
        prompt=use_case,
        context={"domain": "retail_banking", "priority": "high"}
    )
    print(json.dumps(analysis, indent=2))

    print("\n2. Extracting requirements...")
    requirements = use_case_agent.process({
        "use_case": use_case,
        "initial_analysis": analysis
    })
    print(json.dumps(requirements, indent=2))

    print("\n3. Designing data product...")
    design = designer_agent.process({
        "requirements": requirements
    })
    print(json.dumps(design, indent=2))

    # Example source systems
    source_systems = [
        {
            "name": "core_banking",
            "entities": ["customer", "account", "transaction"],
            "type": "oracle"
        },
        {
            "name": "crm",
            "entities": ["customer", "interaction", "product"],
            "type": "salesforce"
        }
    ]

    print("\n4. Creating source mappings...")
    mappings = mapper_agent.process({
        "data_product_id": "cust360_v1",
        "source_systems": source_systems
    })
    
    enhanced_mappings = schema_matcher.match_schemas(
        source_schema=mappings["source_schema"],
        target_schema=mappings["target_schema"]
    )
    print(json.dumps(enhanced_mappings, indent=2))

    print("\n5. Validating data product...")
    validation = validator_agent.process({
        "data_product": {
            "design": design,
            "mappings": enhanced_mappings
        }
    })
    print(json.dumps(validation, indent=2))

    print("\n6. Learning statistics:")
    stats = orchestrator.get_learning_statistics()
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    run_test() 