# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

from bn_adjustable_bed.controller_api.datastore import DataStore


class Api(FastAPI):
    def __init__(self, config: dict, datastore: DataStore):
        super().__init__(title="Command API")

        self.config = config
        self.datastore = datastore

        @self.get("/")
        def api_home():
            return RedirectResponse(url="/docs")

        @self.get("/config")
        def api_config():
            return self.config

        @self.put("/command")
        def api_command(name: str):
            if name in self.config["commands"] and self.config["commands"][name] != "":
                self.datastore.publish_command(name=name)

                return {"name": name, "success": True}
            else:
                raise HTTPException(
                    status_code=404, detail={"name": name, "success": False}
                )
