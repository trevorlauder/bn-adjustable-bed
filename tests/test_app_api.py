# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

import pytest
from fastapi.testclient import TestClient

from bn_adjustable_bed.app_api.api import Api
from bn_adjustable_bed.app_api.config import get_config


class MockDataStore:
    def exists(self, *args, **kwargs):
        return True

    def get(self, key: str):
        switcher = {
            "bed:device_mac_address": "000000000000",
            "bed:authorize_code": 123456,
        }

        return switcher.get(key, "Invalid Key")


class MockDataStoreEmpty:
    def exists(self, *args, **kwargs):
        return False


@pytest.fixture
def app_api_monkeypatch(monkeypatch):
    monkeypatch.setenv("REDIS_HOST", "redis")


config = get_config()
test_config = get_config(file="tests/config/test_app_api.yml")

datastore_empty = MockDataStoreEmpty()
datastore = MockDataStore()

client_empty = TestClient(Api(config=config, datastore=datastore_empty))
client = TestClient(Api(config=config, datastore=datastore))


def test_api_home(app_api_monkeypatch):
    response = client_empty.get("/", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_api_v2_user_auth(app_api_monkeypatch):
    response = client_empty.post(
        "/v2/user_auth",
        json={"corp_id": "", "email": "", "password": ""},
        allow_redirects=False,
    )

    assert response.status_code == 200
    assert response.json() == test_config["api"]["v2_user_auth"]


def test_api_v2_subscribe_devices_empty(app_api_monkeypatch):
    response = client_empty.get("/v2/user/1/subscribe/devices", allow_redirects=False)
    assert response.status_code == 200
    assert response.json() == {
        "list": [],
        "version": 32,
    }


def test_api_v2_subscribe_devices(app_api_monkeypatch):
    response = client.get("/v2/user/1/subscribe/devices", allow_redirects=False)

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
