import pytest
import requests

BASE_URL = 'http://127.0.0.1:5010'

@pytest.fixture
def register_url():
    return BASE_URL

def test_login_successful(register_url):
    data = {'email': 'new_user@example.com', 'password':'Raviteja@132'}
    response = requests.post(register_url, json=data)
    assert response.status_code == 200
    assert response.json['message'] == 'Successfully Login'

def test_invalid_user(register_url):
    data = {'email': 'new_user@example.com', 'password':'Raviteja@132'}
    response = requests.post(register_url, json=data)
    assert response.json['error'] == 'Invalid email or password'

def test_login_incomplete_user(register_url):
    data = {'email': 'new_user@example.com', 'password':'Raviteja@132'}
    response = requests.post(register_url, json=data)
    assert response.json['error'] == 'Please enter Email or Password'