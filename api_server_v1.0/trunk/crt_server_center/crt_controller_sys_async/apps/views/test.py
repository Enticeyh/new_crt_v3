import datetime
from sqlalchemy import select, delete, update

from . import BaseHandler, CfResponse, ErrorCode, redis_factory, db
from ..util.db_module.models import TabUser, TabRole, TabController, TabDevice
from ..util.async_db_api import async_load_user_by_user_name


class TestRedis(BaseHandler):
    async def post(self, request):
        try:
            login_name = request.json.get("login_name")
            password = request.json.get("password")
            await redis_factory.set_string_cache('myName', 'SunKang', redis=self.redis)  # 设置string
            my_name = await redis_factory.get_string_cache('myName', to_json=False, redis=self.redis)  # 获取string
            print(my_name)

            await redis_factory.set_hash_cache('People', {"name": "SunKang", "age": 24}, redis=self.redis)  # 设置hash
            people = await redis_factory.get_hash_cache('People', redis=self.redis)  # 获取hash
            name = await redis_factory.get_hash_item_cache('People', "name", redis=self.redis)  # 获取hash 字段
            print(name)

            is_name = await redis_factory.get_hash_exist('People', "name", redis=self.redis)  # 检查hash是否存在某字段
            print(is_name)
            is_del = await redis_factory.del_hash_item_cache('People', "name", redis=self.redis)  # 删除hash的某字段
            is_name = await redis_factory.get_hash_exist('People', "name", redis=self.redis)  # 检查hash是否存在某字段
            print(is_name)

            people = await redis_factory.get_hash_cache('People', redis=self.redis)  # 获取hash
            print(people)
            is_del = await redis_factory.del_key('People', redis=self.redis)  # 删除
            people = await redis_factory.get_hash_cache('People', redis=self.redis)  # 获取hash
            print(people)
        except Exception as e:
            self.logger.exception(e)
            return self.write_json(CfResponse(err=(1400 + 1, '无效的请求参数'), status=500))

        if login_name != 'zhangSan' or password != '123456':
            return self.write_json(CfResponse(err=(1100 + 1, '账号或密码错误'), status=403))

        data = {
            "login_name": name
        }

        return await self.write_json(CfResponse(data=data))


class TestMySql(BaseHandler):
    async def post(self, request):
        try:
            async_session = request.ctx.async_session
            print(async_session)
            # 查询记录

            # user_name = 'zhangsan'
            # user = async_load_user_by_user_name(user_name=user_name, redis=self.redis)
            # print(user)

            # session = async_session.run_sync()
            # session = async_session.sync_session
            # print(session)
            # stmt = select(TabRole).where(TabRole.id == 1)
            # result = await session.execute(stmt)
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

            # async with async_session() as session:
            #     stmt = select(TabUser).where(TabUser.id == 1)
            #     result = await session.execute(stmt)
            #     person = result.scalar()  # 返回第一列，第一行
            #     print(person)
            #     person = result.all()  # 返回所有
            #     print(person)

            # async with async_session.begin():
            #     stmt = select(TabRole).order_by(TabRole.id).limit(2)
            #     result = await async_session.execute(stmt)
            #     # records = result.scalar()  # 返回第一列，第一行
            #     # print(records)
            #     records = result.all()  # 返回所有
            #     print(records)

            # async with async_session.begin():
            #     stmt = select(TabRole).order_by(TabRole.id.desc()).limit(2)
            #     print(stmt)
            #     result = await async_session.execute(stmt)
            #     # records = result.scalar()  # 返回第一列，第一行
            #     # print(records)
            #     records = result.all()  # 返回所有
            #     print(records)

            # async with async_session.begin():
            #     qry_func = select(TabRole).where(TabRole.id == 1)
            #     record = await async_session.execute(qry_func)
            #     one_role = record.scalar_one()
            #     print(one_role)
            #     print(one_role.to_dict())

            # 新增记录
            # role_data = {
            #     "id": 1,
            #     "name": "业主管理人员"
            # }
            # async_session.add(TabRole(**role_data))
            # await async_session.flush()
            # await async_session.commit()

            # async with async_session.begin():
            #     role_data = {
            #         "id": 2,
            #         "name": "技术员"
            #     }
            #     async_session.add(TabRole(**role_data))
            #     await async_session.flush()

            # 修改记录
            # stmt = select(TabRole).where(TabRole.id == 1)
            # result = await async_session.execute(stmt)
            # person = result.scalar_one()
            # print(person.to_dict())
            # person.id = 3
            # person.name = '业主值班人员'
            # if person in async_session.dirty:
            #     await async_session.flush()
            #     await async_session.commit()

            # async with async_session.begin():
            #     stmt = select(TabRole).where(TabRole.id == 1)
            #     result = await async_session.execute(stmt)
            #     person = result.scalar_one()
            #     print(person.to_dict())
            #     person.name = '业主值班人员'
            #     if person in async_session.dirty:
            #         await async_session.flush()
            #         await async_session.commit()

            # stmt = select(TabRole).where(TabRole.id == 1)
            # result = await async_session.execute(stmt)
            # person = result.scalar_one()
            # print(person.to_dict())

            # async with db.slice_session() as session:
            #     stmt = select(TabRole).where(TabRole.id == 1)
            #     result = await session.execute(stmt)
            #     person = result.scalar_one()
            #     print(person.to_dict())
            #     person.name = '业主值班人员'
            #     if person in session.dirty:
            #         await session.flush()

            #     stmt = select(TabRole).where(TabRole.id == 1)
            #     result = await session.execute(stmt)
            #     person = result.scalar_one()
            #     print(person.to_dict())

            # async with db.slice_session() as session:
            #     stmt = select(TabRole).where(TabRole.id == 1)
            #     result = await session.execute(stmt)
            #     person = result.scalar_one()
            #     print(person.to_dict())
            #     person.name = '业主管理人员'
            #     if person in session.dirty:
            #         await session.flush()

            #     stmt = select(TabRole).where(TabRole.id == 1)
            #     result = await session.execute(stmt)
            #     person = result.scalar_one()
            #     print(person.to_dict())

            # 删除记录
            # async with async_session.begin():
            #     stmt = delete(TabRole).where(TabRole.id == 1)
            #     result = await async_session.execute(stmt)

            # async with async_session.begin():
            #     role_data = {
            #         "name": "1号控制器",
            #         "code": 123456,
            #         "model": "V1.0",
            #         "manufacturer": "南京中消"
            #     }
            #     async_session.add(TabController(**role_data))
            #     await async_session.flush()

            # 查询记录
            # records = await TabController.async_fetch_records(session=async_session)

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
