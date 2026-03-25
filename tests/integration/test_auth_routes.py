def get_token(client):
    client.post("/api/auth/register", json={
        "email": "test2@example.com",
        "password": "123456"
    })

    response = client.post("/api/auth/login", json={
        "email": "test2@example.com",
        "password": "123456"
    })

    return response.json["access_token"]


def test_extract_requires_auth(client):
    response = client.post("/api/extract", json={
        "url": "https://example.com"
    })

    assert response.status_code == 401


def test_extract_success(client, mocker):
    token = get_token(client)

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = """
    <html>
        <head><title>Example</title></head>
        <body>Hello World</body>
    </html>
    """

    mocker.patch("requests.get", return_value=mock_response)

    response = client.post(
        "/api/extract",
        json={"url": "http://test.com"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "title" in response.json