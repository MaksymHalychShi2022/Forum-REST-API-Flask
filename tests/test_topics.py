from . import login_as, login_as_admin


def test_get_topics(client, init_database, test_user, test_category):
    access_token = login_as(client, test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/topics", headers=headers, json={"category_id": test_category.id})
    assert response.status_code == 200


def test_create_topic(client, init_database, test_category):
    access_token = login_as_admin(client)
    headers = {"Authorization": f"Bearer {access_token}"}

    new_topic = {
        "title": "New Topic Title",
        "body": "Body of the new topic",
        "category_id": test_category.id
    }
    response = client.post("/topics", headers=headers, json=new_topic)
    assert response.status_code == 201
    assert response.json["title"] == new_topic["title"]
