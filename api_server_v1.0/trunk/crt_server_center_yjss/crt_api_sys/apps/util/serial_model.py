import time
import serial

from sanic.log import logger


def check_config_params(cfg_class):
    if not hasattr(cfg_class, 'SERIAL_PORT'):
        raise ValueError('传输灯模块, 请正确配置 SERIAL_PORT 配置项')
    if not hasattr(cfg_class, 'SERIAL_BPS'):
        raise ValueError('传输灯模块, 请正确配置 SERIAL_BPS 配置项')
    if not hasattr(cfg_class, 'SERIAL_TIMEOUT'):
        raise ValueError('传输灯模块, 请正确配置 SERIAL_TIMEOUT 配置项')

    logger.info(f'serial config >>>')
    logger.info(f'SERIAL_PORT: {cfg_class.SERIAL_PORT}')
    logger.info(f'SERIAL_BPS: {cfg_class.SERIAL_BPS}')
    logger.info(f'SERIAL_TIMEOUT: {cfg_class.SERIAL_TIMEOUT}')
    logger.info(f' <<<')


class SerialFactory:
    cfg_class = None
    serial_port = None
    serial_bps = None
    serial_timeout = None
    _ser = None

    def __init__(self):
        pass

    @classmethod
    def from_config(cls, cfg_class):
        """
            本函数, 系统初始化时, 需被调用执行
        :param cfg_class:
        :return:
        """
        # check config class
        check_config_params(cfg_class)

        cls.cfg_class = cfg_class
        cls.serial_port = cfg_class.SERIAL_PORT
        cls.serial_bps = cfg_class.SERIAL_BPS
        cls.serial_timeout = cfg_class.SERIAL_TIMEOUT

    @classmethod
    def get_serial(cls):
        if not cls.serial_port:
            raise ValueError('传输灯模块, 请先调用 from_config 进行初始化')

        if cls._ser is None:
            cls._ser = serial.Serial(cls.serial_port, cls.serial_bps, timeout=cls.serial_timeout)
        return cls._ser

    @classmethod
    def send_and_wait(cls, send_str):
        if cls._ser is None:
            cls.get_serial()
        for i in range(10):
            time.sleep(0.5)
            cls._ser.write(send_str.encode())


serial_factory = SerialFactory
