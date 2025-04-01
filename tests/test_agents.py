import pytest
from agents.validator import BankingValidator
from agents.interpreter import BankingInterpreter
import pandas as pd

def test_aml_detection():
    test_data = pd.DataFrame({
        'Transaction_ID': ['TX1', 'TX2'],
        'Amount': [15000, 500],
        'Date': ['2023-01-01', '2023-01-01 00:10:00']
    })
    risks = BankingValidator.detect_aml_risks(test_data)
    assert 'TX1' in risks['high_risk']

def test_sql_injection_block():
    interpreter = BankingInterpreter()
    result = interpreter.generate_sql("DELETE FROM customers")
    assert "Dangerous SQL" in result["error"]