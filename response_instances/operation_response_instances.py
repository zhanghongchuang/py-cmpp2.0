from response_instances.response_instance import ResponseInstance
from utils import Unpack, Pack


class ConnectResponseInstance(ResponseInstance):
    def __init__(self, message):
        super(ConnectResponseInstance, self).__init__(message)
        message_body = message[12:]
        self.raw_status = message_body[0:1]
        self.status, = Unpack.get_unsigned_char_data(self.raw_status)
        self.authenticator_ISMG = message_body[1:17]
        self.version, = Unpack.get_unsigned_char_data(message_body[17:18])


class TerminateResponseInstance(ResponseInstance):
    def __init__(self, message):
        super(TerminateResponseInstance, self).__init__(message)


class SubmitResponseInstance(ResponseInstance):
    def __init__(self, message):
        super(SubmitResponseInstance, self).__init__(message)
        message_body = message[12:]
        self.msg_id, = Unpack.get_unsigned_long_long_data(message_body[0:8])
        self.status, = Unpack.get_unsigned_char_data(message_body[8:9])


class ActiveTestResponseInstance(ResponseInstance):
    def __init__(self, message):
        super(ActiveTestResponseInstance, self).__init__(message)
        self.message_body = Pack.get_unsigned_char_data(1)
