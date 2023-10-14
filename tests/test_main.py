import pytest

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_headers(access_token: str) -> dict:
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture(scope="module")
def test_user():
    yield {}


@pytest.fixture(scope="module")
def access_token():
    client_data = {"username": "test", "password": "testpass"}
    response = client.post("/v1/clients/signup", json=client_data)
    
    if (access_token := response.json().get('access_token')):
        return access_token

    response = client.post("/v1/clients/signin", json=client_data)
    return response.json().get('access_token')


def test_create_user_wit_fake_auth(test_user):
    user_data = {"name": "Guido van Rossum"}; headers = get_headers('testtest')
    response = client.post("/v1/users/", json=user_data, headers=headers)

    assert response.status_code == 403


def test_create_user(access_token, test_user):
    user_data = {"name": "Guido van Rossum"}; headers = get_headers(access_token)
    response = client.post("/v1/users/", json=user_data, headers=headers)

    user = response.json()
    test_user.update(user)

    assert response.status_code == 201
    assert user.get("name") == user_data["name"]


def test_read_users(access_token, test_user):
    headers = get_headers(access_token)
    response = client.get("/v1/users/", headers=headers)
    users = response.json()

    assert response.status_code == 200
    assert isinstance(users, list)
    assert test_user in users


def test_read_user(access_token, test_user):

    user_id = test_user.get("id"); headers = get_headers(access_token)
    response = client.get(f"/v1/users/{user_id}", headers=headers)

    assert response.status_code == 200
    assert response.json() == test_user


def test_update_user(access_token, test_user):
    
    user_id = test_user.get("id"); headers = get_headers(access_token)

    test_user.update({"name": "Guido"})
    response = client.patch(f"/v1/users/{user_id}", json=test_user, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_user


def test_delete_user(access_token, test_user):
    user_id = test_user.get("id"); headers = get_headers(access_token)
    response = client.delete(f"/v1/users/{user_id}", headers=headers)
    assert response.status_code == 204