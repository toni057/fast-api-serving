from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_score_iris():
    data = {"SepalLength": 5.1, "SepalWidth": 3.5, "PetalLength": 1.4, "PetalWidth": 0.2, "Species": "setosa"}
    response = client.post("/iris", json=data)

    assert response.status_code == 200
    assert response.json()['species'] in ['setosa', 'virginica', 'versicolor']
    assert response.json()['prediction'] in ['setosa', 'virginica', 'versicolor']


def test_failing_iris_categories():
    data = {"SepalLength": 5.1, "SepalWidth": 3.5, "PetalLength": 1.4, "PetalWidth": 0.2, "Species": "setossa"}
    response = client.post("/iris", json=data)

    assert response.status_code == 403
    assert response.json() == {"detail": "<Check _isin: isin({'setosa', 'versicolor', 'virginica'})>"}
