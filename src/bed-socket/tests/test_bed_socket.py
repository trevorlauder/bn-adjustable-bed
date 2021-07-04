from bed_socket.bedsocket import BedSocket
from bed_socket.config import get_config
from bed_socket.datastore import DataStore
from bed_socket.loghandler import LogHandler

config = get_config(file="bed_socket/config/config.yml")

bed_logging = LogHandler()


def test_api(mocker):
    mocker.patch("os.environ")
    mocker.patch("bed_socket.datastore")
    mocker.patch("bed_socket.bedsocket.socket.socket")

    datastore = DataStore(
        bed_logging=bed_logging,
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
