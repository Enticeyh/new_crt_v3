from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import select, Column, DateTime, TIMESTAMP, text
from datetime import date, datetime
from sanic.log import logger
from decimal import Decimal
from attrdict import AttrDict

from crt_api_sys.apps.util.db_module.sqlalchemy_factory import db_factory as db

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_time = Column(TIMESTAMP, nullable=False, comment='更新时间')
    is_delete = Column(TINYINT(1), nullable=False, server_default='0', comment='是否删除（0 否 1 是）')

    @classmethod
    async def async_fetch_record_size(cls):
        """
            查询记录总数
        :return:
        """
        async with db.slice_session() as session:
            qry_func = select(cls).where(cls.is_delete == 0).order_by(cls.id)
            record = await session.execute(qry_func)
            size = record.scalar()
            return size

    @classmethod
    async def async_fetch_latest_record(cls):
        """
            查询最新一条记录
        :return:
        """
        async with db.slice_session() as session:
            qry_func = select(cls).where(cls.is_delete == 0).order_by(cls.update_time.desc())
            record = await session.execute(qry_func)
            record = record.scalars().first()
            return record.dict() if record else None

    @classmethod
    async def async_fetch_record_by_id(cls, record_id):
        """
            根据 record_id 查询记录, 可携带分片键提高效率
        :param record_id: 记录id
        :return:
        """
        if record_id is None:
            raise ValueError('Invalid Query Params')

        async with db.slice_session() as session:
            qry_func = select(cls).where(cls.is_delete == 0, cls.id == record_id)
            record = await session.execute(qry_func)
            record = record.scalars().first()
            return record.to_dict() if record else None

    @classmethod
    async def async_fetch_record_by_ids(cls, record_ids):
        """
            根据 record_id 查询记录, 可携带分片键提高效率
        :param record_ids:
        :return:
        """
        if record_ids is None:
            raise ValueError('Invalid Query Params')

        async with db.slice_session() as session:
            qry_func = select(cls).where(cls.is_delete == 0, cls.id.in_(record_ids))
            records = await session.execute(qry_func)
            records = records.scalars().all()
            return [record.to_dict() for record in records]

    @classmethod
    async def async_fetch_records(cls, limit=None):
        """
            查询所有的记录
        :param limit:
        :return:
        """
        if limit is None:
            limit = 500

        async with db.slice_session() as session:
            qry_func = select(cls).where(cls.is_delete == 0).limit(limit)
            records = await session.execute(qry_func)
            records = records.scalars().all()
            return [record.to_dict() for record in records]

    def to_dict(self, translate=True, only_business_field=True, is_attr_dict=True):
        # 对象拷贝, 类型转换,
        # 类型转换是因为某些场景存redis, datetime, Decimal 不能被序列化
        cols = [col for col in self.__table__.columns]

        resp = {}
        for col in cols:
            if only_business_field:
                if col.name in ('update_time', 'is_delete'):
                    continue

            attr_val = getattr(self, col.name)

            if attr_val is not None:
                try:
                    if (str(col.type) == 'DATETIME') and (not isinstance(attr_val, datetime)) and ('T' in attr_val):
                        attr_val = attr_val.replace('T', ' ') + ':00'
                        datetime.strptime(attr_val, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    msg = '格式化带T时间出错！'
                    logger.debug(msg)
                    logger.error(e)

                if translate:
                    if isinstance(attr_val, Decimal):
                        resp[col.name] = float(attr_val)
                    elif isinstance(attr_val, datetime):
                        resp[col.name] = str(attr_val)
                    elif isinstance(attr_val, date):
                        resp[col.name] = str(attr_val)
                    else:
                        resp[col.name] = attr_val
                else:
                    resp[col.name] = attr_val
            else:
                resp[col.name] = attr_val
        return AttrDict(resp) if is_attr_dict else resp
