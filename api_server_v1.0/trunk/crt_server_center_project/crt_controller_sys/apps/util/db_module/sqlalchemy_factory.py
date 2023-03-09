import sys
import contextlib

from sanic.log import logger
from os.path import dirname, realpath
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

root_project_dir = dirname(dirname(dirname(dirname(realpath(__file__)))))
if root_project_dir not in sys.path:
    sys.path.append(root_project_dir)


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
        self.db_engine = create_engine(self.cfg_class.MYSQL_URL, **engine_options)

        # create logger
        self.logger = logger

        check_config(cfg_class)

    def get_session_class(self):
        session_maker = sessionmaker(bind=self.db_engine, expire_on_commit=False, **(self.session_options or {}))
        return scoped_session(session_factory=session_maker)

    @property
    def metadata(self):
        return self.Model.metadata

    def create_all(self):
        self.Model.metadata.create_all(bind=self.db_engine)
        return True

    def drop_all(self):
        self.Model.metadata.drop_all(bind=self.db_engine)
        return True

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


db_factory = SQLAlchemyFactory()
