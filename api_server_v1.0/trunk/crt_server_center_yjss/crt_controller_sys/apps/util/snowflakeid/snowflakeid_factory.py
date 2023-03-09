import time
from sanic.log import logger

# 64位ID的划分
WORKER_ID_BITS = 10
SEQUENCE_BITS = 12

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**10-1 0b1111111111

# 移位偏移计算
WORKER_ID_SHIFT = SEQUENCE_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)  # 2**12-1 0b111111111111

# Twitter元年时间戳
TW_EPOCH = 1288834974657


class IdWorker(object):
    """
    用于生成IDs
    """

    def __init__(self, worker_id, sequence=0):
        """
        初始化
        :param worker_id: 机器ID
        :param sequence: 序号
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        self.worker_id = worker_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

    @staticmethod
    def _gen_timestamp():
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            err = 'clock is moving backwards. Rejecting requests until {}'.format(self.last_timestamp)
            logger.error(err)
            raise ValueError(err)

        if timestamp <= self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - TW_EPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.worker_id << WORKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


def check_config(cfg_class):
    logger.info(f'snow flake module config >>>')
    if hasattr(cfg_class, 'worker_id'):
        logger.info(f'worker_id: {cfg_class.WORKER_ID}')
    logger.info(f' <<<')


class SnowFlakeFactory:
    _id_worker = None

    def __init__(self, worker_id=0):
        self.worker_id = worker_id
        self.cfg_class = None

    def from_config(self, cfg_class):
        # reload config
        self.cfg_class = cfg_class

        if hasattr(cfg_class, 'WORKER_ID'):
            self.worker_id = cfg_class.WORKER_ID

        check_config(cfg_class)

        # reset _id_worker
        SnowFlakeFactory._id_worker = IdWorker(self.worker_id)

    def get_id(self):
        if SnowFlakeFactory._id_worker is None:
            SnowFlakeFactory._id_worker = IdWorker(self.worker_id)
        return self._id_worker.get_id()


snow_fake_factory = SnowFlakeFactory()
snow_fake_factory.worker_id = 1
