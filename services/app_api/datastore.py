import os

import redis


class DataStore:
    def __init__(self):
        self.r = redis.Redis(
            host=os.environ["REDIS_HOST"], decode_responses=True
        )

    def exists(self, key: str):
        return self.r.exists(key) != 0

    def get(self, key: str):
        return self.r.get(key)
