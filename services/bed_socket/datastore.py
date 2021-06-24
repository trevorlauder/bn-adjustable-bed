import os

import redis


class DataStore:
    def __init__(self, bed_logging: object):
        self.bed_logging = bed_logging

        self.r = redis.Redis(
            host=os.environ["REDIS_HOST"], decode_responses=True
        )

    def subscribe(self, channel: str = "controller"):
        sub = self.r.pubsub()
        sub.subscribe([channel])

        return sub

    def update(self, group: str, group_value: str):
        if self.r.exists(group):
            existing_group_value = self.r.get(group)

            if existing_group_value != group_value:
                self.r.set(group, str(group_value))

                self.bed_logging.log(
                    message="Changed {} from {} => {}".format(
                        group,
                        existing_group_value,
                        group_value,
                    )
                )
        else:
            self.r.set(group, str(group_value))

            self.bed_logging.log(
                message="Set {} => {}".format(
                    group,
                    group_value,
                )
            )
