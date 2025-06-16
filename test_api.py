import requests

BASE_URL = "http://127.0.0.1:5000"

def test_create_client():
    client = {
        "email": "test.client@example.com",
        "nume": "Test Client",
        "varsta": 30,
        "accesari": 25
    }
    response = requests.post(f"{BASE_URL}/clients", json=client)
    print("POST /clients:", response.status_code, response.json())

def test_get_clients():
    response = requests.get(f"{BASE_URL}/clients")
    print("GET /clients:", response.status_code, response.json())

def test_update_client():
    client = {
        "email": "test.client@example.com",
        "nume": "Test Client",
        "varsta": 30,
        "accesari": 30
    }
    response = requests.put(f"{BASE_URL}/clients/accesses", json=client)
    print("PUT /clients/accesses:", response.status_code)
    try:
        print(response.json())
    except Exception:
        print("Răspunsul nu este JSON:", response.text)

def test_delete_client():
    response = requests.delete(f"{BASE_URL}/clients", json={"email": "test.client@example.com"})
    print("DELETE /clients:", response.status_code)
    if response.text:
        try:
            print(response.json())
        except Exception:
            print("Răspunsul nu este JSON:", response.text)
    else:
        print("Fără conținut în răspuns")

if __name__ == "__main__":
    test_create_client()
    test_get_clients()
    test_update_client()
    test_get_clients()
    test_delete_client()
    test_get_clients()
