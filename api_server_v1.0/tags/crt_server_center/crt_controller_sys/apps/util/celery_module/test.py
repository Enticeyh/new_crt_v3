import sys

from os.path import dirname, realpath
from crt_controller_sys.apps.util.celery_module.tasks import add, controller_report


if __name__ == '__main__':
    # result = add.delay(2, 8)
    # print(result)
    # controller_report.delay(data={"controller_num": 9}, priority=9)
    # controller_report.delay(data={"controller_num": 8}, priority=8)
    # controller_report.delay(data={"controller_num": 7}, priority=7)
    # controller_report.delay(data={"controller_num": 4}, priority=4)
    # controller_report.delay(data={"controller_num": 5}, priority=5)
    # controller_report.delay(data={"controller_num": 6}, priority=6)
    # controller_report.delay(data={"controller_num": 7}, priority=7)
    # controller_report.delay(data={"controller_num": 8}, priority=8)
    controller_report.delay(1, 9)
    # controller_report.delay(data={"controller_num": 9})
    # controller_report.delay(data={"controller_num": 9})
    # controller_report.apply_async(data={"controller_num": 9}, priority=9)
    # add.delay(1, 9)
    # add.delay(1, 9)
    # add.delay(1, 9)
    # add.delay(1, 9)
