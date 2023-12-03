from . import login_as


def test_get_comments(client, init_database, test_user, test_topic):
    access_token = login_as(client, test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/comments", headers=headers, json={"topic_id": test_topic.id})
    assert response.status_code == 200


def test_create_topic(client, init_database, test_user, test_topic):
    access_token = login_as(client, test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    new_comment = {
        "body": "Test body",
        "topic_id": test_topic.id
    }
    response = client.post("/comments", headers=headers, json=new_comment)
    assert response.status_code == 201


def test_get_comment(client, init_database, test_user, test_comment):
    access_token = login_as(client, test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get(f"/comments/{test_comment.id}", headers=headers)
    assert response.status_code == 200
    assert response.json["id"] == test_comment.id
    assert response.json["body"] == test_comment.body


def test_update_comment(client, init_database, test_user, test_comment):
    access_token = login_as(client, test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    updated_data = {"body": "Updated comment body"}
    response = client.put(f"/comments/{test_comment.id}", headers=headers, json=updated_data)
    assert response.status_code == 200
    assert response.json["body"] == updated_data["body"]


def test_update_comment(client, init_database, test_user, test_comment):
    access_token = login_as(client, test_user.email)
    headers = {"Authorization": f"Bearer {access_token}"}

    updated_data = {"body": "Updated comment body"}
    response = client.put(f"/comments/{test_comment.id}", headers=headers, json=updated_data)
    assert response.status_code == 200
    assert response.json["body"] == updated_data["body"]
