import pytest
from app import app

BASE_URL = 'http://127.0.0.1:5010/api/forget_password'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_forget_successful(client):
    data = {'email': 'new_user@example.com','password':'Raviteja@132'}
    response = client.patch(BASE_URL, json=data)
    assert response.status_code == 200
    assert 'Successfully Reseted the password' in response.json['message']

def test_invalid_user(client):
    data = {'email': 'new_user5@example.com'}
    response = client.post(BASE_URL, json=data)
    assert 'Invalid email or password' in response.json['error']

def test_login_incomplete_user(client):
    data = {'email': ''}
    response = client.post(BASE_URL, json=data)
    assert 'Please enter email_id to reset' in response.json['error']