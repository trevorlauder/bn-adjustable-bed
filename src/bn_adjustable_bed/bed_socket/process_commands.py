# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

import json


def process_commands(
    bed_logging: object,
    datastore: object,
    bed_socket: object,
):
    command_sub = datastore.subscribe()

    while True:
        try:
            for item in command_sub.listen():
                if item["type"] == "message":
                    data = json.loads(item["data"])

                    if "name" and "command" in data:
                        bed_socket.socket_send_data(data["command"])

                        bed_logging.log(
                            message="Sent to Bed (command: {}): {}".format(
                                data["name"],
                                data["command"],
                            )
                        )
        except RuntimeError as e:
            bed_logging.log(message=e)
