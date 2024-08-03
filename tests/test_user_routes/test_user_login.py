'''
1. Active user should be to login
2. User should not be able to login with incorrect password
3. Inactive user should not be able to login
'''

from tests.conftest import USER_PASSWORD


def test_user_login(client, user):
    data = {'username': user.email, 'password': USER_PASSWORD}
    response = client.post('/auth/login', data=data)
    assert response.status_code == 200
    assert response.json()['access_token'] is not None
    assert response.json()['refresh_token'] is not None
    assert response.json()['expires_in'] is not None


def test_user_login_with_invalid_password(client, user):
    data = {'username': user.email, 'password': 'wrong-password'}
    response = client.post('/auth/login', data=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid email or password.'


def test_user_login_with_wrong_email(client):
    data = {'username': 'wrong@email.com', 'password': USER_PASSWORD}
    response = client.post('/auth/login', data=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Email is not registered with us.'


def test_inactive_user_login(client, inactive_user):
    data = {'username': inactive_user.email, 'password': USER_PASSWORD}
    response = client.post('/auth/login', data=data)
    assert response.status_code == 400
