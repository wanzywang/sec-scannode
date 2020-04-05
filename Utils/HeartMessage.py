# coding=utf-8
import datetime
import socket

from Models import heartmodel
from Utils import TimeUtil
from Utils import mylog
log = mylog.Log().getInstance()


def getbody(info='') -> heartmodel.HeartModel:
    """ 生成心跳消息体 """
    server = socket.gethostname()
    local_time, local_strtime, local_timestamp = TimeUtil.current_datetime()
    active = True
    c = heartmodel.HeartModel(server=server, timespan=str(local_timestamp), active=active, info=info)
    return c
