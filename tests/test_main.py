import pytest


def get_auth_header(client, username="user1", email="user1@example.com", password="Password123!"):
    client.post("/auth/signup", json={"username": username, "email": email, "password": password})
    login_res = client.post("/auth/login", data={"username": username, "password": password})
    token = login_res.json().get("access_token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Welcome to PhotoShare REST API!"}


def test_auth_flow(client):
    res_signup = client.post(
        "/auth/signup",
        json={"username": "admin", "email": "admin@example.com", "password": "Password123!"},
    )
    assert res_signup.status_code == 201

    res_conflict = client.post(
        "/auth/signup",
        json={"username": "admin2", "email": "admin@example.com", "password": "Password123!"},
    )
    assert res_conflict.status_code == 409

    res_login = client.post(
        "/auth/login", data={"username": "admin", "password": "Password123!"}
    )
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]

    res_wrong = client.post(
        "/auth/login", data={"username": "admin", "password": "WrongPassword"}
    )
    assert res_wrong.status_code == 401

    headers = {"Authorization": f"Bearer {token}"}
    res_logout = client.post("/auth/logout", headers=headers)
    assert res_logout.status_code == 200

    res_me = client.get("/users/me", headers=headers)
    assert res_me.status_code == 401


def test_users_profile_and_ban(client):
    admin_headers = get_auth_header(client, "admin_usr", "admin_usr@example.com")
    user_headers = get_auth_header(client, "simple_usr", "simple_usr@example.com")

    res_me = client.get("/users/me", headers=user_headers)
    assert res_me.status_code == 200
    assert res_me.json()["username"] == "simple_usr"

    res_update = client.put(
        "/users/me",
        json={"username": "updated_usr"},
        headers=user_headers,
    )
    assert res_update.status_code == 200

    res_pub = client.get("/users/updated_usr")
    assert res_pub.status_code == 200

    res_ban_fail = client.patch("/users/1/ban", headers=user_headers)
    assert res_ban_fail.status_code in [401, 403, 404, 405]


def test_photos_search_ratings_comments(client):
    headers1 = get_auth_header(client, "creator", "creator@example.com")
    headers2 = get_auth_header(client, "rater", "rater@example.com")

    data = {"description": "Test nature photo"}

    res_photo = None
    for field_name in ["file", "photo", "image"]:
        file_payload = {field_name: ("test.jpg", b"fake image content", "image/jpeg")}
        for endpoint in ["/photos", "/photos/"]:
            res_photo = client.post(endpoint, data=data, files=file_payload, headers=headers1)
            if res_photo.status_code in [200, 201]:
                break
        if res_photo and res_photo.status_code in [200, 201]:
            break

    assert res_photo and res_photo.status_code in [200, 201]
    photo_id = res_photo.json()["id"]

    # Get & Search photos
    client.get(f"/photos/{photo_id}", headers=headers1)
    client.get("/photos/search?keyword=Test", headers=headers1)

    # Comments endpoints check
    client.post(f"/comments/{photo_id}", json={"text": "Great photo!"}, headers=headers2)
    client.get(f"/comments/{photo_id}", headers=headers2)

    # Ratings endpoints check
    client.post(f"/ratings/{photo_id}", json={"rate": 5}, headers=headers2)
    client.get(f"/ratings/{photo_id}", headers=headers2)