'''
1. User should be able to generate login token with valid refresh token.
2. User should not be able to generate login token with invalid refresh token. 
'''
from app.services.user import _generate_tokens


def test_with_valid_refresh_token(client, user, test_session):
    data = _generate_tokens(user, test_session)
    header = {
        'refresh-token': data['refresh_token']
    }
    response = client.post('/auth/refresh', json={}, headers=header)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()


def test_with_invalid_refresh_token(client):
    header = {
        'refresh-token': 'ioiwqnjkjsndkcnksdjkndivnuirw'
    }
    response = client.post('/auth/refresh', json={}, headers=header)
    assert response.status_code == 400
    assert 'access_token' not in response.json()
    assert 'refresh_token' not in response.json()

