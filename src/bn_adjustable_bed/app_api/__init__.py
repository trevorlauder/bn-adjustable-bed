# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

import os

import uvicorn  # type: ignore

from bn_adjustable_bed.app_api.api import Api
from bn_adjustable_bed.app_api.config import get_config
from bn_adjustable_bed.app_api.datastore import DataStore


def main():
    config = get_config()

    datastore = DataStore(host=os.environ["REDIS_HOST"])

    api = Api(config=config, datastore=datastore)

    uvicorn.run(api, host="0.0.0.0", port=80)
