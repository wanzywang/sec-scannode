# coding=utf-8
import pika, json, datetime, traceback,os, requests, sys, multiprocessing,socket
import pika.exceptions, time
import ScanResult
from Models import TaskModel, taskresultmodel
from Utils import TimeUtil
from config import myconfig
from Utils import mylog
from helpers import redishelper
import VulRun
log = mylog.Log().getInstance()


"""
 从待扫描队列读取扫描任务，进行扫描
 改成了redis读取任务
"""


def receive():
    log.info("receive......")
    while True:
        try:
            task = redishelper.getonetask()
            taskid = task['id']
            plugin_url = task['url']
            module_name = task['name']
            ip = task['ip']

            if not os.path.exists(os.path.join(os.path.abspath(__file__), 'scripts', module_name + '.py')):
                try:
                    r = requests.get(plugin_url, timeout=10)
                    if r.status_code == 200:
                        with open(os.path.join(os.path.dirname(os.path.abspath("__file__")), 'scripts', module_name + ".py"),
                                  "wb") as f:
                            f.write(r.content)
                    else:
                        log.error("下载脚本失败：{}".format(r))
                        ScanResult.sendmsg(taskid, "FAIL", False, "下载脚本失败：{}".format(r), node=socket.gethostname())
                        continue
                except Exception as re:
                    log.error("收取消息后，处理失败：{},\ndetail-{}".format(re, traceback.format_exc()))
                    ScanResult.sendmsg(taskid, "FAIL", False, "下载脚本失败：{}".format(re), node=socket.gethostname())
                    continue

            ScanResult.sendmsg(taskid, "RUNNING", False, "", node=socket.gethostname())
            # 返回running
            run_proc = multiprocessing.Process(target=vul_handler, args=(module_name, ip, taskid))
            run_proc.start()
            # 等待结束
            while True:
                run_proc.join(timeout=60)
                if run_proc.is_alive():
                    if redishelper.needstop(taskid):
                        log.info("has task cancle event. {}".format(taskid))
                        run_proc.terminate()
                        run_proc.join()
                        log.info("{} : task cancel........")
                        ScanResult.sendmsg(taskid, "CANCEL", False, "",socket.gethostname())
                    else:
                        log.info("不需要提前结束，继续等待检查完成......")
                        continue
                else:
                    break
        except Exception as err:
            log.error("task basic_consume error:", traceback.format_exc())
            ScanResult.sendmsg(taskid, "FAIL", False, str(err), socket.gethostname())
            time.sleep(30)


def vul_handler(module, ip, taskid):
    log.info(" start " + module + "  ")
    # 准备进入实际脚本开始检查
    task_suc, scan_status, scan_result = VulRun.check(module, ip)
    log.info("end  {}, {}, {}".format(module, ip, " scan..."))
    if task_suc:
        task_suc = "FINISH"
    else:
        task_suc = "FAIL"
    ScanResult.sendmsg(taskid, task_suc, scan_status, scan_result,socket.gethostname())


def rec_callback(ch, method, prop, body):
    try:
        taskid = "unknown"
        scan_status = False  # 脚本检查是否认为有异常 True= 有异常
        task_suc = False  # 任务执行是否有异常
        body_msg = body.decode()
        log.info("receive task: ", body)

        msg = json.loads(body_msg, encoding='utf-8')
        taskid = msg['id']
        plugin_url = msg['url']
        module_name = msg['name']
        ip = msg['ip']

        if not os.path.exists(os.path.join(os.path.abspath(__file__), 'scripts', module_name+'.py')):
            r = requests.get(plugin_url)
            with open(os.path.join(os.path.dirname(os.path.abspath("__file__")), 'scripts', module_name + ".py"), "wb") as f:
                f.write(r.content)
        # 准备进入实际脚本开始检查
        task_suc, scan_status, scan_result = VulRun.check(module_name, ip)
        print("end to ", module_name, " scan...")
    except Exception as err:
        print('receive deal failed. ', err)
        task_suc = False
        scan_result = "执行失败，" + str(err)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    if task_suc:
        task_suc = "FINISH"
    else:
        task_suc = "FAIL"
    # 准备返回json模型
    rt = taskresultmodel.TaskResultModel(taskid=taskid, taskstatus=task_suc, scriptstatus=scan_status,
                                         result=scan_result,
                                         tasktime=TimeUtil.datetime_to_strtime(datetime.datetime.now()),
                                         node=socket.gethostname())
    # 给结果队列发送消息
    ScanResult.sendtorabbitmq(json.dumps(obj=rt.__dict__, ensure_ascii=False))


def scanmonitor():
    """ 监听扫描队列 """
    try:
        receive()
    except Exception as err:
        print("listen scan task failed. ", err)


if __name__ == "__main__":
    log.info(("{}".format(b'asfasasf')))
    res = requests.get("https://www.baidu.com")
    log.info("{}".format(res))
    # p = multiprocessing.Process(target=test)
    # p.start()
    # receive()
    # time.sleep(60)
    # r = requests.get("http://localhost/test.py")
    # with open(os.path.join(os.path.dirname(os.path.abspath("__file__")), 'scripts', "test" + ".py"), "wb") as f:
    #     f.write(r.content)
    #print(os.path.join(os.path.abspath(__file__), 'scripts', "module_name" + '.py'))
    # receive()
