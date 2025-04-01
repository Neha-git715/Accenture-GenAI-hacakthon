import requests
import json

def test_analyze_requirements():
    url = "http://localhost:8000/analyze-requirements"
    
    # Sample use case in request body
    payload = {
        "use_case_description": "Create a Customer 360 view for retail banking customers to enable personalized marketing and risk assessment. The view should include customer demographics, account information, transaction history, and interaction data from various channels."
    }
    
    # Make the request with JSON body
    response = requests.post(url, json=payload)
    
    # Print the response
    print("\n=== Use Case Analysis Results ===\n")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_analyze_requirements() 