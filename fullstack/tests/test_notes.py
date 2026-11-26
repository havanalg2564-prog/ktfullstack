def get_user_token(client, email, password):
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password}
    )
    return response.json()["access_token"]

def test_create_note(client):
    token = get_user_token(client, "creator@test.com", "password")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/notes/",
        json={"title": "Моя первая заметка", "content": "Текст", "category_id": 1},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Моя первая заметка"

def test_read_user_notes(client):
    token = get_user_token(client, "reader@test.com", "password")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Создаем заметку
    client.post(
        "/notes/",
        json={"title": "Секретная заметка", "content": "Текст", "category_id": 1},
        headers=headers
    )
    
    # Читаем свои заметки
    response = client.get("/notes/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_delete_note_rbac(client):
    # Создаем обычного пользователя и его заметку
    token_user1 = get_user_token(client, "user1@test.com", "password")
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}
    
    res = client.post(
        "/notes/",
        json={"title": "Заметка юзера 1", "content": "Текст", "category_id": 1},
        headers=headers_user1
    )
    note_id = res.json()["id"]
    
    # Создаем второго обычного пользователя
    token_user2 = get_user_token(client, "user2@test.com", "password")
    headers_user2 = {"Authorization": f"Bearer {token_user2}"}
    
    # Пытаемся удалить заметку (RBAC должен вернуть 403, так как нужен ADMIN)
    response = client.delete(f"/notes/{note_id}", headers=headers_user2)
    assert response.status_code == 403
    assert "Недостаточно прав" in response.json()["detail"]