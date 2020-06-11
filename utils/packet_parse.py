from utils import Unpack


def parse_packet_head(message):
    t_len = Unpack.get_unsigned_long_data(message[:4])
    cm_id = Unpack.get_unsigned_long_data(message[4:8])
    seq_id = Unpack.get_unsigned_long_data(message[8:12])
    return t_len, cm_id, seq_id