'''
1. Only authenticated users should be able to fetch the user details
2. A request with an invalid token should not be entertained
'''

from app.services.user import _generate_tokens


def test_fetch_user(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {
        'Authorization': f"Bearer {data['access_token']}"
    }
    response = client.get('/users/me', headers=headers)
    assert response.status_code == 200
    assert response.json()['email'] == user.email


def test_fetch_user_with_invalid_token(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {
        'Authorization': f"Bearer {data['access_token'][:-6]}ajajks"
    }
    response = client.get('/users/me', headers=headers)
    assert response.status_code == 401
    assert 'email' not in response.json()


def test_fetch_user_detail_by_id(auth_client, user):
    response = auth_client.get(f'/users/{user.id}')
    assert response.status_code == 200
    assert response.json()['email'] == user.email

