# coding=utf-8
import pika, traceback, json, datetime
from config import myconfig
from Models import ExceptionResult
from Utils import mylog
from Models import taskresultmodel
from Utils import TimeUtil
from helpers import redishelper
log = mylog.Log().getInstance()


def sendtoredis(body):
    if not redishelper.send_result(body, myconfig['default'].MQ_RESULT_EXCHANGE):
        ExceptionResult.failed_list.add(body)


def sendtorabbitmq(body):
    """给 结果 交换路由 发送消息 """
    try:
        credentials = pika.PlainCredentials(myconfig['default'].MQ_USER, myconfig['default'].MQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=myconfig['default'].MQ_URL,
                                                                       port=myconfig['default'].MQ_PORT,
                                                                       credentials=credentials))
        channel = connection.channel()
        # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
        channel.exchange_declare(exchange=myconfig['default'].MQ_RESULT_EXCHANGE, durable=True,
                                 exchange_type=myconfig['default'].MQ_RESULT_EXCHNAGE_TYPE)
        # 向队列插入数值 routing_key是队列名。delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化。routing_key 不需要配置
        channel.basic_publish(exchange=myconfig['default'].MQ_RESULT_EXCHANGE, routing_key='',
                              body=body, properties=pika.BasicProperties(delivery_mode=2))

        log.info("send result msg success. {},{}".format(myconfig['default'].MQ_RESULT_EXCHANGE, body))
        connection.close()
    except Exception as err:
        log.error("send result failed, {},{}".format(err, traceback.format_exc()))
        ExceptionResult.failed_list.add(body)
        log.warning("add send failed msg to fail_list, wait retry.")


def sendmsg(taskid, taskstatus, scriptstatus, result, node):
    rt = taskresultmodel.TaskResultModel(taskid=taskid, taskstatus=taskstatus, scriptstatus=scriptstatus,
                                         result=result,
                                         tasktime=TimeUtil.datetime_to_strtime(datetime.datetime.now()),
                                         node=node)
    # 给结果队列发送消息
    sendtoredis(json.dumps(obj=rt.__dict__, ensure_ascii=False))
