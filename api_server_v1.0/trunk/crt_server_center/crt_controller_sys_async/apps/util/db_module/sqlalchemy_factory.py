import contextlib

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sanic.log import logger
from asyncio import current_task


def check_config(cfg_class):
    if not hasattr(cfg_class, 'MYSQL_URL'):
        raise ValueError('db_module 模块, 请正确配置 MYSQL_URL 配置项')

    logger.info(f'mysql config >>>')
    logger.info(f'MYSQL_URL: {cfg_class.MYSQL_URL}')
    logger.info(f' <<<')


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

    def from_config(self, cfg_class, engine_options=None, session_options=None):
        """
            初始化
        :param cfg_class:
        :param engine_options:
        :param session_options:
        :return:
        """
        self.cfg_class = cfg_class
        self.engine_options = engine_options
        self.session_options = session_options

        # create db engine
        self.db_engine = create_async_engine(self.cfg_class.MYSQL_URL)

        # create logger
        self.logger = logger

        check_config(cfg_class)

    def get_session_class(self):
        session_maker = sessionmaker(bind=self.db_engine, class_=AsyncSession, expire_on_commit=False,
                                     **(self.session_options or {}))
        return async_scoped_session(session_factory=session_maker, scopefunc=current_task)

    @property
    def metadata(self):
        return self.Model.metadata

    def create_all(self):
        self.Model.metadata.create_all(bind=self.db_engine)
        return True

    def drop_all(self):
        self.Model.metadata.drop_all(bind=self.db_engine)
        return True

    @contextlib.asynccontextmanager
    async def slice_session(self):
        sess = None
        try:
            sess = self.get_session_class()
            if not sess:
                raise ValueError('sqlalchemy_factory 请先调用 from_config 进行初始化 ')
            yield sess
        except Exception as e:
            if sess:
                await sess.rollback()
            raise e
        else:
            await sess.commit()
        finally:
            if sess:
                await sess.close()


db_factory = SQLAlchemyFactory()
