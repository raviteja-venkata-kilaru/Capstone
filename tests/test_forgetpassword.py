import pytest
import requests

BASE_URL = 'http://127.0.0.1:5010/api/forget_password'

@pytest.fixture
def register_url():
    return BASE_URL

def test_forget_successful(register_url):
    data = {'email': 'new_user@example.com'}
    response = requests.post(register_url, json=data)
    assert response.status_code == 200
    assert response.json['message'] == 'Successfully Reseted the password'

def test_invalid_user(register_url):
    data = {'email': 'new_user@example.com'}
    response = requests.post(register_url, json=data)
    assert response.json['error'] == 'Invalid email or password'

def test_login_incomplete_user(register_url):
    data = {'email': ''}
    response = requests.post(register_url, json=data)
    assert response.json['error'] == 'Please enter email_id to reset'