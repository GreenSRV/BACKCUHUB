import requests

BASE_URL = "http://127.0.0.1:5000"

def test_ping():
    response = requests.get(f"{BASE_URL}/ping")
    assert response.status_code == 200
    assert response.text == "Pong!"

def test_add_student():
    payload = {
        "student_id" : 1,  # Replace with a valid student ID
        "name": "John Doe",
        "year": 2
    }
    response = requests.post(f"{BASE_URL}/students", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Student added successfully"

def test_get_students():
    response = requests.get(f"{BASE_URL}/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_student():
    # Replace <id> with a valid student ID from your database
    student_id = "<id>"
    payload = {
        "name": "Jane Doe"
    }
    response = requests.put(f"{BASE_URL}/students/{student_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Student updated successfully"

def test_delete_student():
    # Replace <id> with a valid student ID from your database
    student_id = "<id>"
    response = requests.delete(f"{BASE_URL}/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Student deleted successfully"

def test_add_club():
    payload = {
        "club_id" : 1,  # Replace with a valid student ID
        "name": "Chess Club",
        "category": "Board Games"
    }
    response = requests.post(f"{BASE_URL}/clubs", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Club added successfully"

def test_get_clubs():
    response = requests.get(f"{BASE_URL}/clubs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_club():
    # Replace <id> with a valid club ID from your database
    club_id = "<id>"
    payload = {
        "category": "Recreational"
    }
    response = requests.put(f"{BASE_URL}/clubs/{club_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Club updated successfully"

def test_delete_club():
    # Replace <id> with a valid club ID from your database
    club_id = "<id>"
    response = requests.delete(f"{BASE_URL}/clubs/{club_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Club deleted successfully"