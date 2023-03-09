import xlsxwriter
from io import BytesIO
from json import dumps
from sanic import Sanic
from urllib import parse
from sanic.log import logger
from datetime import datetime
from sanic.views import HTTPMethodView
from sanic.response import json, empty, HTTPResponse

from ..util.err_code import ErrorCode
from ..util.redis_module import redis_factory
from ..util.db_module.sqlalchemy_factory import db_factory as db

app = Sanic.get_app('crt_controller_sys_async')


# 生成响应结构的便捷类, 提高可读性
class CfResponse:
    def __init__(self, ok=True, code=0, msg='', data=None, err=None, status=200):
        """
            :param ok:
            :param code:
            :param msg: 存在优先级
            :param data:
            :param err:  错误码, 快捷方式, 简化赋值过程
        """
        if data is None:
            data = {}

        self.ok = ok
        self.data = data
        self.status = status
        if err:
            self.code, self.msg = err
            self.ok = False
            if msg:  # Different priorities
                self.msg = msg
        else:
            self.code = code
            self.msg = '成功'
            self.status = 200

    def to_json(self):
        return dumps({
            'ok': self.ok,
            'code': self.code,
            'msg': self.msg,
            'data': self.data,
            'status': self.status,
        })


class BaseHandler(HTTPMethodView):
    def __init__(self, *a, **kw):
        super(BaseHandler, self).__init__(*a, **kw)

        # self.request = None

        self.redis = app.config.REDIS
        self.logger = logger
        # self.login_data = None

        self.conn = None  # redis_module 连接
        self.start_time = 0  # 请求开始处理时间
        # self.json_args = None  # json 请求参数

    # async def options(self, request):
    #     self.logger.info(f'{request}')
    #     headers = {
    #         "Access-Control-Allow-Origin": "mydomain.com",
    #         "Access-Control-Allow-Credentials": "true",
    #         "Access-Control-Allow-Headers": (
    #             "origin, content-type, accept, "
    #             "authorization, x-xsrf-token, x-request-id"
    #         ),
    #     }
    #     return empty(headers=headers)

    async def write_json(self, obj):
        self.logger.debug(f'{obj}')
        response_data = {
            'ok': obj.ok,
            'code': obj.code,
            'msg': obj.msg,
            'data': obj.data
        }
        return json(response_data, status=obj.status)

    async def write_excel(self, file_name, datas, mapping):
        """
            提供 excel 下载功能, 可以第一版 zp 的版本保持一致
        :param file_name:
        :param datas:
        :param mapping:
        :return:
        """

        self.logger.debug(f'生成excel文件')

        # 1 生成 excel
        title_heads = list([title for title, _ in mapping])

        file_name = file_name + '-' + datetime.now().strftime('%Y%m%d')

        output = BytesIO()
        # 创建Excel文件,不保存, 直接输出
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # 设置Sheet的名字
        worksheet = workbook.add_worksheet(file_name)
        # 表头
        worksheet.write_row(0, 0, title_heads)
        title_heads_len = len(title_heads)

        row = 1
        for data in datas:
            for i in range(title_heads_len):
                title = mapping[i][1]['title']
                value = data[title]
                mapping_value = mapping[i][1].get('value', None)
                if mapping_value is not None:
                    if value is not None:
                        value = mapping_value[str(value)]
                    value = str(value)
                if value is None:
                    value = ''
                worksheet.write_string(row, i, f'{value}')
            row += 1
        workbook.close()

        headers = {
            'Content-Type': f"attachment; filename={parse.quote(file_name)}.xlsx",
            'Cache-Control': "no-cache",
            'Content-Disposition': f"attachment; filename={parse.quote(file_name)}.xlsx",
            'filename': parse.quote(file_name),
            "Access-Control-Expose-Headers": 'filename'
        }

        http_response = HTTPResponse(body=output.getvalue(), headers=headers, content_type='application/vnd.ms-excel')

        return http_response


def get_args(request, name, default=None, field_type=str):
    val = request.args.get(name, default)

    if (field_type != str) and (val is not None):
        val = field_type(val)

    return val
