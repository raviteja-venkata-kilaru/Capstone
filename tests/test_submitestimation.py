import pytest
import requests

BASE_URL = 'http://127.0.0.1:5010/api/submit_estimation'

@pytest.fixture
def submit_estimation_url():
    return BASE_URL

def test_submit_estimation_successful(submit_estimation_url):
    data = {'Task': 'New Task', 'Complexity': 'High', 'Size': '8', 'typeOfTask': 'Integration', 'Note': 'Test comment','Estimation': '101','Confidence': 'Low'}
    response = requests.post(submit_estimation_url, json=data)
    assert response.status_code == 200

