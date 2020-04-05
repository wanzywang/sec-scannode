# coding=utf-8
import multiprocessing
import ScanHandler
import HeartBeatHandler
import recovermq
import time
from Utils import mylog
log = mylog.Log().getInstance()


if __name__ == "__main__":
    # 心跳
    multiprocessing.Process(target=HeartBeatHandler.HeartMonitor, args=()).start()
    # 失败消息重试
    multiprocessing.Process(target=recovermq.recover, args=()).start()
    # 扫描
    ScanHandler.scanmonitor()
    # p = multiprocessing.Process(target=test)
    # p.start()
    # time.sleep(10)
    # p.terminate()
    # p.join()
    # print('end....12113')
