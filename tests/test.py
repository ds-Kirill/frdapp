from fastapi.testclient import TestClient
import ..main

client = TestClient(main.app)


def test_info():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"tx_id": 1510422180, "is_fraud": 0}
    print(response.json())
