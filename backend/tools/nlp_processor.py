from typing import Dict, List, Any
import spacy
import re

class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def extract_key_entities(self, text: str) -> List[str]:
        """Extract key entities from text"""
        doc = self.nlp(text)
        return [ent.text for ent in doc.ents]
    
    def extract_data_requirements(self, text: str) -> Dict[str, List[str]]:
        """Extract data-related requirements from text"""
        doc = self.nlp(text)
        
        requirements = {
            "entities": [],
            "attributes": [],
            "relationships": [],
            "constraints": []
        }
        
        # Simple pattern matching for common data requirements
        entity_patterns = r"(?i)(customer|account|transaction|product|service)"
        attribute_patterns = r"(?i)(name|id|number|date|amount|status|type)"
        relationship_patterns = r"(?i)(has|owns|belongs to|related to|linked with)"
        constraint_patterns = r"(?i)(required|unique|mandatory|optional|must have)"
        
        for sent in doc.sents:
            sent_text = sent.text.lower()
            
            # Extract entities
            entities = re.findall(entity_patterns, sent_text)
            requirements["entities"].extend(entities)
            
            # Extract attributes
            attributes = re.findall(attribute_patterns, sent_text)
            requirements["attributes"].extend(attributes)
            
            # Extract relationships
            relationships = re.findall(relationship_patterns, sent_text)
            requirements["relationships"].extend(relationships)
            
            # Extract constraints
            constraints = re.findall(constraint_patterns, sent_text)
            requirements["constraints"].extend(constraints)
        
        # Remove duplicates and clean up
        for key in requirements:
            requirements[key] = list(set(requirements[key]))
            
        return requirements
    
    def identify_pii_elements(self, text: str) -> List[str]:
        """Identify potential PII elements in text"""
        pii_patterns = [
            r"(?i)(name|address|email|phone|ssn|social security|birth date|passport)",
            r"(?i)(credit card|account number|license number)",
            r"(?i)(personal|private|sensitive|confidential)"
        ]
        
        pii_elements = []
        for pattern in pii_patterns:
            matches = re.findall(pattern, text)
            pii_elements.extend(matches)
            
        return list(set(pii_elements))
    
    def suggest_refresh_frequency(self, text: str) -> str:
        """Suggest data refresh frequency based on requirements"""
        doc = self.nlp(text.lower())
        
        # Keywords indicating different refresh frequencies
        realtime_keywords = ["real-time", "realtime", "immediate", "instant"]
        daily_keywords = ["daily", "day", "24 hours"]
        weekly_keywords = ["weekly", "week"]
        monthly_keywords = ["monthly", "month"]
        
        text_lower = text.lower()
        
        for keyword in realtime_keywords:
            if keyword in text_lower:
                return "real-time"
                
        for keyword in daily_keywords:
            if keyword in text_lower:
                return "daily"
                
        for keyword in weekly_keywords:
            if keyword in text_lower:
                return "weekly"
                
        for keyword in monthly_keywords:
            if keyword in text_lower:
                return "monthly"
                
        # Default to daily if no specific frequency is mentioned
        return "daily" 