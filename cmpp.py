import logging
import socket

from cmpp_defines import CMPP_ACTIVE_TEST_RESP, CMPP_ACTIVE_TEST_REQ
from request_instances import ConnectRequestInstance, TerminateRequestInstance, SubmitRequestInstance, \
    HeartBeatRequestInstance
from response_instances import parse_to_response_instance, ActiveTestResponseInstance
from utils import Unpack, time

TIMEOUT_CONNECT_TIMES = 3


class Cmpp(object):
    def __init__(self, host: str, port: int, sp_id: str, sp_secret: str):
        """
        :param host: Gateway IP
        :param port: Gateway port
        :param sp_id: Service provider id
        :param sp_secret: Service provider secret
        """
        self._host = host
        self._port = port
        self._sp_id = sp_id
        self._sp_secret = sp_secret
        self._so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def submit(self, content, phone_list, sep_no=None):
        req = SubmitRequestInstance(self._sp_id, content, phone_list, sep_no=sep_no)
        resp = self._start_request(req)
        return resp.status if resp else -1

    def _start_request(self, request_obj):
        try:
            if not self._commence():
                raise ValueError('server auth fail')
            self._send(request_obj.message)
            resp_msg = self._receive()
            resp = parse_to_response_instance(resp_msg)
            self._terminate()
            return resp
        except Exception as e:
            print(e)
        finally:
            self._close()

    def _commence(self):
        # self._connect()
        conn_req = ConnectRequestInstance(self._sp_id, self._sp_secret)
        self._send(conn_req.message)
        resp_msg = self._receive()
        if not resp_msg:
            print("Connect response message empty.")
            return
        conn_res = parse_to_response_instance(resp_msg)
        if conn_res.status == 0:
            return True
        print(
            "Connect response status({}) wrong.".format(str(conn_res.status)))

    def _terminate(self):
        self._send(TerminateRequestInstance().message)

    def _connect(self):
        self._so.connect((self._host, self._port))

    def _send(self, message):
        self._so.send(message)

    def receive(self):
        while True:
            self._receive()

    def _receive(self):
        receive_data = self._so.recv(4)
        if receive_data:
            msg_length, = Unpack.get_unsigned_long_data(receive_data)
            response_data = receive_data + self._so.recv(msg_length)
            self.handle_req_or_res(response_data)
            print(response_data)
            return response_data
        return None

    def _close(self):
        self._so.close()

    def heartbeat(self):
        while True:
            time.sleep(30)
            self._heartbeat()

    def _heartbeat(self, times=1):
        try:
            if times >= TIMEOUT_CONNECT_TIMES:
                raise ConnectionError('已超出心跳重连次数')
            self._send(HeartBeatRequestInstance().message)
            # self._so.settimeout(60)
            #
            # message = self._receive()
            # if not message:
            #     return
            # command_id, = Unpack.get_unsigned_long_data(message[4:8])
            # # self.handle_req_or_res(message)
            # while command_id != CMPP_ACTIVE_TEST_RESP:
            #     self.handle_req_or_res(message)
            #     message = self._receive()
            #     if not message:
            #         return
            #     command_id, = Unpack.get_unsigned_long_data(message[4:8])
            print('beat...')
        except TimeoutError as e:
            print(e)
            self._heartbeat(times + 1)
        except ConnectionError as e:
            print(e)
            self._close()
        except OSError:
            # 重连
            print('reconnect')
            self.login_server()

    def login_server(self):
        try:
            print('begin login')
            self._so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._connect()
            self._so.settimeout(5)
            if not self._commence():
                raise ValueError('server auth fail')
            self._so.settimeout(None)
            return True
        except Exception as e:
            print(e)

    def disconnect(self):
        self._terminate()
        self._close()

    def handle_req_or_res(self, message):
        command_id, = Unpack.get_unsigned_long_data(message[4:8])
        print(hex(command_id))
        if command_id == CMPP_ACTIVE_TEST_REQ:
            resp = ActiveTestResponseInstance(message)
        else:
            resp = parse_to_response_instance(message)
        if resp:
            self._send(resp.message)
