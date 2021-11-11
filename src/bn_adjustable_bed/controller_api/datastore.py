# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

import json

from redis import Redis


class DataStore:
    def __init__(self, config: dict, host: str):
        self.config = config

        self.r = Redis(host=host, decode_responses=True)

    def publish_command(self, name: str, channel: str = "controller"):
        self.r.publish(
            channel,
            json.dumps({"name": name, "command": self.config["commands"][name]}),
        )
