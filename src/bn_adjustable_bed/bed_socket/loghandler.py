# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

import datetime
import logging


class LogHandler:
    def __init__(self):
        logging.basicConfig(format="%(levelname)s:     %(message)s", level=logging.INFO)

        self.logging = logging

    def log(self, message: str = None):
        if message:
            timestamp = str(datetime.datetime.now().strftime("%d %b %Y %H:%M:%S"))

            self.logging.info("{}: {}".format(timestamp, message))
