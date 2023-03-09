import datetime

from . import BaseHandler, CfResponse, ErrorCode
from ..util.celery_module.task_sender import adjust_time, report_info
# from ..util.redis_query.query_sender import controller_report


class AdjustTime(BaseHandler):
    async def get(self, request):
        self.logger.info(f'reports：{request.json}')

        # filename = 'D:\\Desktop\\old_controller_adjustTime.txt'
        filename = '/mnt/d/Desktop/old_controller_adjustTime.txt'

        with open(filename, 'a') as file_object:
            file_object.write(f'heartBeats：{request.json}\n')

        try:
            device_num = int(request.args.get("page", 0))
        except Exception as e:
            self.logger.exception(e)
            return self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_LACK))

        adjust_time(device_num)

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
            all_data = request.json.get("data")

            self.logger.info(f'reports：{all_data}')

            # filename = 'D:\\Desktop\\old_controller_reports.txt'
            filename = '/mnt/d/Desktop/old_controller_reports.txt'

            with open(filename, 'a') as file_object:
                file_object.write(f'heartBeats：{request.json}\n')

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.BUSINESS_ERR_PARAMS_INVALID, status=500))

        try:
            for data in all_data:
                device_num = int(data.get("device_num", 0))  # 控制器号
                loop_num = int(data.get("loop_num", 0))  # 回路号
                addr_num = int(data.get("addr_num", 0))  # 地址号

                equipment_num = int(data.get("equipment_num", 0))  # 设备号
                module_num = int(data.get("module_num", 0))  # 模块号

                pass_num = int(data.get("pass_num", 0))  # 通道号
                alarm_time = data.get("datetime")  # 发生时间
                event_type = int(data.get("event_type", 0))  # 报警类型
                event_state = int(data.get("event_state", 0))  # 状态 出现 消失等
                event_statetype = int(data.get("event_statetype", 0))  # 状态类型（国标事件类型）
                type = int(data.get("type", 0))  # 设备类型

                report_data = {
                    'alarm_time': alarm_time,
                    'controller_num': device_num,
                    'loop_num': loop_num,
                    'addr_num': addr_num,
                    'equipment_num': equipment_num,
                    'module_num': module_num,
                    'pass_num': pass_num,
                    'alarm_type_id': event_type,
                    'event_state': event_state,
                    'event_statetype': event_statetype,
                    'device_type_id': type,
                    'alarm_type': 0,
                }

                report_info(report_data)  # 发送到队列等待异步处理
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
        self.logger.info(f'operate：{request.json}')

        # filename = 'D:\\Desktop\\old_controller_operate.txt'
        filename = '/mnt/d/Desktop/old_controller_operate.txt'

        with open(filename, 'a') as file_object:
            file_object.write(f'heartBeats：{request.json}\n')

        data = {
            "errno": "0",
            "typeno": "0",
        }

        return await self.write_json(CfResponse(data=data))


class Heartbeats(BaseHandler):
    async def post(self, request):
        self.logger.info(f'heartBeats：{request.json}')

        # filename = 'D:\\Desktop\\old_controller_heartBeats.txt'
        filename = '/mnt/d/Desktop/old_controller_heartBeats.txt'

        with open(filename, 'a') as file_object:
            file_object.write(f'heartBeats：{request.json}\n')

        data = {
            "errno": "0",
            "typeno": "0",
            "is_check_device": 0,
            "is_check_device_status": 0
        }

        return await self.write_json(CfResponse(data=data))
