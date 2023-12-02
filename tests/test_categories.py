from . import login_as, login_as_admin


def test_get_categories(client, init_database, test_user):
    access_token = login_as(client, test_user.email)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/categories", headers=headers)
    assert response.status_code == 200


def test_create_category(client, init_database):
    access_token = login_as_admin(client)

    new_category = {"title": "New Category", "description": "Description of new category"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/categories", headers=headers, json=new_category)
    assert response.status_code == 201
    assert response.json["title"] == new_category["title"]
