# -*- coding:utf8 -*-
import time
import serial
import logging
import binascii
import platform
import threading

from logging.handlers import RotatingFileHandler

logger = logging.getLogger('test_new_can')
log_path = f'./test_new_can.log'
file_handler = RotatingFileHandler(filename=log_path, maxBytes=1024 * 1024 * 50, backupCount=10, encoding="utf-8")
logger.addHandler(file_handler)

if platform.system() == "Windows":
    from serial.tools import list_ports
else:
    import glob, os, re


class SerialHelper(object):
    def __init__(self, Port="/dev/ttyS0", BaudRate="9600", ByteSize="8", Parity="N", Stopbits="1"):
        """
        初始化一些参数
        :param Port: 
        :param BaudRate: 
        :param ByteSize: 
        :param Parity: 
        :param Stopbits: 
        """
        self.port = Port
        self.baudrate = BaudRate
        self.bytesize = ByteSize
        self.parity = Parity
        self.stopbits = Stopbits
        self.threshold_value = 1
        self.receive_data_list = []
        self.receive_data_dict = {}
        self.left_data = ""
        self.right_data = ""
        self.baojing_state = "无"
        self.guzhang_state = "无"
        self.shouming_state = "无"
        self.zijian_state = "无"
        self.device_state = "正常"
        self.device_nongdu = "0"

        self._serial = None
        self._is_connected = False

    def connect(self, timeout=60):
        """
        连接设备
        """
        self._serial = serial.Serial()
        self._serial.port = self.port
        self._serial.baudrate = self.baudrate
        self._serial.bytesize = int(self.bytesize)
        self._serial.parity = self.parity
        self._serial.stopbits = int(self.stopbits)
        self._serial.timeout = timeout

        try:
            self._serial.open()
            if self._serial.isOpen():
                self._is_connected = True
        except Exception as e:
            self._is_connected = False
            logger.error(e)

    def disconnect(self):
        """
        断开连接
        """
        if self._serial:
            self._serial.close()

        #     def write(self, data, isHex=True):

    #         """
    #         发送数据给串口设备
    #         """
    #         if self._is_connected:
    #             # fontCode = "utf-8"
    #             if isHex:
    #                 # https://wiki.python.org/moin/Python3UnicodeDecodeError
    #                 # data=re.sub('[^ 0-9a-fA-F]', '', data)      #删除非法字符
    #                 # if len(data)%2==1:
    #                 #     data=data[:-1]
    #                 # data = binascii.unhexlify(data).decode('iso-8859-1')
    #                 data = binascii.unhexlify(data)
    #                 logger.info(data,"发送的转化数据=============================")
    # #            else :
    # #                if platform.system() == "Windows":
    # #                    fontCode = "gbk"
    #             self._serial.write(data)

    def write(self, data, isHex=False):
        if self._is_connected:
            if self._serial.isOpen():
                if isHex:
                    data = binascii.unhexlify(data)
                self._serial.write(data)

    def on_connected_changed(self, func):
        """
        set serial connected status change callback
        """
        tConnected = threading.Thread(target=self._on_connected_changed, args=(func,))
        tConnected.setDaemon(True)
        tConnected.start()

    def _on_connected_changed(self, func):
        """
        set serial connected status change callback
        """
        self._is_connected_temp = False
        while True:
            if platform.system() == "Windows":
                for com in list_ports.comports():
                    if com[0] == self.port:
                        self._is_connected = True
                        break
            elif platform.system() == "Linux":
                if self.port in self.find_usb_tty():
                    self._is_connected = True

            if self._is_connected_temp != self._is_connected:
                func(self._is_connected)
            self._is_connected_temp = self._is_connected
            time.sleep(0.8)

    def on_data_received(self, func):
        """
        set serial data recieved callback
        """
        tDataReceived = threading.Thread(target=self._on_data_received, args=(func,))
        tDataReceived.setDaemon(True)
        tDataReceived.start()

    def _on_data_received(self, func):
        """
        set serial data recieved callback
        """
        while True:
            if self._is_connected:
                try:
                    number = self._serial.inWaiting()
                    logger.info("读到计数", number, str(threading.current_thread().ident) + str(threading.current_thread().name))
                    if number > 0:
                        # data1 = self._serial.read(number)
                        # data1 = self._serial.readline()
                        time.sleep(0.1)
                        n = self._serial.inWaiting()
                        data = self._serial.read(n)
                        logger.info("读取的数据", n, type(data), data,
                              str(threading.current_thread().ident) + str(threading.current_thread().name))
                        if data:
                            func(data)
                    time.sleep(0.02)
                    logger.info("出来了", number, str(threading.current_thread().ident) + str(threading.current_thread().name))
                except Exception as e:
                    self._is_connected = False
                    self._serial = None
                    #                    time.sleep(0.01)
                    break

    def find_usb_tty(self, vendor_id=None, product_id=None):
        """
        查找Linux下的串口设备
        """
        tty_devs = list()
        for dn in glob.glob('/sys/bus/usb/devices/*'):
            try:
                vid = int(open(os.path.join(dn, "idVendor")).read().strip(), 16)
                pid = int(open(os.path.join(dn, "idProduct")).read().strip(), 16)
                if ((vendor_id is None) or (vid == vendor_id)) and ((product_id is None) or (pid == product_id)):
                    dns = glob.glob(os.path.join(dn, os.path.basename(dn) + "*"))
                    for sdn in dns:
                        for fn in glob.glob(os.path.join(sdn, "*")):
                            if re.search(r"\/ttyUSB[0-9]+$", fn):
                                tty_devs.append(os.path.join("/dev", os.path.basename(fn)))
            except Exception as ex:
                pass
        return tty_devs


class testHelper(object):
    def __init__(self):
        self.myserial = SerialHelper(Port="/dev/ttyS0", BaudRate="9600")
        # self.myserial.on_connected_changed(self.myserial_on_connected_changed)

    def write(self, data):
        self.myserial.write(data, True)

    def myserial_on_connected_changed(self, is_connected):
        if is_connected:
            logger.info("Connected")
            self.myserial.connect()
            self.myserial.on_data_received(self.myserial_on_data_received)
        else:
            logger.info("DisConnected")

    def myserial_on_data_received(self, data):
        logger.info("打印的数据：", data)


if __name__ == '__main__':
    myserial = testHelper()
    myserial.myserial_on_connected_changed(is_connected=True)

    time.sleep(1)
    # myserial.write("7EF9010000FA7E")
    count = 0
    while count < 1000:
        logger.info("Count: %s" % count)
        time.sleep(1)
        count += 1
