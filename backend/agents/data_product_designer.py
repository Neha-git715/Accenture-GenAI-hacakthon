

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