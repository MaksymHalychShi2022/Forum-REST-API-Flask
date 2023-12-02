def login_as(client, email, password="password"):
    return client.post("/auth/login", json={"email": email, "password": password}).json["access_token"]


def login_as_admin(client):
    return client.post("/auth/login", json={"email": "admin@example.com", "password": "password"}).json["access_token"]
