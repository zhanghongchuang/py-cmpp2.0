from utils import Pack

_global_sep_no = 1


class RequestInstance(object):
    def __init__(self, command_id, message_body, sep_no=None):
        self.command_id = command_id
        self._message_body = message_body

        if sep_no:
            self.sequence_no = sep_no
        else:
            global _global_sep_no
            if _global_sep_no >= 2**31:
                _global_sep_no = 1
            else:
                _global_sep_no += 1
            self.sequence_no = _global_sep_no

    @property
    def message(self):
        cm_id = Pack.get_unsigned_long_data(self.command_id)
        seq_no = Pack.get_unsigned_long_data(self.sequence_no)
        t_len = len(self._message_body) + len(cm_id) + len(seq_no) + 4
        return Pack.get_unsigned_long_data(t_len) + cm_id + seq_no + self._message_body
