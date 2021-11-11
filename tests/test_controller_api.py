import pytest
from fastapi.testclient import TestClient

from bn_adjustable_bed.controller_api.api import Api
from bn_adjustable_bed.controller_api.config import get_config


class MockDataStore:
    def exists(self, key: str):
        return False

    def publish_command(self, name: str, channel: str = "controller"):
        return RuntimeError


config = get_config(file="config/controller_api.yml")
test_config = get_config(file="tests/config/test_controller_api.yml")

datastore = MockDataStore()

client = TestClient(Api(config=config, datastore=datastore))


@pytest.fixture
def controller_api_monkeypatch(monkeypatch):
    monkeypatch.setenv("REDIS_HOST", "redis")


def test_api_home(controller_api_monkeypatch):
    response = client.get("/", allow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_api_config(controller_api_monkeypatch):
    response = client.get("/config", allow_redirects=False)

    assert response.status_code == 200
    assert response.json() == test_config


def test_api_command_valid(controller_api_monkeypatch):
    commands = [
        "flat",
        "zero_g",
        "preset_one",
        "preset_two",
        "preset_three",
    ]

    for command in commands:
        payload = {"name": command}

        response = client.put("/command", params=payload, allow_redirects=False)

        assert response.status_code == 200
        assert response.json() == {"name": command, "success": True}


def test_api_command_invalid(controller_api_monkeypatch):
    commands = ["preset_four"]

    for command in commands:
        payload = {"name": command}

        response = client.put("/command", params=payload, allow_redirects=False)

        assert response.status_code == 404
        assert response.json() == {"detail": {"name": command, "success": False}}
