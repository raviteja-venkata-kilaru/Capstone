import pytest
import requests

BASE_URL = 'http://127.0.0.1:5010/api/register/'

@pytest.fixture
def register_url():
    return BASE_URL

def test_register_successful(register_url):
    data = {'firstname': 'Raviteja', 'lastname': 'kilaru', 'email': 'new_user@example.com', 'password':'Raviteja@132'}

    response = requests.post(register_url, json=data)
    assert response.json['message'] == 'User Registration Successful,Please LogIn'

def test_register_duplicate_user(register_url):
    data = {'firstname': 'Raviteja', 'lastname': 'kilaru', 'email': 'new_user@example.com', 'password':'Raviteja@132'}

    response = requests.post(register_url, json=data)

    assert response.json['error'] == 'User Already There, Please LogIn'

def test_register_incomplete_user(register_url):
    data = {'firstname': 'Raviteja', 'lastname': '', 'email': 'new_user@example.com', 'password':'Raviteja@132'}

    response = requests.post(register_url, json=data)

    assert response.json['error'] == 'Fill Every details please'