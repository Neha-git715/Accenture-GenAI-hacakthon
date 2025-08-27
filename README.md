# BankGen360 🏦

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Framework](https://img.shields.io/badge/Framework-CrewAI-orange?style=for-the-badge)
![Frontend](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

An AI-powered multi-agent system that automates the design of Customer 360° data products for the retail banking sector. This project was developed as a submission for an **Accenture GenAI Hackathon**.

## 🚀 Overview

In the banking industry, creating a new data product—like a system to identify customers for a new loan offer—is a slow, manual process. Data teams spend weeks understanding business needs, designing data schemas, and mapping data sources.

**BankGen360** solves this by using a crew of specialized AI agents. You provide a simple business problem, and the autonomous agents work together like an assembly line to produce a complete technical design document in minutes, not weeks.

## ✨ Features

-   **Automated Requirement Analysis:** An AI agent interprets the business problem and extracts the core objectives.
-   **Dynamic Schema Generation:** A Data Architect agent designs a robust JSON schema for the final data product.
-   **Intelligent Source Mapping:** A mapping specialist agent identifies the likely source systems (e.g., CRM, Core Banking) for each data field.
-   **Final Design Validation:** A QA agent reviews all artifacts for consistency and alignment with the initial goal.
-   **Interactive Web UI:** A user-friendly interface built with Streamlit to input use cases and view the generated results.

## 🛠️ System Architecture

The project uses **CrewAI** to orchestrate a sequential workflow of AI agents. The output from one agent serves as the context for the next, ensuring a cohesive and logical process from start to finish.

```
 Business Use Case (Input)
         |
         v
 [🤖 Business Analyst Agent] --> Analyzes requirements
         |
         v
 [🤖 Data Product Designer Agent] --> Creates JSON Schema
         |
         v
 [🤖 Source System Mapper Agent] --> Maps data sources
         |
         v
 [🤖 Data Product Validator Agent] --> Reviews & Compiles
         |
         v
 Final Design Document (Output)
```

## 💻 Tech Stack

-   **AI Framework:** CrewAI
-   **LLM:** Google Gemini 1.5 Flash (via API)
-   **LLM Connector:** LangChain Community (`ChatLiteLLM`)
-   **Frontend:** Streamlit
-   **Backend:** FastAPI & Uvicorn
-   **Language:** Python 3.11

## ⚙️ Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone [https://github.com/Neha-git715/Accenture-GenAI-hacakthon.git](https://github.com/Neha-git715/Accenture-GenAI-hacakthon.git)
cd Accenture-GenAI-hacakthon
```

### 2. Create and Activate a Virtual Environment

It's recommended to use a virtual environment.

```bash
# Create the environment
py -3.11 -m venv .venv

# Activate the environment (on Windows)
.\.venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Set Up Your API Key

The project uses the Google Gemini API, which has a generous free tier.

1.  Create a file named `.env` in the root of the project folder.
2.  Get your free API key from **[Google AI Studio](https://aistudio.google.com/app/apikeys)**.
3.  Add your key to the `.env` file like this:

    ```
    # Inside your .env file
    GOOGLE_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxx"
    ```

## ▶️ How to Run

Once the setup is complete, run the Streamlit application from your terminal:

```bash
streamlit run app.py
```

Your web browser will open to the application's UI. Enter a business use case and click the "Generate" button to start the AI crew!

## 📸 Demo

*(Consider recording a short GIF of the app working and adding it here!)*

![BankGen360 Demo GIF](placeholder-for-your-demo.gif)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
