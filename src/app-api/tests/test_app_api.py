from app_api.api import Api
from app_api.config import get_config
from fastapi.testclient import TestClient


class MockDataStore:
    def exists(self, key: str):
        return True

    def get(self, key: str):
        switcher = {
            "bed:device_mac_address": "000000000000",
            "bed:authorize_code": 123456,
        }

        return switcher.get(key, "Invalid Key")


class MockDataStoreEmpty:
    def exists(self, key: str):
        return False


config = get_config(file="app_api/config/config.yml")
test_config = get_config(file="tests/config/config.yml")

datastore_empty = MockDataStoreEmpty()
datastore = MockDataStore()

client_empty = TestClient(Api(config=config, datastore=datastore_empty))
client = TestClient(Api(config=config, datastore=datastore))


def test_api_home():
    response = client_empty.get("/", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_api_v2_user_auth():
    response = client_empty.post(
        "/v2/user_auth",
        json={"corp_id": "", "email": "", "password": ""},
        allow_redirects=False,
    )
    assert response.status_code == 200
    assert response.json() == test_config["api"]["v2_user_auth"]


def test_api_v2_subscribe_devices_empty():
    response = client_empty.get(
        "/v2/user/1/subscribe/devices", allow_redirects=False
    )
    assert response.status_code == 200
    assert response.json() == {
        "list": [],
        "version": 32,
    }


def test_api_v2_subscribe_devices():
    response = client.get(
        "/v2/user/1/subscribe/devices", allow_redirects=False
    )

    assert response.status_code == 200
    assert response.json() == {
        "list": [
            test_config["api"]["v2_subscribe_devices"]
            | {
                "mac": "000000000000",
                "name": "BASE000000000000",
                "authorize_code": 123456,
            }
        ],
        "version": 32,
    }
