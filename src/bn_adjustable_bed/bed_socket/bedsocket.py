# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

import re
import socket
import sys


class BedSocket:
    def __init__(
        self,
        config: dict,
        datastore: object,
        bed_logging: object,
        host: str = "0.0.0.0",
        port: int = 23778,
    ):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))
        self.s.listen(1)

        self.config = config
        self.datastore = datastore
        self.bed_logging = bed_logging

        self.address = None
        self.connection = None

    def receive_data(self):
        self.connection.settimeout(2.0)

        while True:
            socket_data = None

            try:
                socket_data = self.connection.recv(2048)
            except OSError:
                next
            except socket.timeout:
                continue

            if socket_data is not None and len(socket_data) == 0:
                self.connection.close()

                self.bed_logging.log(
                    message="Connection Closed: {}:{}".format(
                        self.address[0], self.address[1]
                    )
                )

                sys.exit(1)
            elif socket_data is not None:
                break

        return socket_data

    def socket_send_data(self, data: str):
        try:
            self.connection.send(bytes.fromhex(data))
        except OSError:
            self.connection.close()

            self.bed_logging.log(
                message="Socket Closed While Trying to Send: {}:{} ()".format(
                    self.address[0], self.address[1]
                )
            )

            sys.exit(1)

    def accept_connection(self):
        self.bed_logging.log(message="Started and Waiting for a New Connection!")

        self.connection, self.address = self.s.accept()

        self.bed_logging.log(
            message="Connection Opened: {}:{}".format(self.address[0], self.address[1])
        )

    def api(self, online: bool, loop: bool = True):
        self.online = online

        do_loop = True

        while do_loop:
            socket_data = self.receive_data()

            socket_data_hex = socket_data.hex()

            self.bed_logging.log(
                message="Received from {}:{}: {}".format(
                    self.address[0],
                    self.address[1],
                    socket_data_hex,
                )
            )

            for response in self.config["responses"]:
                socket_data_match = re.search(response, socket_data_hex)

                if socket_data_match:
                    respond_data = self.config["responses"][response]

                    if "groups" in respond_data and isinstance(
                        respond_data["groups"], list
                    ):
                        for count, group in enumerate(respond_data["groups"], start=1):
                            group_value = bytes.fromhex(
                                socket_data_match.group(count)
                            ).decode()

                            self.datastore.update(
                                group=group,
                                group_value=group_value,
                            )

                    self.socket_send_data(data=respond_data["response"])

                    self.bed_logging.log(
                        message="Sent to {}:{} in Response: {}".format(
                            self.address[0],
                            self.address[1],
                            respond_data["response"],
                        )
                    )

                    if not self.online:
                        command = self.config["commands"]["online"]["send"]

                        self.socket_send_data(data=command)

                        self.online = True

                        self.bed_logging.log(
                            message="Sent to {}:{} (to put online): {}".format(
                                self.address[0], self.address[1], command
                            )
                        )

            do_loop = loop
