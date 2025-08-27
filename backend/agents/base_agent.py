# In backend/agents/base_agent.py

import os
from dotenv import load_dotenv
# NEW: Import a more generic LLM connector from langchain-community
from langchain_community.chat_models.litellm import ChatLiteLLM

# Load environment variables from your .env file
load_dotenv()

# Check for the Google API Key (this part is still good practice)
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError(
        "Google API key not found. Please make sure you have a GOOGLE_API_KEY in your .env file"
    )

# NEW: Initialize the LLM using ChatLiteLLM
# This passes the model name directly in the format the docs recommend.
llm = ChatLiteLLM(
    model="gemini/gemini-1.5-flash",
    # api_key=os.environ["GOOGLE_API_KEY"],
    verbose=True,
    temperature=0.5
)