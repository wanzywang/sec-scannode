# coding=utf-8
import logging
import logging.config
import logging.handlers
from config import myconfig
from mlogging import TimedRotatingFileHandler_MP
from os import path


class Log:
    __file = 'vhostlog'  # 日志文件名称
    __handler = False
    __fmt = '%(asctime)s - %(filename)s:[line:%(lineno)s] - %(name)s - %(message)s'# 输出格式
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Log, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        # read config
        logging.config.fileConfig(path.join(path.dirname(path.abspath(__file__)), '../logger.conf'))

        #logging.basicConfig(filename=self.__file, filemode='a+', format=self.__fmt)
        # self.__handler = logging.handlers.RotatingFileHandler(self.__file, maxBytes=1024*1024, backupCount=5)
        # 打印
        #self.__handler = logging.StreamHandler()
        #self.__handler.setLevel(logging.INFO)

        # 设置格式
        #formatter = logging.Formatter(self.__fmt)
        #self.__handler.setFormatter(formatter)
        return

    # 获取实例
    def getInstance(self):
        logger = logging.getLogger()
        #logger.addHandler(self.__handler)
        #logger.setLevel(logging.DEBUG)
        return logger

