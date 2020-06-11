from utils import Unpack, Pack


class ResponseInstance(object):
    def __init__(self, message):
        self.length, = Unpack.get_unsigned_long_data(message[0:4])
        self.command_id, = Unpack.get_unsigned_long_data(message[4:8])
        self.sequence, = Unpack.get_unsigned_long_data(message[8:12])
        self.message_body = message[12:self.length]
        self.status = -1

    @property
    def message(self):
        cm_id = Pack.get_unsigned_long_data(self.command_id)
        seq_no = Pack.get_unsigned_long_data(self.sequence)
        t_len = len(self.message_body) + len(cm_id) + len(seq_no) + 4
        return Pack.get_unsigned_long_data(t_len) + cm_id + seq_no + self.message_body
