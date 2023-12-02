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
