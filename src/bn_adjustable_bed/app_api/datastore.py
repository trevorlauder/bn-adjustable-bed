# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

from redis import Redis


class DataStore:
    def __init__(self, host: str):
        self.r = Redis(host=host, decode_responses=True)

    def exists(self, key: str):
        return self.r.exists(key) != 0

    def get(self, key: str):
        return self.r.get(key)
