# coding=utf-8
import multiprocessing
import ScanHandler
import HeartBeatHandler
import recovermq,pipmanage
import time
from Utils import mylog
log = mylog.Log().getInstance()


if __name__ == "__main__":
    # 心跳
    multiprocessing.Process(target=HeartBeatHandler.HeartMonitor, args=()).start()
    # 失败消息重试
    multiprocessing.Process(target=recovermq.recover, args=()).start()
    # pip packages 管理
    multiprocessing.Process(target=pipmanage.host_pip_install, args=()).start()
    # 扫描
    log.info("我准备好，要开始监控有没有任务了！！！！ready loop scan....")
    ScanHandler.scanmonitor()
    # p = multiprocessing.Process(target=test)
    # p.start()
    # time.sleep(10)
    # p.terminate()
    # p.join()
    # print('end....')
