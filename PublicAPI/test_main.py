from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_memes():
    response = client.get("/memes", headers={
        'offset': "1",
        'limit': "3"
    })

    assert response.status_code == 200
    headers = response.headers['x-json-data']
    print(headers)



def test_get_meme():
    response = client.get('/memes/4')

    assert response.status_code == 200
    assert response.json()['filename'] == '1.jpg'
