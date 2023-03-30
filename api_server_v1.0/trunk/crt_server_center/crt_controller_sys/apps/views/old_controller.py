import os
import datetime

from . import BaseHandler, CfResponse
from crt_controller_sys.apps.util.err_code import ErrorCode
from crt_controller_sys.apps.util.snowflakeid import snow_fake_factory
from crt_controller_sys.apps.util.celery_module.task_sender import send_controller_adjust_time, \
    send_old_controller_report, send_old_controller_operate, send_controller_heartbeats


class AdjustTime(BaseHandler):
    async def get(self, request):
        self.logger.info(f'reports：{request.json}')

        try:
            # 如果控制器类型标记为2 说明为新版控制器 需要修改为1
            if int(self.conn.get('controller_type') or 2) == 2:
                self.conn.set('controller_type', 1)
        except Exception as e:
            self.logger.exception(e)
            self.conn.set('controller_type', 1)

        try:
            device_num = int(request.args.get("page", 0))
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK))

        send_controller_adjust_time(device_num)  # 发送到队列等待异步处理

        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        data = {
            "errno": "0",
            "typeno": "1",
            "device_num": device_num,
            "datetime": str(now)
        }

        return await self.write_json(CfResponse(data=data))


class Reports(BaseHandler):
    async def post(self, request):

        try:
            if int(self.conn.get('nic_mode') or 0) == 0:
                # 修改网卡协商模式
                os.system("mii-tool -F 100baseTx-HD enp2s0")
                self.conn.set('nic_mode', 1)
        except Exception as e:
            self.logger.error("修改网卡协商模式失败！")
            self.logger.error(e)

        try:
            all_data = request.json.get("data")

            self.logger.info(f'reports：{all_data}')

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            alarm_type = all_data[0].get('alarm_type', 0)  # 从数据中取出报警类型，如果没有即为真实报警，如果值为1则为模拟报警
            for data in all_data:
                data['snow_id'] = snow_fake_factory.get_id()

            try:
                # 如果控制器类型标记为2 说明为新版控制器 需要修改为1 模拟报警不修改
                if int(self.conn.get('controller_type') or 2) == 2 and int(alarm_type) == 0:
                    self.conn.set('controller_type', 1)
            except Exception as e:
                self.logger.exception(e)
                self.conn.set('controller_type', 1)

            send_old_controller_report(all_data)  # 发送到队列等待异步处理

            # controller_report(report_data)  # 发送到队列等待异步处理

        except Exception as e:
            self.logger.exception(e)

        data = {
            "errno": "0",
            "typeno": "0",
        }

        return await self.write_json(CfResponse(data=data))


class DeviceOperateInfo(BaseHandler):
    async def post(self, request):

        try:
            # 如果控制器类型标记为2 说明为新版控制器 需要修改为1
            if int(self.conn.get('controller_type') or 2) == 2:
                self.conn.set('controller_type', 1)
        except Exception as e:
            self.logger.exception(e)
            self.conn.set('controller_type', 1)

        try:
            if int(self.conn.get('nic_mode') or 0) == 0:
                # 修改网卡协商模式
                os.system("mii-tool -F 100baseTx-HD enp2s0")
                self.conn.set('nic_mode', 1)
        except Exception as e:
            self.logger.error("修改网卡协商模式失败！")
            self.logger.error(e)

        try:
            all_data = request.json.get("data")

            self.logger.info(f'reports：{all_data}')

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            for data in all_data:
                data['snow_id'] = snow_fake_factory.get_id()
            send_old_controller_operate(all_data)  # 发送到队列等待异步处理
        except Exception as e:
            self.logger.exception(e)

        data = {
            "errno": "0",
            "typeno": "0",
        }

        return await self.write_json(CfResponse(data=data))


class Heartbeats(BaseHandler):
    async def post(self, request):

        try:
            # 如果控制器类型标记为2 说明为新版控制器 需要修改为1
            if int(self.conn.get('controller_type') or 2) == 2:
                self.conn.set('controller_type', 1)
        except Exception as e:
            self.logger.exception(e)
            self.conn.set('controller_type', 1)

        try:
            all_data = request.json.get("data")

            self.logger.info(f'reports：{all_data}')

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            send_controller_heartbeats()  # 发送到队列等待异步处理
        except Exception as e:
            self.logger.exception(e)

        data = {
            "errno": "0",
            "typeno": "0",
            "is_check_device": 0,
            "is_check_device_status": 0
        }

        return await self.write_json(CfResponse(data=data))
