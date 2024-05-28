import pytest
from app import app

BASE_URL = 'http://127.0.0.1:5010/api/register'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_register_successful(client):
    data = {'firstname': 'Raviteja', 'lastname': 'kilaru', 'email': 'new_user2@example.com', 'password':'Raviteja@132'}
    response = client.post(BASE_URL, json=data)       
    assert 'User Registration Successful' in response.json['message']

def test_register_duplicate_user(client):
    data = {'firstname': 'Raviteja', 'lastname': 'kilaru', 'email': 'new_user@example.com', 'password':'Raviteja@132'}
    response = client.post(BASE_URL, json=data)
    assert 'User Already There' in response.json['error']

def test_register_incomplete_user(client):
    data = {'firstname': 'Raviteja', 'lastname': '', 'email': 'new_user@example.com', 'password':'Raviteja@132'}
    response = client.post(BASE_URL, json=data)
    assert 'Fill Every details please' in response.json['error']