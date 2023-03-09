import datetime
from sqlalchemy import select, delete, update

from . import BaseHandler, CfResponse
from crt_controller_sys.apps.util.err_code import ErrorCode
from crt_controller_sys.apps.util.redis_module.redis_factory import redis_factory
from crt_controller_sys.apps.util.db_module.sqlalchemy_factory import db_factory as db
from crt_controller_sys.apps.util.db_module.models import TabUser, TabRole, TabController, TabDevice
from crt_controller_sys.apps.util.sync_db_api import sync_load_user_by_user_name, sync_load_device_type
from crt_controller_sys.apps.util.celery_module.task_sender import send_check_reset_error_data


class TestRedis(BaseHandler):
    async def post(self, request):
        try:
            login_name = request.json.get("login_name")
            password = request.json.get("password")
            redis_factory.set_string_cache('myName', 'SunKang', conn=self.conn)  # 设置string
            my_name = redis_factory.get_string_cache('myName', to_json=False, conn=self.conn)  # 获取string
            print(my_name)

            redis_factory.set_hash_cache('People', {"name": "SunKang", "age": 24}, conn=self.conn)  # 设置hash
            people = redis_factory.get_hash_cache('People', conn=self.conn)  # 获取hash
            name = redis_factory.get_hash_item_cache('People', "name", conn=self.conn)  # 获取hash 字段
            print(name)

            is_name = redis_factory.get_hash_exist('People', "name", conn=self.conn)  # 检查hash是否存在某字段
            print(is_name)
            is_del = redis_factory.del_hash_item_cache('People', "name", conn=self.conn)  # 删除hash的某字段
            is_name = redis_factory.get_hash_exist('People', "name", conn=self.conn)  # 检查hash是否存在某字段
            print(is_name)

            people = redis_factory.get_hash_cache('People', conn=self.conn)  # 获取hash
            print(people)
            is_del = redis_factory.del_key('People', conn=self.conn)  # 删除
            people = redis_factory.get_hash_cache('People', conn=self.conn)  # 获取hash
            print(people)
        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=(1400 + 1, '无效的请求参数'), status=500))

        if login_name != 'zhangSan' or password != '123456':
            return await self.write_json(CfResponse(err=(1100 + 1, '账号或密码错误'), status=403))

        data = {
            "login_name": name
        }

        return await self.write_json(CfResponse(data=data))


class TestMySql(BaseHandler):
    async def post(self, request):
        try:
            session = request.ctx.session
            print(session)

            # 查询记录
            # user_name = 'zhangsan'
            # user = sync_load_user_by_user_name(user_name=user_name, conn=self.conn)
            # print(user)

            # session = async_session.run_sync()
            # session = async_session.sync_session
            # print(session)
            # stmt = select(TabRole).where(TabRole.id == 1)
            # result = session.execute(stmt)
            # person = result.scalar()  # 返回第一列，第一行
            # print(person)

            # from sqlalchemy import create_engine
            # engine = create_engine('mysql+pymysql://root:123456@112.124.25.173:13306/crt_test', echo=True, future=True)
            # from sqlalchemy.orm import Session
            # session = Session(engine)
            # print(session)
            # stmt = select(TabRole).where(TabRole.id == 1)
            # person = session.scalars(stmt)
            # for user in person:
            #     print(user.to_dict())

            # with session.begin():
            #     stmt = select(TabRole).order_by(TabRole.id).limit(2)
            #     result = session.execute(stmt)
            #     records = result.scalar()  # 返回第一列，第一行
            #     print(records.to_dict())
            #     records = result.scalars().all()  # 返回所有
            #     records = [record.to_dict() for record in records]
            #     print(records)

            # with session.begin():
            #     qry_func = select(TabRole).where(TabRole.id == 1)
            #     record = session.execute(qry_func)
            #     one_role = record.scalar_one()
            #     print(one_role)
            #     print(one_role.to_dict())

            # stmt = select(TabRole).where(TabRole.id == 1)
            # result = session.execute(stmt)
            # role = result.scalar_one()
            # print(role.to_dict())

            # 新增记录
            # role_data = {
            #     "name": "其他"
            # }
            # session.add(TabRole(**role_data))
            # session.flush()
            # session.commit()

            # with session.begin():
            #     role_data = {
            #         "name": "其他2"
            #     }
            #     session.add(TabRole(**role_data))
            #     session.flush()

            # with session.begin():
            #     role_data = {
            #         "name": "2号控制器",
            #         "code": 1234567,
            #         "model": "V1.0",
            #         "manufacturer": "南京中消"
            #     }
            #     session.add(TabController(**role_data))
            #     session.flush()

            # 修改记录
            # stmt = select(TabRole).where(TabRole.id == 4)
            # result = session.execute(stmt)
            # role = result.scalar_one()
            # print(role.to_dict())
            # role.name = '其他6'
            # if role in session.dirty:
            #     session.flush()
            #     session.commit()

            # with session.begin():
            #     stmt = select(TabRole).where(TabRole.id == 5)
            #     result = session.execute(stmt)
            #     role = result.scalar_one()
            #     print(role.to_dict())
            #     role.name = '其他'
            #     if role in session.dirty:
            #         session.flush()

            # with db.slice_session() as session:
            #     stmt = select(TabRole).where(TabRole.id == 5)
            #     result = session.execute(stmt)
            #     role = result.scalar_one()
            #     print(role.to_dict())
            #     role.name = '业主值班人员'
            #     if role in session.dirty:
            #         session.flush()
            #
            #     stmt = select(TabRole).where(TabRole.id == 5)
            #     result = session.execute(stmt)
            #     person = result.scalar_one()
            #     print(person.to_dict())

            # with db.slice_session() as session:
            #     update_fun = update(TabDevice).where(TabDevice.is_delete == 0).values(TabDevice.alarm == 0)
            #     print(update_fun)

            # 删除记录
            # with session.begin():
            #     stmt = delete(TabRole).where(TabRole.id == 5)
            #     session.execute(stmt)

            # 查询记录
            # records = await TabController.async_fetch_records(session=session)
            # records = sync_load_user_by_user_name(user_name='wangwu', conn=self.conn)
            # records = sync_load_device_type(page=0, conn=self.conn, fast_to_dict=True)
            # for record_id, record in records.items():
            #     print(f'{record_id}: {record}')
            # print(records)

            send_check_reset_error_data()

        except Exception as e:
            self.logger.exception(e)
            return await self.write_json(CfResponse(err=(1400 + 1, '无效的请求参数'), status=500))

        areas = [
            {
                'name': '小区名称',
                'area': '小区',
                'buildings_units': [
                    {
                        'name': '楼宇_单元名称',
                        'building': '楼宇',
                        'unit': '单元',
                        'floors_district': [
                            {
                                'name': '楼层分区名称',
                                'floor': '楼层',
                                'district': '分区'
                            }
                        ]
                    }
                ]
            }
        ]

        records = areas

        return await self.write_json(CfResponse(data=records))
