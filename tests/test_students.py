VALID_STUDENT = {
    "name": "Kavya",
    "email": "kavya@example.com",
    "age": 19,
    "course": "Computer Science",
}


def test_create_student_returns_201(client):
    response = client.post("/students/", json=VALID_STUDENT)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == VALID_STUDENT["name"]
    assert data["email"] == VALID_STUDENT["email"]
    assert data["age"] == VALID_STUDENT["age"]
    assert data["course"] == VALID_STUDENT["course"]


def test_get_all_students_returns_200(client):
    client.post("/students/", json=VALID_STUDENT)

    response = client.get("/students/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == VALID_STUDENT["name"]


def test_get_existing_student_returns_200(client):
    created = client.post("/students/", json=VALID_STUDENT).json()

    response = client.get(f"/students/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["email"] == VALID_STUDENT["email"]


def test_get_nonexistent_student_returns_404(client):
    response = client.get("/students/9999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_existing_student(client):
    created = client.post("/students/", json=VALID_STUDENT).json()

    response = client.put(
        f"/students/{created['id']}",
        json={"course": "Software Engineering"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert data["course"] == "Software Engineering"
    assert data["name"] == VALID_STUDENT["name"]


def test_delete_existing_student(client):
    created = client.post("/students/", json=VALID_STUDENT).json()

    response = client.delete(f"/students/{created['id']}")

    assert response.status_code == 204
    follow_up = client.get(f"/students/{created['id']}")
    assert follow_up.status_code == 404


def test_invalid_student_data_is_rejected_with_422(client):
    response = client.post(
        "/students/",
        json={
            "name": "",
            "email": "invalid-email",
            "age": 15,
            "course": "Computer Science",
        },
    )

    assert response.status_code == 422
