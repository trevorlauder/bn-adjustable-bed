# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

import yaml


def get_config(file: str = "config/controller_api.yml"):
    with open(file) as f:
        return yaml.safe_load(f.read())
