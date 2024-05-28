import pytest
from app import app

BASE_URL = 'http://127.0.0.1:5010/api/submit_estimation'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_submit_estimation_successful(client):
    data = {'Task': 'New Task', 'Complexity': 'High', 'Size': '8', 'typeOfTask': 'Integration', 'Note': 'Test comment','Estimation': '8','Confidence': 'medium'}
    response = client.post(BASE_URL, json=data)
    assert response.status_code == 201

