# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

import os
import threading

from bn_adjustable_bed.bed_socket.bedsocket import BedSocket
from bn_adjustable_bed.bed_socket.config import get_config
from bn_adjustable_bed.bed_socket.datastore import DataStore
from bn_adjustable_bed.bed_socket.loghandler import LogHandler
from bn_adjustable_bed.bed_socket.process_commands import process_commands


def main():
    config = get_config()

    bed_logging = LogHandler()

    datastore = DataStore(bed_logging=bed_logging, host=os.environ["REDIS_HOST"])

    bed_socket = BedSocket(config=config, datastore=datastore, bed_logging=bed_logging)

    online = False

    while True:
        bed_socket.accept_connection()

        process_commands_kwargs = {
            "bed_logging": bed_logging,
            "datastore": datastore,
            "bed_socket": bed_socket,
        }

        bed_socket_api_kwargs = {"online": online}

        process_commands_thread = threading.Thread(
            target=process_commands, kwargs=process_commands_kwargs
        )
        process_commands_thread.start()

        bed_socket_api_thread = threading.Thread(
            target=bed_socket.api, kwargs=bed_socket_api_kwargs
        )
        bed_socket_api_thread.start()

        online = True
