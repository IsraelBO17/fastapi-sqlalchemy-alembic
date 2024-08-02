'''
1 - Test if the user account activation action is working
2 - Test activation link is valid only once
3 - Test activation is not allowing invalid token
4 - Test activation is not allowing invalid email 
'''

import time
from app.config.security import hash_password
from app.models.user import User
from app.utils.email_context import USER_VERIFY_ACCOUNT


def test_user_account_verification(client, inactive_user, test_session):
    token_context = inactive_user.get_context_string(USER_VERIFY_ACCOUNT)
    token = hash_password(token_context)
    data = {
        'email': inactive_user.email,
        'token': token
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code == 200
    activated_user = test_session.query(User).filter(User.email == inactive_user.email).first()
    assert activated_user.is_active is True
    assert activated_user.verified_at is not None


def test_user_account_verification_link_doesnt_work_twice(client, inactive_user):
    token_context = inactive_user.get_context_string(USER_VERIFY_ACCOUNT)
    token = hash_password(token_context)
    time.sleep(1)
    data = {
        'email': inactive_user.email,
        'token': token
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code == 200
    response = client.post('/users/verify', json=data)
    assert response.status_code != 200


def test_invalid_token_doesnt_work(client, inactive_user, test_session):
    data = {
        'email': inactive_user.email,
        'token': 'agaghagsxkaubiuncuiwe7e982jind93dubsds'
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code != 200
    activated_user = test_session.query(User).filter(User.email == inactive_user.email).first()
    assert activated_user.is_active is False
    assert activated_user.verified_at is None


def test_invalid_email_doesnt_work(client, inactive_user, test_session):
    token_context = inactive_user.get_context_string(USER_VERIFY_ACCOUNT)
    token = hash_password(token_context)
    data = {
        'email': 'test@describly.com',
        'token': token
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code != 200
    activated_user = test_session.query(User).filter(User.email == inactive_user.email).first()
    assert activated_user.is_active is False
    assert activated_user.verified_at is None
