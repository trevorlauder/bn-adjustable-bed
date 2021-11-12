# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

import os

import yaml

config_path = f"{os.path.join(os.path.dirname(__file__))}/../config"


def get_config(file: str = f"{config_path}/bed_socket.yml"):
    with open(file) as f:
        return yaml.safe_load(f.read())
