import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app


@pytest.fixture()
def client():
    storage.students.clear()
    storage.next_id = 1
    with TestClient(app) as test_client:
        yield test_client
    storage.students.clear()
    storage.next_id = 1
