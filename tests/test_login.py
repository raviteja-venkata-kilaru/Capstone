import pytest
from app import app

BASE_URL = 'http://127.0.0.1:5010/'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login_successful(client):
    data = {'email': 'new_user@example.com', 'password':'Raviteja@132'}
    response = client.post(BASE_URL, json=data)
    assert response.status_code == 200
    assert 'Successfully Login' in response.json['message']

def test_invalid_user(client):
    data = {'email': 'new_user3@example.com', 'password':'Raviteja@132'}
    response = client.post(BASE_URL, json=data)
    assert 'Invalid email or password' in response.json['error']

def test_login_incomplete_user(client):
    data = {'email': 'new_user@example.com', 'password':''}
    response = client.post(BASE_URL, json=data)
    assert 'Please enter Email or Password' in response.json['error']