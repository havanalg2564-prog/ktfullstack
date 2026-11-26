def test_register(client):
    response = client.post(
        "/auth/register", 
        json={"email": "test@test.com", "password": "secret123"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@test.com"

def test_login(client):
    # Регистрируем пользователя
    client.post("/auth/register", json={"email": "login@test.com", "password": "secret123"})
    
    # Логинимся (OAuth2 требует data, а не json)
    response = client.post(
        "/auth/login",
        data={"username": "login@test.com", "password": "secret123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()