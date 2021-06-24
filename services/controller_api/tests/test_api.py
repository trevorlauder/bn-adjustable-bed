from api import Api
from config import get_config
from fastapi.testclient import TestClient


class MockDataStore:
    def exists(self, key: str):
        return False

    def publish_command(self, name: str, channel: str = "controller"):
        return RuntimeError


config = get_config(file="config/config.yml")
test_config = get_config(file="tests/config/config.yml")

datastore = MockDataStore()

client = TestClient(Api(config=config, datastore=datastore))


def test_api_home():
    response = client.get("/", allow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_api_config():
    response = client.get("/config", allow_redirects=False)

    assert response.status_code == 200
    assert response.json() == test_config


def test_api_command_valid():
    commands = [
        "flat",
        "zero_g",
        "preset_one",
        "preset_two",
        "preset_three",
    ]

    for command in commands:
        payload = {"name": command}

        response = client.put(
            "/command", params=payload, allow_redirects=False
        )

        assert response.status_code == 200
        assert response.json() == {"name": command, "success": True}


def test_api_command_invalid():
    commands = ["preset_four"]

    for command in commands:
        payload = {"name": command}

        response = client.put(
            "/command", params=payload, allow_redirects=False
        )

        assert response.status_code == 404
        assert response.json() == {
            "detail": {"name": command, "success": False}
        }
