# BankGen 360 - Retail Banking Data Product

## Overview
This project implements a multi-agent system for designing and recommending BankGen 360 data products in retail banking. The system automates the process of understanding business requirements, designing data structures, and creating attribute mappings.

### Solution Overview
This project implements a multi-agent system for designing and recommending Customer 360 data products in retail banking. The system automates the process of understanding business requirements, designing data structures, and creating attribute mappings.

### System Components
1. **Use Case Interpreter Agent**
   - Analyzes business requirements
   - Extracts key data requirements
   - Identifies customer data attributes needed

2. **Data Product Designer Agent**
   - Recommends optimal data product structure
   - Defines schema and relationships
   - Ensures compliance with data standards

3. **Source System Mapper Agent**
   - Identifies relevant source systems
   - Maps source attributes to target schema
   - Handles data transformation rules

4. **Data Product Validator Agent**
   - Validates data product design
   - Ensures PII compliance
   - Certifies data product against standards

### Key Features
- Natural language processing for requirement analysis
- Automated schema design and recommendation
- Source system attribute mapping
- Data product certification
- PII and compliance handling

### Technical Architecture
- FastAPI-based microservices
- SQL and NoSQL database support
- Secure API endpoints for agent communication
- Data governance integration

### Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables
3. Run the application: `python app.py`

### API Documentation
Access the API documentation at `/docs` endpoint after starting the server.