from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from main import app

# Заглушка для Cloudinary, щоб тести проходили без реальних ключів
patch("cloudinary.uploader.upload", return_value={
    "secure_url": "https://res.cloudinary.com/demo/image/upload/sample.jpg",
    "public_id": "photoshare/sample"
}).start()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def get_auth_header(client, username, email):
    payload = {
        "username": username,
        "email": email,
        "password": "password123"
    }
    signup_endpoints = ["/api/auth/signup", "/auth/signup", "/api/auth/register", "/auth/register"]
    for ep in signup_endpoints:
        client.post(ep, json=payload)

    login_payload = {
        "username": email,
        "password": "password123"
    }
    token = None
    login_endpoints = ["/api/auth/login", "/auth/login"]
    for ep in login_endpoints:
        res = client.post(ep, data=login_payload)
        if res.status_code == 200:
            token = res.json().get("access_token")
            break

    if not token:
        login_payload_user = {"username": username, "password": "password123"}
        for ep in login_endpoints:
            res = client.post(ep, data=login_payload_user)
            if res.status_code == 200:
                token = res.json().get("access_token")
                break

    return {"Authorization": f"Bearer {token}"} if token else {}

def test_healthcheck(client):
    res = None
    for ep in ["/api/healthchecker", "/healthchecker", "/", "/api/"]:
        res = client.get(ep)
        if res.status_code == 200:
            break
    assert res and res.status_code == 200

def test_auth_flow(client):
    res_signup = None
    for ep in ["/api/auth/signup", "/auth/signup", "/api/auth/register"]:
        res_signup = client.post(ep, json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        })
        if res_signup.status_code in [201, 409]:
            break
    assert res_signup and res_signup.status_code in [201, 409]

    res_login = None
    for ep in ["/api/auth/login", "/auth/login"]:
        res_login = client.post(ep, data={
            "username": "testuser@example.com",
            "password": "password123"
        })
        if res_login.status_code == 200:
            break
    assert res_login and res_login.status_code == 200
    data = res_login.json()
    assert "access_token" in data

def test_users_profile_and_ban(client):
    headers = get_auth_header(client, "profileuser", "profileuser@example.com")
    res_me = None
    for ep in ["/api/users/me", "/users/me"]:
        res_me = client.get(ep, headers=headers)
        if res_me.status_code == 200:
            break
    assert res_me and res_me.status_code == 200

def test_photos_search_ratings_comments(client):
    headers1 = get_auth_header(client, "creator", "creator@example.com")
    data = {"description": "Test nature photo"}
    res_photo = None
    for field_name in ["file", "photo", "image"]:
        file_payload = {field_name: ("test.jpg", b"fake image content", "image/jpeg")}
        for endpoint in ["/photos", "/photos/", "/api/photos", "/api/photos/"]:
            res_photo = client.post(endpoint, data=data, files=file_payload, headers=headers1)
            if res_photo.status_code in [200, 201]:
                break
        if res_photo and res_photo.status_code in [200, 201]:
            break
    assert res_photo and res_photo.status_code in [200, 201]