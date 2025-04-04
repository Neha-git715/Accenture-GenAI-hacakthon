from typing import Dict, Any, List
import ollama
import json
from datetime import datetime
from backend.agents.base_agent import BaseAgent
import logging

class IntelligentOrchestrator:
    def __init__(self):
        self.conversation_history = []
        self.learning_examples = {}
        self.model_context = {
            "successful_patterns": [],
            "failed_patterns": [],
            "domain_rules": {}
        }

    def process_with_memory(self, prompt: str, context: Dict) -> Dict:
        """Process with learning from past interactions"""
        # Enhance prompt with past successful patterns
        enhanced_prompt = self._build_enhanced_prompt(prompt, context)
        
        # Get LLM response
        response = self._get_llm_response(enhanced_prompt)
        
        # Learn from the interaction
        self._update_learning(prompt, response, context)
        
        return response

    def _build_enhanced_prompt(self, prompt: str, context: Dict) -> str:
        """Build enhanced prompt using context and learning"""
        # Add successful patterns as examples
        examples = "\n".join([
            f"Example {i+1}:\n{pattern}"
            for i, pattern in enumerate(self.model_context["successful_patterns"][-3:])
        ])

        # Add domain-specific rules
        rules = "\n".join([
            f"Rule: {rule}"
            for rule in self.model_context["domain_rules"].values()
        ])

        return f"""
        Previous successful patterns:
        {examples}

        Domain rules to consider:
        {rules}

        Current context:
        {json.dumps(context, indent=2)}

        Task:
        {prompt}

        Provide a detailed response following the successful patterns while adhering to domain rules.
        """

    def _get_llm_response(self, prompt: str) -> Dict:
        """Get enhanced LLM response"""
        try:
            response = ollama.generate(
                model='tinyllama',  # Using mistral for better JSON handling
                prompt=prompt,
                format='json',
                options={
                    'temperature': 0.1,  # Lower temperature for more focused responses
                    'top_p': 0.5,  # Lower top_p for faster sampling
                    'context_window': 2048,  # Reduced context window
                    'num_predict': 500,  # Reduced token prediction
                    'num_ctx': 1024,  # Reduced context size
                    'num_thread': 4  # Using more threads for faster processing
                }
            )
            
            # Extract raw response
            raw_response = response.get('response', '').strip()
            
            # Log the raw response for debugging
            logging.debug(f"Raw response: {raw_response}")
            
            # Check if the response seems like valid JSON
            if not raw_response.startswith("{") or not raw_response.endswith("}"):
                raise Exception(f"Response doesn't seem like valid JSON: {raw_response}")
            
            # Attempt to parse JSON
            return json.loads(raw_response)

        except json.JSONDecodeError as e:
            logging.error(f"JSON Decode Error: {str(e)}")
            logging.error(f"Response content: {raw_response}")
            raise Exception(f"LLM processing failed due to JSON decoding error: {str(e)}")
        except Exception as e:
            logging.error(f"LLM processing failed: {str(e)}")
            raise Exception(f"LLM processing failed: {str(e)}")

    def _update_learning(self, prompt: str, response: Dict, context: Dict):
        """Update learning from interaction"""
        # Store interaction in history
        self.conversation_history.append({
            "prompt": prompt,
            "response": response,
            "context": context,
            "timestamp": datetime.now().isoformat()
        })

        # Update successful patterns if response was good
        if self._is_response_successful(response):
            self.model_context["successful_patterns"].append({
                "prompt": prompt,
                "response_structure": self._extract_structure(response)
            })

    def _is_response_successful(self, response: Dict) -> bool:
        """Determine if response was successful"""
        # Check for required elements
        required_elements = ["entities", "attributes", "relationships"]
        has_required = all(elem in response for elem in required_elements)

        # Check for data quality
        quality_score = self._calculate_quality_score(response)
        
        return has_required and quality_score > 0.8

    def _calculate_quality_score(self, response: Dict) -> float:
        """Calculate quality score of response"""
        score = 0.0
        checks = [
            self._check_completeness(response),
            self._check_consistency(response),
            self._check_validity(response)
        ]
        return sum(checks) / len(checks)

    def _check_completeness(self, response: Dict) -> float:
        """Check if response has all required fields"""
        required_fields = ["entities", "attributes", "relationships"]
        return len([f for f in required_fields if f in response]) / len(required_fields)

    def _check_consistency(self, response: Dict) -> float:
        """Check internal consistency of response"""
        return 1.0  # Simplified for now

    def _check_validity(self, response: Dict) -> float:
        """Check validity of response data"""
        return 1.0  # Simplified for now

    def _extract_structure(self, response: Dict) -> Dict:
        """Extract structural patterns from response"""
        return {
            "entity_patterns": self._find_patterns(response.get("entities", [])),
            "attribute_patterns": self._find_patterns(response.get("attributes", [])),
            "relationship_patterns": self._find_patterns(response.get("relationships", []))
        }

    def _find_patterns(self, items: List) -> List[str]:
        """Find common patterns in successful responses"""
        patterns = []
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    pattern = {k: type(v).__name__ for k, v in item.items()}
                    patterns.append(str(pattern))
        return list(set(patterns))

    def add_domain_rule(self, rule_name: str, rule_definition: str):
        """Add new domain-specific rule"""
        self.model_context["domain_rules"][rule_name] = rule_definition

    def get_learning_statistics(self) -> Dict:
        """Get statistics about learning progress"""
        return {
            "total_interactions": len(self.conversation_history),
            "successful_patterns": len(self.model_context["successful_patterns"]),
            "domain_rules": len(self.model_context["domain_rules"]),
            "average_quality_score": sum(
                self._calculate_quality_score(interaction["response"])
                for interaction in self.conversation_history[-10:]
            ) / min(10, len(self.conversation_history)) if self.conversation_history else 0
        } 
