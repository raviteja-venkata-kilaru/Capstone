import pytest
from app import app

BASE_URL = 'http://127.0.0.1:5010/api/calculate_estimation'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_calculate_estimation_return_data(client):
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert len(response.json['history']) > 0

def test_calculate_estimation_no_data(client):
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert 'message' not in response.json.keys()

def test_calculate_estimation_no_data_details(client):
    data = {'Complexity':'High','Size':4,'typeOfTask': 'Integration'}
    response = client.post(BASE_URL, json=data)
    assert 'Manually enter the Estimation and Confidence level' in response.json['message']

def test_calculate_estimation_successful(client):
    data = {'Complexity':'High','Size':"8",'typeOfTask': 'Developing'}
    response = client.post(BASE_URL, json=data)
    assert response.json['estimated_effort'] > 0
    assert response.json['confidence_level'] in ['high','medium','low']