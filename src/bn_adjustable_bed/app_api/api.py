# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse


class UserAuth(BaseModel):
    corp_id: str
    email: str
    password: str


class Api(FastAPI):
    def __init__(self, config: dict, datastore: object):
        super().__init__(title="Mobile App API")

        self.config = config
        self.datastore = datastore

        @self.get("/")
        def api_home():
            return RedirectResponse(url="/docs")

        @self.post("/v2/user_auth")
        def api_v2_user_auth(user_auth: UserAuth):
            return self.config["api"]["v2_user_auth"]

        @self.get("/v2/user/1/subscribe/devices")
        def api_v2_subscribe_devices():
            if self.datastore.exists("bed:authorize_code") and self.datastore.exists(
                "bed:device_mac_address"
            ):
                authorize_code = self.datastore.get("bed:authorize_code")
                device_mac_address = self.datastore.get("bed:device_mac_address")

                devices = {
                    "list": [
                        self.config["api"]["v2_subscribe_devices"]
                        | {
                            "mac": device_mac_address,
                            "name": "{}{}".format("BASE", device_mac_address),
                            "authorize_code": authorize_code,
                        }
                    ],
                    "version": 32,
                }
            else:
                devices = {
                    "list": [],
                    "version": 32,
                }

            return devices
