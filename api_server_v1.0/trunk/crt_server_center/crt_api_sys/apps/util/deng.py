import math
import time
import serial
import serial.tools.list_ports


def SendAndWait(ser, sendstr, findstr, timeout):
    ser.write(sendstr.encode())
    timeout = math.ceil(timeout)
    time.sleep(timeout)
    result = str(ser.read_all())  # 读出串口返回值
    a = result.find(findstr)  # 找出返回值中所需要的语句作为判断条件
    # 根据自己需要对a进行应用
    return


def test(ser):
    """

    :param ser:
    :return:
    """
    # 发送串口指令
    SendAndWait(ser, "1", "", 5)  # ser是打开的串口，xxxxx是串口指令，zzzzz是需要在串口指令返回值中寻找的语句，5是timeout


if __name__ == '__main__':
    port = "/dev/ttyS2"
    bps = 9600
    timeout = 5

    ser = serial.Serial(port, bps, timeout=timeout)
    test(ser)
