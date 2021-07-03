import json
import os

import redis


class DataStore:
    def __init__(self, config: dict):
        self.config = config

        self.r = redis.Redis(
            host=os.environ["REDIS_HOST"], decode_responses=True
        )

    def publish_command(self, name: str, channel: str = "controller"):
        self.r.publish(
            channel,
            json.dumps(
                {"name": name, "command": self.config["commands"][name]}
            ),
        )
