# coding=utf-8
import time, traceback
import multiprocessing
from Models import ExceptionResult
from Utils import mylog
import ScanResult

log = mylog.Log().getInstance()


def recover():
    while True:
        if len(ExceptionResult.failed_list) > 0:
            log.info("recover send msg: ", ExceptionResult.failed_list)
            try:
                msg = ExceptionResult.failed_list.pop()
                # 重用一下这个方法，以后有问题就再重写吧
                ScanResult.sendtoredis(msg)
                pass
            except Exception as err:
                log.error("recover error: ", traceback.format_exc())
        time.sleep(10 * 60)
