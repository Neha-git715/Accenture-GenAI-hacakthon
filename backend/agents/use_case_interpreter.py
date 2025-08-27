# from typing import Dict, Any
# import ollama
# import json
# from backend.agents.base_agent import BaseAgent

# class UseCaseInterpreterAgent(BaseAgent):
#     def __init__(self):
#         super().__init__(
#             name="UseCase Interpreter",
#             description="Analyzes business requirements and extracts data requirements"
#         )

#     def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
#         self.log_activity("Processing use case requirements")
        
#         use_case = input_data.get("use_case", "")
#         if not use_case:
#             return self.format_response(
#                 data={},
#                 status="error",
#                 message="No use case provided"
#             )

#         try:
#             # Generate structured analysis using Ollama
#             prompt = f"""
#             As a Banking Data Requirements Analyst, analyze this use case:
#             {use_case}

#             Extract and provide in JSON format:
#             1. Key business objectives
#             2. Required customer data attributes
#             3. Data sensitivity considerations (PII, etc.)
#             4. Recommended refresh frequency
#             5. Data quality requirements
#             """

#             response = ollama.generate(
#                 model='tinyllama',  # Using tinyllama for faster responses
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

#             analysis = json.loads(response['response'])
            
#             self.log_activity("Successfully analyzed use case requirements")
#             return self.format_response(
#                 data=analysis,
#                 message="Use case analysis completed"
#             )

#         except Exception as e:
#             self.log_activity(f"Error analyzing use case: {str(e)}", "error")
#             return self.format_response(
#                 data={},
#                 status="error",
#                 message=f"Failed to analyze use case: {str(e)}"
#             ) 


# In backend/agents/use_case_interpreter.py

from crewai import Agent
from .base_agent import llm # Note the '.' for relative import

use_case_interpreter = Agent(
    role='Business Problem Analyst',
    goal='Clearly understand and articulate the business problem for designing a 360-degree customer data product.',
    backstory=(
        "You are an expert business analyst with a knack for distilling complex business needs "
        "into clear, actionable requirements for data engineering teams."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)