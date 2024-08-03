'''
1. User should be able to send forgot password request
2. User should not be able to send forgot password request with invalid email address
3. Unverified user should not be able to send forgot password request
4. Inactive user should not be able to request forgot password email
'''

def test_forgot_password_request(client, user):
    data = {'email': user.email}
    response = client.post('/auth/forgot-password', json=data)
    assert response.status_code == 200

def test_forgot_password_request_with_invalid_email(client):
    data = {'email': 'invalid_email@email.com'}
    response = client.post('/auth/forgot-password', json=data)
    assert response.status_code == 404

def test_forgot_password_request_with_unverified_user(client, unverified_user):
    data = {'email': unverified_user.email}
    response = client.post('/auth/forgot-password', json=data)
    assert response.status_code == 400

def test_forgot_password_request_with_inactive_user(client, inactive_user):
    data = {'email': inactive_user.email}
    response = client.post('/auth/forgot-password', json=data)
    assert response.status_code == 400

