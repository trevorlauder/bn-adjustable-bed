# Copyright 2021 Trevor Lauder.
# SPDX-License-Identifier: MIT

import pytest

from bn_adjustable_bed.bed_socket.bedsocket import BedSocket
from bn_adjustable_bed.bed_socket.config import get_config
from bn_adjustable_bed.bed_socket.datastore import DataStore
from bn_adjustable_bed.bed_socket.loghandler import LogHandler

config = get_config()

bed_logging = LogHandler()


@pytest.fixture
def bed_socket_monkeypatch(monkeypatch):
    monkeypatch.setenv("REDIS_HOST", "redis")


def test_api(mocker, bed_socket_monkeypatch):
    mocker.patch("bn_adjustable_bed.bed_socket.datastore")
    mocker.patch("bn_adjustable_bed.bed_socket.bedsocket.socket.socket")

    datastore = DataStore(
        bed_logging=bed_logging,
        host="redis",
    )

    bedsocket = BedSocket(
        config=config,
        datastore=datastore,
        bed_logging=bed_logging,
    )

    mocker.patch.object(bedsocket, "connection")
    mocker.patch.object(bedsocket, "address")
    socket_send_data_spy = mocker.spy(bedsocket, "socket_send_data")

    bedsocket.connection.recv.return_value = bytes.fromhex("d300000000")

    bedsocket.api(online=False, loop=False)

    assert bedsocket.online is True

    socket_send_data_spy.assert_has_calls(
        [
            mocker.call(
                data="d800000000",
            ),
            mocker.call(
                data="90000000173321fd6e4f8f1aaa50aa44eb433dbe1bba972776005c05"
            ),
        ]
    )
