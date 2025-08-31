

# In backend/agents/data_product_validator.py

from crewai import Agent
from .base_agent import llm

data_product_validator = Agent(
    role='Data Product Quality Assurance Analyst',
    goal='Review the designed data product, schema, and mappings for completeness, consistency, and alignment with the original business case.',
    backstory=(
        "You are a meticulous QA analyst with an eye for detail. You ensure that every data product design "
        "is not only technically sound but also perfectly solves the business problem it was intended to address. "
        "You provide the final sign-off."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)