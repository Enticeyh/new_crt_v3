from . import BaseHandler, CfResponse
from crt_controller_sys.apps.util.err_code import ErrorCode
from crt_controller_sys.apps.util.snowflakeid import snow_fake_factory
from crt_controller_sys.apps.util.celery_module.task_sender import send_check_reset_error_data, \
    send_controller_evt_synchronous


class CheckResetErrorData(BaseHandler):
    async def post(self, _):
        try:
            send_check_reset_error_data()  # 发送到队列等待异步处理

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, status=500))

        return await self.write_json(CfResponse())


class GetSnowId(BaseHandler):
    async def post(self, _):
        try:
            snow_id = snow_fake_factory.get_id()  # 发送到队列等待异步处理

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, status=500))

        return await self.write_json(CfResponse(data={"snow_id": snow_id}))


class ControllerEvtSynchronous(BaseHandler):
    async def post(self, _):
        try:
            send_controller_evt_synchronous()  # 发送到队列等待异步处理

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=ErrorCode.SVR_ERR_COMM, status=500))

        return await self.write_json(CfResponse())
