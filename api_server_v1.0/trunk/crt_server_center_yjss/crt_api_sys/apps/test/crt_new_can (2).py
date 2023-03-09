# -*- coding:utf8 -*-
import time
import serial
import logging
import binascii
import threading
import redis
import datetime
import json

logging.basicConfig(level=logging.DEBUG, filename="/home/nanjingcrt/new_crt/logs/can.log",
                    format="【%(asctime)s】 【%(levelname)s】 >>>  %(message)s", datefmt="%Y-%m-%d %H:%M")


class SerialCan:

    def __init__(self, Port="/dev/ttyS0", BaudRate="9600", ByteSize="8", Parity="N", Stopbits="1"):
        """
        :param Port: COM串口
        :param BaudRate: 波特率
        :param ByteSize: 字节大小
        :param Parity: 校验位
        :param Stopbits: 停止位
        """
        self.port = Port
        self.baudrate = BaudRate
        self.bytesize = ByteSize
        self.parity = Parity
        self.stopbits = Stopbits
        self.timeout = 60
        self._serial = None
        self._is_connected = False
        conn_pool = redis.ConnectionPool(host="127.0.0.1",
                                         port=6379,
                                         db=0,
                                         password="njzx20220512",
                                         decode_responses=True)
        self.redis_store = redis.StrictRedis(connection_pool=conn_pool)

    def connect(self):
        """
        连接设备
        """
        self._serial = serial.Serial()
        self._serial.port = self.port
        self._serial.baudrate = self.baudrate
        self._serial.bytesize = int(self.bytesize)
        self._serial.parity = self.parity
        self._serial.stopbits = int(self.stopbits)
        self._serial.timeout = self.timeout

        try:
            self._serial.open()
            if self._serial.isOpen():
                self._is_connected = True
                self._serial.flushInput()
                self.redis_store.delete("can_data")
        except Exception as e:
            self._is_connected = False
            logging.error(e)

    def disconnect(self):
        """
        断开连接
        """
        if self._serial:
            self._serial.close()

    def write(self, data, isHex=False):
        """
        发送数据给串口设备
        """
        if self._is_connected:
            if self._serial.isOpen():
                if isHex:
                    data = binascii.unhexlify(data)
                self._serial.write(data)

    def _on_data_received(self, func):
        """
        接收原始报文数据
        """
        while True:
            if self._is_connected:
                try:
                    number = self._serial.inWaiting()
                    if number > 0:
                        # data1 = self._serial.read(number)
                        # data1 = self._serial.readline()
                        time.sleep(0.1)
                        n = self._serial.inWaiting()
                        data = self._serial.read(n)
                        logging.info("读取的数据", type(data), data)
                        if data:
                            func(data)
                    time.sleep(0.02)
                except Exception as e:
                    self._is_connected = False
                    self._serial = None
                    break

    def on_data_received(self, func):
        """
        设置接收原始报文数据守护线程
        """
        tDataReceived = threading.Thread(target=self._on_data_received, args=(func,))
        tDataReceived.setDaemon(True)
        tDataReceived.start()

    def crt_serial_on_connected_changed(self, is_connected):
        if is_connected:
            logging.info("Connected")
            self.connect()
            self.on_data_received(self.crt_serial_on_data_received)
        else:
            logging.info("DisConnected")

    def crt_serial_on_data_received(self, data):
        logging.info("存储到缓存数据", str(datetime.datetime.now()), data)
        # self.serial_recieve_data += data.decode("utf-8", "ignore")
        # self.serial_recieve_data_hex = binascii.hexlify(data).decode("utf-8").upper()
        # data_str = data.decode("utf-8", "ignore")
        data_hex = binascii.hexlify(data).decode("utf-8").upper()
        data_dict = {"data_str": str(data), "data_hex": data_hex, "sort": int(time.time() * 1000)}
        self.redis_store.rpush("can_data", json.dumps(data_dict))


if __name__ == "__main__":
    crt_serial = SerialCan()
    crt_serial.crt_serial_on_connected_changed(is_connected=True)
    while True:
        logging.info("程序运行中")
        time.sleep(3600)
