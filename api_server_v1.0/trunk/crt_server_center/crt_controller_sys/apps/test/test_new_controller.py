import aiohttp
import datetime
import asyncio


async def request_heartbeat():
    url = 'http://localhost:5000/api/v1_0/new/update_state_api'
    data = {
        "ctrl_no": 1,
        "ctrl_type": 1,
        "ctrl_state": 0,
        "evt_num": 2,
        "is_update": True,
        "alarm_evt_num": 0,
        "fault_evt_num": 1,
        "feedback_evt_num": 0,
        "action_evt_num": 0,
        "supervisor_evt_num": 0,
        "shielding_evt_num": 0,
        "operate_evt_num": 1
    }
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            async with session.post(url, json=data) as resp:
                if resp.status == 200:
                    response = await resp.text()
                    print(response)


async def request_alarm():
    url = 'http://localhost:5000/api/v1_0/new/alarm_reports_api'
    record = {
        "id": 1,
        "ctrl_num": 1,
        "dev_num": 0,
        "loop_num": 1,
        "addr_num": 1,
        "device_gb_type": 1,
        "device_state": 0,
        "evt_code": 3,
        "datetime": datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
        "channels": []
    }
    data = {
        "ctrl_no": 1,
        "evt_num": 2,
        "is_update": True,
        "alarm_evt_num": 0,
        "fault_evt_num": 1,
        "feedback_evt_num": 0,
        "action_evt_num": 0,
        "supervisor_evt_num": 0,
        "shielding_evt_num": 0,
        "operate_evt_num": 1,
        "records": [{
            "id": 1,
            "ctrl_num": 1,
            "dev_num": 0,
            "loop_num": 1,
            "addr_num": i + 150,
            "device_gb_type": 1,
            "device_state": 0,
            "evt_code": 3,
            "datetime": datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),
            "channels": []
        } for i in range(64)]
    }
    async with aiohttp.ClientSession() as session:
        for i in range(1):
            data["evt_num"] += 1
            data["alarm_evt_num"] += 1
            async with session.post(url, json=data) as resp:
                if resp.status == 200:
                    response = await resp.text()
                    print(response)


async def request_operate():
    pass


if __name__ == '__main__':
    asyncio.run(request_alarm())
    # asyncio.run(request_heartbeat())
