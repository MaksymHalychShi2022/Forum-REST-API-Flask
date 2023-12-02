def test_get_categories(client, init_database, test_user):
    login_response = client.post("/auth/login", json={"email": "test@example.com", "password": "password"})
    access_token = login_response.json["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/categories", headers=headers)
    assert response.status_code == 200


def test_create_category(client, init_database):
    login_response = client.post("/auth/login", json={"email": "admin@example.com", "password": "password"})
    access_token = login_response.json["access_token"]

    new_category = {"title": "New Category", "description": "Description of new category"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/categories", headers=headers, json=new_category)
    assert response.status_code == 201
    assert response.json["title"] == new_category["title"]
