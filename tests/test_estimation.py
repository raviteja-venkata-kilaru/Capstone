import pytest
import requests
from app import app

BASE_URL = 'http://127.0.0.1:5010/api/calculate_estimation'

@pytest.fixture
def register_url():
    return BASE_URL

@pytest.fixture
def client():
    return app.test_client()


def test_calculate_estimation_return_data(register_url,client):
    response = client.get(register_url)
    assert response.status_code == 200
    assert len(response.json['history']) > 0

def test_calculate_estimation_no_data(register_url,client):
    response = client.get(register_url)
    assert response.status_code == 200
    assert response.json['message'] == 'There is No data In database to Search'

def test_calculate_estimation_no_data_details(register_url):
    data = {'complexity':'High','size':4,'type': 'Developing'}
    response = requests.post(register_url, json=data)
    assert response.json['message'] == 'There is no data in database please add Estimation and confidence'

def test_calculate_estimation_successful(register_url):
    data = {'complexity':'High','size':4,'type': 'Developing'}
    response = requests.post(register_url, json=data)
    assert response.json['estimated_effort'] > 0
    assert response.json['confidence_level'] in ['high','medium','low']