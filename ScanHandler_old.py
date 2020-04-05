# coding=utf-8
import pika, json, datetime, traceback,os, requests, sys,socket
import pika.exceptions
import ScanResult
from Models import TaskModel, taskresultmodel
from Utils import TimeUtil
from config import myconfig
from Utils import mylog
import VulRun
log = mylog.Log().getInstance()

""" 从待扫描队列读取扫描任务，进行扫描 """


def receive():
    while True:
        try:
            credentials = pika.PlainCredentials(myconfig['default'].MQ_USER, myconfig['default'].MQ_PASS)
            connect = pika.BlockingConnection(pika.ConnectionParameters(host=myconfig['default'].MQ_URL,
                                                                        port=myconfig['default'].MQ_PORT,
                                                                        credentials=credentials,
                                                                        heartbeat=0))
            ch = connect.channel()
            ch.basic_qos(prefetch_count=1)
            ch.queue_declare(myconfig['default'].MQ_URL, durable=True)
            try:
                ch.basic_consume(queue=myconfig['default'].MQ_SCAN_QUEUE, on_message_callback=rec_callback,
                                 auto_ack=False)
                log.info("task listening rabbitmq..")
                ch.start_consuming()
            except pika.exceptions.ChannelClosedByBroker as err:
                log.error("listen mq failed,", traceback.format_exc())
            finally:
                ch.close()
                connect.close()
        except Exception as err:
            log.error("task basic_consume error:", traceback.format_exc())


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
    log.info("hahah",b'sdfsdf')
    # r = requests.get("http://localhost/test.py")
    # with open(os.path.join(os.path.dirname(os.path.abspath("__file__")), 'scripts', "test" + ".py"), "wb") as f:
    #     f.write(r.content)
    #print(os.path.join(os.path.abspath(__file__), 'scripts', "module_name" + '.py'))
    # receive()
