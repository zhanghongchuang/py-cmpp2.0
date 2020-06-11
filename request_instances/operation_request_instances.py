import utils
from cmpp_defines import CMPP_VERSION, CMPP_CONNECT_REQ, CMPP_SUBMIT_REQ, \
    CMPP_TERMINATE_REQ, CMPP_ACTIVE_TEST_REQ
from request_instances.request_instance import RequestInstance
from utils import Pack


class ConnectRequestInstance(RequestInstance):
    def __init__(self, sp_id, sp_secret):
        _version = Pack.get_unsigned_char_data(CMPP_VERSION)

        _sp_id = sp_id.encode('utf-8')
        _sp_secret = sp_secret.encode("utf-8")
        _time_str = utils.get_string_time()

        self.auth_source = utils.get_md5_digest(
            _sp_id + 9 * b'\x00' + _sp_secret + _time_str.encode("utf-8"))
        message_body = _sp_id + self.auth_source + _version + Pack. \
            get_unsigned_long_data(int(_time_str))
        RequestInstance.__init__(self, CMPP_CONNECT_REQ, message_body)


class TerminateRequestInstance(RequestInstance):
    def __init__(self):
        message_body = b''
        super(TerminateRequestInstance, self).__init__(CMPP_TERMINATE_REQ,
                                                       message_body)


class SubmitRequestInstance(RequestInstance):
    def __init__(self, msg_src, msg_content, dest_terminal_id, src_id='1069052123456',
                 pk_total=1, pk_number=1, registered_delivery=0, msg_level=0, service_id='MI',
                 fee_usertype=2, fee_terminal_id="", tp_pid=0, tp_udhi=0, msg_fmt=8,
                 feetype='01', feecode='000000', valid_time=17 * '\x00', at_time=17 * '\x00', sep_no=None):

        if len(msg_content) >= 70:
            raise ValueError("msg_content more than 70 words")
        if len(dest_terminal_id) > 100:
            raise ValueError("single submit more than 100 phone numbers")
        if not dest_terminal_id:
            raise ValueError("phone number can not be null")

        _msg_id = 8 * b'\x00'
        _pk_total = Pack.get_unsigned_char_data(pk_total)
        _pk_number = Pack.get_unsigned_char_data(pk_number)
        _registered_delivery = Pack.get_unsigned_char_data(registered_delivery)
        _msg_level = Pack.get_unsigned_char_data(msg_level)
        _service_id = (service_id + (10 - len(service_id)) * '\x00').encode(
            'utf-8')
        _fee_usertype = Pack.get_unsigned_char_data(fee_usertype)
        _fee_terminal_id = (fee_terminal_id + (
                21 - len(fee_terminal_id)) * '\x00').encode('utf-8')
        _tp_pid = Pack.get_unsigned_char_data(tp_pid)
        _tp_udhi = Pack.get_unsigned_char_data(tp_udhi)
        _msg_fmt = Pack.get_unsigned_char_data(msg_fmt)
        _msg_src = msg_src.encode('utf-8')
        _feetype = feetype.encode('utf-8')
        _feecode = feecode.encode('utf-8')
        _valid_time = valid_time.encode('utf-8')
        _at_time = at_time.encode('utf-8')
        _src_id = (src_id + (21 - len(src_id)) * '\x00').encode('utf-8')
        _destusr_tl = Pack.get_unsigned_char_data(len(dest_terminal_id))
        _dest_terminal_id = b""
        for msisdn in dest_terminal_id:
            _dest_terminal_id += (msisdn + (21 - len(msisdn)) * '\x00').encode(
                'utf-8')
        _msg_content = msg_content.encode('utf-16-be')
        _msg_length = Pack.get_unsigned_char_data(len(_msg_content))
        _reserve = 8 * b'\x00'
        _message_body = _msg_id + _pk_total + _pk_number + \
                        _registered_delivery + _msg_level + _service_id + \
                        _fee_usertype + _fee_terminal_id + _tp_pid + _tp_udhi + _msg_fmt + _msg_src + _feetype \
                        + _feecode + _valid_time + _at_time + _src_id + \
                        _destusr_tl + _dest_terminal_id \
                        + _msg_length + _msg_content + _reserve

        RequestInstance.__init__(self, CMPP_SUBMIT_REQ, _message_body, sep_no)


class HeartBeatRequestInstance(RequestInstance):
    def __init__(self):
        message_body = b''
        super(HeartBeatRequestInstance, self).__init__(CMPP_ACTIVE_TEST_REQ,
                                                       message_body)