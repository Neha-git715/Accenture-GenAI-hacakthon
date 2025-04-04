from .base_agent import BaseAgent
from typing import Any, Dict, List
from ..models.schemas import DataProduct, CertificationStatus
import ollama
import json

class DataProductValidatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Data Product Validator",
            description="Validates and certifies data products against standards"
        )

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.log_activity("Validating data product")
        
        data_product = input_data.get("data_product", {})
        if not data_product:
            return self.format_response(
                data={},
                status="error",
                message="No data product provided for validation"
            )

        try:
            # Generate validation analysis using Ollama
            prompt = f"""
            As a Banking Data Quality Specialist, validate this data product:
            {json.dumps(data_product, indent=2)}

            Provide JSON validation report with:
            1. Compliance checks (PII handling, data governance)
            2. Data quality assessment
            3. Completeness of mappings
            4. Security considerations
            5. Overall certification recommendation
            """

            response = ollama.generate(
                model='tinyllama',
                prompt=prompt,
                format='json',
                options={'temperature': 0.2}
            )

            validation_results = json.loads(response['response'])
            
            # Determine certification status
            certification_status = CertificationStatus.CERTIFIED
            issues = validation_results.get("issues", [])
            if issues:
                if any(issue.get("severity") == "high" for issue in issues):
                    certification_status = CertificationStatus.FAILED
                else:
                    certification_status = CertificationStatus.IN_PROGRESS

            validation_results["certification_status"] = certification_status

            self.log_activity(f"Validation completed with status: {certification_status}")
            return self.format_response(
                data=validation_results,
                message=f"Data product validation completed with status: {certification_status}"
            )

        except Exception as e:
            self.log_activity(f"Error validating data product: {str(e)}", "error")
            return self.format_response(
                data={},
                status="error",
                message=f"Failed to validate data product: {str(e)}"
            ) 