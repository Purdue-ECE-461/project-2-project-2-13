def test_hello(client):
    response = client.get('/')
    assert response.data == "Hello World!"