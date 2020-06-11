from cmpp_defines import CMPP_CONNECT_RESP, CMPP_TERMINATE_RESP, \
    CMPP_SUBMIT_RESP, CMPP_ACTIVE_TEST_RESP

from response_instances import *

_RESPONSE_MAPPING = {
    CMPP_CONNECT_RESP: ConnectResponseInstance,
    CMPP_TERMINATE_RESP: TerminateResponseInstance,
    CMPP_SUBMIT_RESP: SubmitResponseInstance,
    CMPP_ACTIVE_TEST_RESP: ActiveTestResponseInstance
}


def parse_to_response_instance(message):
    command_id, = Unpack.get_unsigned_long_data(message[4:8])
    if command_id not in _RESPONSE_MAPPING:
        return
    return _RESPONSE_MAPPING[command_id](message)
