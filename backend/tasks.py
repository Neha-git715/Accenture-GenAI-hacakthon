# In backend/tasks.py

from crewai import Task

# Task 1: Analyze the business problem for the use_case_interpreter agent
analysis_task = Task(
    description=(
        "Analyze the provided business use case: '{use_case}'. "
        "Distill the core business objectives, identify the target customer profile, "
        "and determine the key questions the data product needs to answer. "
        "Your final output should be a concise summary of these findings."
    ),
    expected_output=(
        "A detailed summary report including: \n"
        "1. Core Business Objective.\n"
        "2. Target Customer Profile.\n"
        "3. Key questions to be answered by the data."
    ),
    agent=None # The agent will be assigned in the main application script
)

# Task 2: Design the data product schema for the data_product_designer agent
design_task = Task(
    description=(
        "Based on the business analysis report, design a detailed and scalable JSON schema "
        "for the customer 360 data product. The schema must be well-structured with clear field names, "
        "appropriate data types (e.g., string, integer, boolean, array), and include example values."
    ),
    expected_output=(
        "A complete JSON object that represents the schema for the new data product. "
        "The JSON must be properly formatted and enclosed in a single markdown code block."
    ),
    context=[analysis_task], # This task depends on the output of the analysis_task
    agent=None
)

# Task 3: Map source systems for the source_system_mapper agent
mapping_task = Task(
    description=(
        "Using the designed JSON schema, identify the most likely source systems within a typical retail bank "
        "for each field. Create a clear mapping document that lists each target field from the schema, its description, "
        "and its corresponding source system and source field name (e.g., 'Core Banking Platform', 'CRM', 'Loan Origination System')."
    ),
    expected_output=(
        "A markdown table mapping each target field to its source system and source attribute. "
        "The table should have the columns: | Target Field | Description | Source System | Source Field |"
    ),
    context=[design_task], # This task depends on the output of the design_task
    agent=None
)

# Task 4: Validate the final design for the data_product_validator agent
validation_task = Task(
    description=(
        "Review the business analysis, the JSON schema, and the source system mapping. "
        "Ensure there is perfect alignment between the original business use case and the technical artifacts. "
        "Compile all artifacts into a single, cohesive design document. "
        "Provide a final verdict on whether the design is approved or requires revision, with justifications."
    ),
    expected_output=(
        "A final, polished design document in markdown format. It must include:\n"
        "1. Executive Summary (based on the original use case).\n"
        "2. The full JSON Schema.\n"
        "3. The Source-to-Target Mapping Table.\n"
        "4. A final 'Validation Verdict' section with an 'Approved' status and a brief justification."
    ),
    context=[analysis_task, design_task, mapping_task], # This task uses the output of all previous tasks
    agent=None
)