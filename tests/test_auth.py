def test_register(client, init_database):
    new_user = {"email": "newuser@example.com", "username": "newuser", "password": "password"}
    response = client.post("/auth/register", json=new_user)
    assert response.status_code == 201
    assert response.json["email"] == new_user["email"]


def test_login(client, init_database, test_user):
    login_data = {"email": "test@example.com", "password": "password"}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 201
    assert "access_token" in response.json


def test_get_user(client, init_database, test_user):
    login_response = client.post("/auth/login", json={"email": "test@example.com", "password": "password"})
    access_token = login_response.json["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/user", headers=headers)
    assert response.status_code == 200


def test_update_user(client, init_database, test_user):
    login_response = client.post("/auth/login", json={"email": "test@example.com", "password": "password"})
    access_token = login_response.json["access_token"]

    updated_data = {"username": "updatedName"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.put("/auth/user", headers=headers, json=updated_data)
    assert response.status_code == 200
    assert response.json["username"] == updated_data["username"]
