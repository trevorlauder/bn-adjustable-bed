import threading

import reyaml

from bedsocket import BedSocket
from datastore import DataStore
from loghandler import LogHandler
from process_commands import process_commands


def main():
    config = None

    with open("config/config.yml") as f:
        config = reyaml.load(f.read())

    bed_logging = LogHandler()

    datastore = DataStore(bed_logging=bed_logging)

    bed_socket = BedSocket(
        config=config, datastore=datastore, bed_logging=bed_logging
    )

    online = False

    while True:
        bed_socket.accept_connection(bed_logging=bed_logging)

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


if __name__ == "__main__":
    main()
