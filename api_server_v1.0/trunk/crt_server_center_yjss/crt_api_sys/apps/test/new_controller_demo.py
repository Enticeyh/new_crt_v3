import requests
import json

from concurrent.futures import ThreadPoolExecutor


base_url = 'http://192.168.8.102:8013/cf/api/v1/crt'


def do_test_test_api():
    url = f'{base_url}/test_api'
    resp = requests.get(url)
    print(resp.text)


def do_test_qry_api():
    data = {
        "crt_sn": "1234",
        "datetime": "2022-06-23 11:12:12",
        "sdjflsdkf": 2
    }
    headers = {
        "Connection": "close",
    }
    url = f'{base_url}/qry_state_api'
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    print(resp.text)


import time

def do_test():
    succ = 0
    fail = 0
    for i in range(5000):
        try:
            do_test_test_api()
            do_test_qry_api()
            # time.sleep(.01)
        except Exception as e:
            print(e)
            fail += 1
        else:
            succ += 1

    # do_test_qry_api()


if __name__ == '__main__':
    do_test()
