import asyncio
import contextlib
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, TIMESTAMP, func, select
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from attrdict import AttrDict
from datetime import date, datetime
from decimal import Decimal


def logger_init(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    format_fmt = '%(asctime)s-%(levelname)s-%(filename)s-%(lineno)d: %(message)s'
    formatter = logging.Formatter(format_fmt)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.propagate = False
    return logger


logger = logger_init(logger_name='sqlalchemy_test')

# logger = logging.getLogger('sqlalchemy_test')
# logger.setLevel(logging.INFO)
# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
# logger.addHandler(ch)


Base = declarative_base()


class TabRole(Base):
    __tablename__ = 'tab_role'
    __table_args__ = {'comment': '权限表'}

    id = Column(INTEGER(11), primary_key=True, comment='ID')
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    update_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='更新时间')
    is_delete = Column(TINYINT(1), nullable=False, server_default='0', comment='是否删除（0 否 1 是）')
    name = Column(String(32), nullable=False, comment='角色名称')

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


class SQLAlchemyFactory:

    def __init__(self):
        self.cfg_class = None

        # Model Base
        self.Model = declarative_base()
        self.db_engine = None
        self.session_class = None
        self.engine_options = None
        self.session_options = None
        self.logger = None

    def from_config(self, cfg_class):
        """
            初始化
        :param cfg_class:
        :return:
        """
        self.cfg_class = cfg_class

        # create db engine
        self.db_engine = create_engine(self.cfg_class.MYSQL_URL)

    def get_session_class(self):
        session_maker = sessionmaker(bind=self.db_engine, expire_on_commit=False, **(self.session_options or {}))
        return scoped_session(session_factory=session_maker)

    @contextlib.contextmanager
    def slice_session(self):
        sess = None
        try:
            sess = self.get_session_class()
            if not sess:
                raise ValueError('sqlalchemy_factory 请先调用 from_config 进行初始化 ')
            yield sess
        except Exception as e:
            if sess:
                sess.rollback()
            raise e
        else:
            sess.commit()
        finally:
            if sess:
                sess.close()


def test(db):
    """

    :param db:
    :return:
    """
    with db.slice_session() as session:
        stmt = select(TabRole).where(TabRole.id == 1)
        result = session.execute(stmt)
        role = result.scalar_one()
        print(role.to_dict())


if __name__ == '__main__':
    db_factory = SQLAlchemyFactory()
    cfg_class = AttrDict({
        "MYSQL_URL": 'mysql+pymysql://root:123456@localhost:13306/crt_test'
    })
    logger.info(cfg_class)
    db_factory.from_config(cfg_class)

    test(db_factory)

    # loop = asyncio.get_event_loop()
    # task = loop.create_task()
    # loop.run_until_complete(task)
