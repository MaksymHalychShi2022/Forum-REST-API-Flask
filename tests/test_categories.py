from . import login_as, login_as_admin


def test_get_categories(client, init_database, test_user):
    access_token = login_as(client, test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/categories", headers=headers)
    assert response.status_code == 200


def test_create_category(client, init_database):
    access_token = login_as_admin(client)
    headers = {"Authorization": f"Bearer {access_token}"}

    new_category = {"title": "New Category", "description": "Description of new category"}

    response = client.post("/categories", headers=headers, json=new_category)
    assert response.status_code == 201
    assert response.json["title"] == new_category["title"]


def test_get_category(client, init_database, test_user, test_category):
    access_token = login_as(client, test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get(f"/categories/{test_category.id}", headers=headers)
    assert response.status_code == 200
    assert response.json["id"] == test_category.id


def test_update_category(client, init_database, test_category):
    access_token = login_as_admin(client)
    headers = {"Authorization": f"Bearer {access_token}"}

    updated_data = {"title": "Updated Category", "description": "Updated description"}

    response = client.patch(f"/categories/{test_category.id}", headers=headers, json=updated_data)
    assert response.status_code == 200
    assert response.json["title"] == updated_data["title"]


def test_delete_category(client, init_database, test_category):
    access_token = login_as_admin(client)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.delete(f"/categories/{test_category.id}", headers=headers)
    assert response.status_code == 204

    response = client.get(f"/categories/{test_category.id}", headers=headers)
    assert response.status_code == 404
