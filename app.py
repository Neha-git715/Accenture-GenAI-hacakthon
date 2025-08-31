import streamlit as st
from crewai import Crew, Process

# Import your agents and tasks from the backend
# This works because of the __init__.py files you created
from backend.agents import (
    use_case_interpreter,
    data_product_designer,
    source_system_mapper,
    data_product_validator
)
from backend.tasks import (
    analysis_task,
    design_task,
    mapping_task,
    validation_task
)

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="BankGen360", page_icon="🏦", layout="wide")

st.title("🏦 BankGen360: AI-Powered Customer Data Product Design")
st.markdown("""
Welcome to BankGen360! This tool uses a team of AI agents to automate the design of a 360-degree customer view.
Enter a business problem below, and the AI crew will generate a full data product design for you.
""")

st.subheader("Enter Your Business Use Case")
use_case = st.text_area(
    "For example: 'Design a data product to identify customers who are at high risk of churning in the next 3 months.'",
    height=150
)

# --- Crew Execution Logic ---
if st.button("🚀 Generate Data Product Design", type="primary"):
    if not use_case:
        st.error("Please enter a business use case to proceed.")
    else:
        with st.spinner("🤖 The AI Crew is on the job... This may take a few minutes..."):
            try:
                # Dynamically assign agents to their respective tasks
                analysis_task.agent = use_case_interpreter
                design_task.agent = data_product_designer
                mapping_task.agent = source_system_mapper
                validation_task.agent = data_product_validator

                # Assemble the crew with a sequential process
                bank_crew = Crew(
                    agents=[
                        use_case_interpreter,
                        data_product_designer,
                        source_system_mapper,
                        data_product_validator
                    ],
                    tasks=[
                        analysis_task,
                        design_task,
                        mapping_task,
                        validation_task
                    ],
                    process=Process.sequential,
                    verbose=True  # Shows detailed logs of the crew's work
                )

                # Prepare the inputs for the kickoff
                inputs = {'use_case': use_case}

                # Kick off the crew's work
                final_result = bank_crew.kickoff(inputs=inputs)

                st.success("🎉 Crew finished the job! Here is the final design document:")
                st.markdown(final_result)

            except Exception as e:
                st.error(f"An error occurred during the crew's execution: {e}")
