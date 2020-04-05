# ！/usr/bin/python3.6
# coding:utf-8
import os, traceback, sys
# from Utils import mylog
# log = mylog.Log().getInstance()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    def __init__(self):
        self.MQ_URL = '172.22.139.13'
        self.MQ_PORT = 5672
        self.MQ_SCAN_QUEUE = "prod_scan_queue"
        self.MQ_SCAN_QUEUE_PRIO = 3
        self.MQ_HEART_EXCHANGE = "prod_heart_exchange"
        self.MQ_HEART_EXCHANGE_TYPE = "fanout"
        self.MQ_RESULT_EXCHANGE = "prod_result_exchange"
        self.MQ_RESULT_EXCHNAGE_TYPE = "fanout"
        self.MQ_USER = "test"
        self.MQ_PASS = "88888888"
        # ======= REDIS =======
        self.REDIS_URL = "127.0.0.1"
        self.REDIS_PORT = 6379
        self.REDIS_PASS = "davy811220"
        self.REDIS_DB = 0
        # 心跳频率
        self.HEART_RATE = 60


    # 从环境变量中读取并解析配置
    def get_env(self):
        mq_info_str = os.environ.get('MQ_ENV')          # test:88888@1.2.3.4:5555
        print("MQ_ENV:", mq_info_str)
        mq_scan_str = os.environ.get('MQ_SCAN_ENV')     # queuename:max priority   scan_queue:3
        print("MQ_SCAN_ENV:", mq_scan_str)
        mq_heart_str = os.environ.get('MQ_HEART_ENV')     # exchangename:exchangetype   proc_heart_exchange:fanout
        print("MQ_HEART_ENV:", mq_heart_str)
        mq_result_str = os.environ.get('MQ_RESULT_ENV')     # queuename:max priority   proc_result_exchange:fanout
        print("MQ_RESULT_ENV:", mq_result_str)
        redis_info_str = os.environ.get('REDIS_ENV')    # db_num:password@ip:port
        print("REDIS_ENV:", redis_info_str)
        heart_rate = os.environ.get('HEART_RATE')
        print("HEART_RATE:", heart_rate)
        try:
            if heart_rate is not None:
                self.HEART_RATE = int(heart_rate)
            if mq_info_str is not None:
                mq_info = str(mq_info_str).strip().split('@')
                if len(mq_info) != 2:
                    raise Exception('analysis mq_env length not equal 2, failed.')
                # 整理 MQ相关的
                mq_info_account = mq_info[0].split(':')
                self.MQ_USER = mq_info_account[0].strip()
                self.MQ_PASS = mq_info_account[1].strip()
                mq_info_url = mq_info[1].split(':')
                self.MQ_URL = mq_info_url[0].strip()
                self.MQ_PORT = int(mq_info_url[1].strip())
            if mq_scan_str is not None:
                mq_tmp = mq_scan_str.split(":")
                self.MQ_SCAN_QUEUE = mq_tmp[0].strip()
                self.MQ_SCAN_QUEUE_PRIO = int(mq_tmp[1].strip())
            if mq_heart_str is not None:
                mq_tmp = mq_heart_str.split(':')
                self.MQ_HEART_EXCHANGE = mq_tmp[0]
                self.MQ_HEART_EXCHANGE_TYPE = mq_tmp[1]
            if mq_result_str is not None:
                mq_tmp = mq_result_str.split(':')
                self.MQ_RESULT_EXCHANGE = mq_tmp[0]
                self.MQ_RESULT_EXCHNAGE_TYPE = mq_tmp[1]

            # 整理redis相关的  db_num:password@ip:port
            if redis_info_str is not None:
                redis_info = str(redis_info_str).strip().split('@')
                if len(redis_info) != 2:
                    raise Exception('analysis redis_env length not equal 2, failed.')
                redis_tmp = redis_info[0].split(':')
                if len(redis_tmp) != 2:
                    self.REDIS_DB = 0
                    self.REDIS_PASS = ''
                else:
                    self.REDIS_DB = int(redis_tmp[0].strip())
                    self.REDIS_PASS = redis_tmp[1].strip()
                redis_tmp = redis_info[1].split(':')
                self.REDIS_URL = redis_tmp[0].strip()
                self.REDIS_PORT = int(redis_tmp[1].strip())
        except Exception as err:
            print('analysis env args failed. ', err)
            sys.exit(-1)


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.get_env()
        # 自定义一些测试环境变量值
        self.MQ_URL = '172.22.139.13'
        self.MQ_SCAN_QUEUE = "dev_scan_queue"
    pass


class TestingConfig(Config):
    def __init__(self):
        super().__init__()
        self.get_env()
    pass


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.get_env()
    pass


myconfig = {
    # 'development': DevelopmentConfig(),
    # 'testing': TestingConfig(),
    # 'production': ProductionConfig(),
    'default': ProductionConfig()
}


if __name__ == "__main__":
    print(myconfig['default'].MQ_URL, myconfig['default'].MQ_SCAN_QUEUE)


