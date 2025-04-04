from typing import Dict, List, Any
import ollama
import json
import numpy as np
from difflib import SequenceMatcher

class SchemaMatcherAI:
    def __init__(self):
        self.similarity_threshold = 0.7
        self.context_window = []
        self.successful_matches = {}

    def match_schemas(self, source_schema: Dict, target_schema: Dict) -> Dict[str, Any]:
        """Match source schema to target schema using AI"""
        try:
            # Prepare context from previous successful matches
            context = self._prepare_matching_context(source_schema, target_schema)
            
            # Generate AI-based matching suggestions
            prompt = f"""
            As a Data Schema Matching Expert, analyze and create mappings between:

            Source Schema:
            {json.dumps(source_schema, indent=2)}

            Target Schema:
            {json.dumps(target_schema, indent=2)}

            Previous successful matches:
            {json.dumps(context, indent=2)}

            Provide JSON with:
            1. Direct matches (exact or high confidence)
            2. Transformation suggestions for partial matches
            3. Confidence scores for each match
            4. Required data quality checks
            """

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

            ai_suggestions = json.loads(response['response'])
            
            # Enhance AI suggestions with similarity metrics
            enhanced_matches = self._enhance_matches(
                ai_suggestions,
                source_schema,
                target_schema
            )

            # Learn from this matching session
            self._update_learning(enhanced_matches)

            return enhanced_matches

        except Exception as e:
            raise Exception(f"Schema matching failed: {str(e)}")

    def _prepare_matching_context(self, source: Dict, target: Dict) -> Dict:
        """Prepare context from previous successful matches"""
        relevant_matches = {}
        
        # Find similar schemas from history
        for schema_pair, matches in self.successful_matches.items():
            source_similarity = self._calculate_schema_similarity(
                source,
                json.loads(schema_pair.split("||")[0])
            )
            target_similarity = self._calculate_schema_similarity(
                target,
                json.loads(schema_pair.split("||")[1])
            )
            
            if source_similarity > 0.6 and target_similarity > 0.6:
                relevant_matches[schema_pair] = matches

        return {
            "similar_cases": relevant_matches,
            "common_patterns": self._extract_common_patterns(relevant_matches)
        }

    def _enhance_matches(self, ai_matches: Dict, source: Dict, target: Dict) -> Dict:
        """Enhance AI matches with similarity metrics"""
        enhanced = {
            "direct_matches": [],
            "transformation_matches": [],
            "unmatched_source": [],
            "unmatched_target": []
        }

        # Process direct matches
        for match in ai_matches.get("direct_matches", []):
            similarity = self._calculate_field_similarity(
                match["source_field"],
                match["target_field"]
            )
            match["similarity_score"] = similarity
            match["confidence_score"] = (similarity + match.get("ai_confidence", 0.5)) / 2
            
            if match["confidence_score"] >= self.similarity_threshold:
                enhanced["direct_matches"].append(match)
            else:
                enhanced["transformation_matches"].append(match)

        # Process transformation matches
        for match in ai_matches.get("transformation_matches", []):
            match["transformation_complexity"] = self._calculate_transformation_complexity(
                match["transformation_rule"]
            )
            enhanced["transformation_matches"].append(match)

        # Find unmatched fields
        matched_source_fields = {m["source_field"] for m in enhanced["direct_matches"]}
        matched_target_fields = {m["target_field"] for m in enhanced["direct_matches"]}
        
        enhanced["unmatched_source"] = [
            field for field in source.keys()
            if field not in matched_source_fields
        ]
        enhanced["unmatched_target"] = [
            field for field in target.keys()
            if field not in matched_target_fields
        ]

        return enhanced

    def _calculate_field_similarity(self, source_field: str, target_field: str) -> float:
        """Calculate similarity between two fields"""
        # Name similarity
        name_similarity = SequenceMatcher(None, source_field, target_field).ratio()
        
        # Type similarity (if available)
        type_similarity = 1.0  # Implement type comparison logic
        
        # Weighted average
        return 0.7 * name_similarity + 0.3 * type_similarity

    def _calculate_transformation_complexity(self, transformation: str) -> float:
        """Calculate complexity of transformation rule"""
        # Simple heuristic based on transformation length and operations
        operations = ["split", "concat", "substring", "replace", "cast"]
        complexity = len(transformation) / 100  # Base complexity
        
        for op in operations:
            if op in transformation.lower():
                complexity += 0.1  # Increase complexity for each operation
                
        return min(complexity, 1.0)

    def _calculate_schema_similarity(self, schema1: Dict, schema2: Dict) -> float:
        """Calculate overall similarity between two schemas"""
        common_fields = set(schema1.keys()) & set(schema2.keys())
        total_fields = set(schema1.keys()) | set(schema2.keys())
        
        if not total_fields:
            return 0.0
            
        return len(common_fields) / len(total_fields)

    def _extract_common_patterns(self, matches: Dict) -> List[Dict]:
        """Extract common matching patterns from successful matches"""
        patterns = []
        
        # Analyze patterns in successful matches
        for schema_pair, match_results in matches.items():
            for match in match_results.get("direct_matches", []):
                pattern = {
                    "source_pattern": self._extract_field_pattern(match["source_field"]),
                    "target_pattern": self._extract_field_pattern(match["target_field"]),
                    "frequency": 1
                }
                
                # Update pattern frequency
                existing = next(
                    (p for p in patterns 
                     if p["source_pattern"] == pattern["source_pattern"]
                     and p["target_pattern"] == pattern["target_pattern"]),
                    None
                )
                
                if existing:
                    existing["frequency"] += 1
                else:
                    patterns.append(pattern)
        
        return sorted(patterns, key=lambda x: x["frequency"], reverse=True)

    def _extract_field_pattern(self, field_name: str) -> str:
        """Extract pattern from field name"""
        # Implement pattern extraction logic
        # Example: "customer_id" -> "{entity}_id"
        return field_name  # Placeholder

    def _update_learning(self, matches: Dict):
        """Update learning from successful matches"""
        if matches.get("direct_matches"):
            schema_pair = f"{json.dumps(matches['source_schema'])}||{json.dumps(matches['target_schema'])}"
            self.successful_matches[schema_pair] = matches
            
            # Keep only recent history
            if len(self.successful_matches) > 100:
                oldest_key = min(self.successful_matches.keys())
                del self.successful_matches[oldest_key] 