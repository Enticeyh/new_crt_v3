import os
import datetime

from . import BaseHandler, CfResponse
from crt_controller_sys.apps.util.err_code import ErrorCode
from crt_controller_sys.apps.util.snowflakeid import snow_fake_factory
from crt_controller_sys.apps.util.celery_module.task_sender import send_new_controller_state, \
    send_new_controller_alarm, send_new_controller_operate


class UpdateStateApi(BaseHandler):
    async def post(self, request):
        """系统状态采集（心跳接口）"""
        self.logger.info(f"request data {request.json}")

        try:
            # 如果控制器类型标记为2 说明为新版控制器 需要修改为1
            if int(self.conn.get('controller_type') or 2) == 1:
                self.conn.set('controller_type', 2)
        except Exception as e:
            self.logger.exception(e)
            self.conn.set('controller_type', 2)

        # 新版控制器状态更新任务
        send_new_controller_state(request.json)  # 发送到队列等待异步处理

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "datetime": str(now)
        }

        return await self.write_json(CfResponse(data=data))


class AlarmReportsApi(BaseHandler):
    async def post(self, request):
        """控制器报警事件采集"""
        self.logger.info(f"request data {request.json}")

        try:
            if int(self.conn.get('nic_mode') or 0) == 0:
                # 修改网卡协商模式
                os.system("mii-tool -F 100baseTx-HD enp2s0")
                self.conn.set('nic_mode', 1)
        except Exception as e:
            self.logger.error("修改网卡协商模式失败！")
            self.logger.error(e)

        try:
            state = {
                "ctrl_no": request.json.get("ctrl_no"),
                "evt_num": request.json.get("evt_num"),
                "is_update": request.json.get("is_update"),
                "alarm_evt_num": request.json.get("alarm_evt_num"),
                "fault_evt_num": request.json.get("fault_evt_num"),
                "feedback_evt_num": request.json.get("feedback_evt_num"),
                "action_evt_num": request.json.get("action_evt_num"),
                "supervisor_evt_num": request.json.get("supervisor_evt_num"),
                "shielding_evt_num": request.json.get("shielding_evt_num"),
                "operate_evt_num": request.json.get("operate_evt_num"),
                "vl_action_evt_num": request.json.get("vl_action_evt_num"),
                "vl_fault_evt_num": request.json.get("vl_fault_evt_num"),
                "vl_shielding_evt_num": request.json.get("vl_shielding_evt_num")
            }
            records = request.json.get("records")

            self.logger.info(f'state：{state}')
            self.logger.info(f'records：{records}')

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            # 新版控制器状态更新任务
            send_new_controller_state(state)  # 发送到队列等待异步处理

            for data in records:
                data['snow_id'] = snow_fake_factory.get_id()

            try:
                # 如果控制器类型标记为2 说明为新版控制器 需要修改为1 模拟报警不修改
                if int(self.conn.get('controller_type') or 2) == 1:
                    self.conn.set('controller_type', 2)
            except Exception as e:
                self.logger.exception(e)
                self.conn.set('controller_type', 2)

            send_new_controller_alarm(records)  # 发送到队列等待异步处理

        except Exception as e:
            self.logger.exception(e)

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "datetime": str(now)
        }

        return await self.write_json(CfResponse(data=data))


class OperateReportsApi(BaseHandler):
    async def post(self, request):
        """控制器操作事件采集"""
        self.logger.info(f"request data {request.json}")

        try:
            if int(self.conn.get('nic_mode') or 0) == 0:
                # 修改网卡协商模式
                os.system("mii-tool -F 100baseTx-HD enp2s0")
                self.conn.set('nic_mode', 1)
        except Exception as e:
            self.logger.error("修改网卡协商模式失败！")
            self.logger.error(e)

        try:
            state = {
                "ctrl_no": request.json.get("ctrl_no"),
                "evt_num": request.json.get("evt_num"),
                "is_update": request.json.get("is_update"),
                "alarm_evt_num": request.json.get("alarm_evt_num"),
                "fault_evt_num": request.json.get("fault_evt_num"),
                "feedback_evt_num": request.json.get("feedback_evt_num"),
                "action_evt_num": request.json.get("action_evt_num"),
                "supervisor_evt_num": request.json.get("supervisor_evt_num"),
                "shielding_evt_num": request.json.get("shielding_evt_num"),
                "operate_evt_num": request.json.get("operate_evt_num"),
                "vl_action_evt_num": request.json.get("vl_action_evt_num"),
                "vl_fault_evt_num": request.json.get("vl_fault_evt_num"),
                "vl_shielding_evt_num": request.json.get("vl_shielding_evt_num")
            }
            records = request.json.get("records")

            self.logger.info(f'state：{state}')
            self.logger.info(f'records：{records}')

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            # 新版控制器状态更新任务
            send_new_controller_state(state)  # 发送到队列等待异步处理

            for data in records:
                data['snow_id'] = snow_fake_factory.get_id()

            try:
                # 如果控制器类型标记为2 说明为新版控制器 需要修改为1 模拟报警不修改
                if int(self.conn.get('controller_type') or 2) == 1:
                    self.conn.set('controller_type', 2)
            except Exception as e:
                self.logger.exception(e)
                self.conn.set('controller_type', 2)

            send_new_controller_operate(records)  # 发送到队列等待异步处理

        except Exception as e:
            self.logger.exception(e)

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "datetime": str(now)
        }

        return await self.write_json(CfResponse(data=data))
