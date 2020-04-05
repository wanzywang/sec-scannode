# coding=utf-8
import pika, sys
from config import myconfig
from Utils import HeartMessage
import json, traceback
import time
from helpers import redishelper
from Utils import mylog
log = mylog.Log().getInstance()


def HeartMonitor():
    while True:
        try:
            __sendheartmessage()
        except Exception as err:
            print('send heart failed. detail - ', err)
        time.sleep(myconfig['default'].HEART_RATE)


def __sendheartmessage(info=''):
    """ 给心跳订阅者发送redis消息 """
    heart_msg = json.dumps(obj=HeartMessage.getbody(info=info).__dict__, ensure_ascii=False)
    redishelper.send_heart(heart_msg, myconfig['default'].MQ_HEART_EXCHANGE)


def __sendheartmessage_mq(info=''):
    """ 给心跳订阅者发送订阅消息 """
    credentials = pika.PlainCredentials(myconfig['default'].MQ_USER, myconfig['default'].MQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=myconfig['default'].MQ_URL,
                                                                   port=myconfig['default'].MQ_PORT,
                                                                   credentials=credentials))
    channel = connection.channel()
    # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
    channel.exchange_declare(exchange=myconfig['default'].MQ_HEART_EXCHANGE, durable=True, exchange_type="fanout")
    # 向队列插入数值 routing_key是队列名。delivery_mode = 2 声明消息在队列中持久化，delivery_mod = 1 消息非持久化。routing_key 不需要配置

    channel.basic_publish(exchange=myconfig['default'].MQ_HEART_EXCHANGE, routing_key='',
                          body=json.dumps(obj=HeartMessage.getbody(info=info).__dict__, ensure_ascii=False),
                          properties=pika.BasicProperties(delivery_mode=2))

    # log.info("send heart message success.")
    # print('heart:',json.dumps(obj=HeartMessage.getbody().__dict__, ensure_ascii=False))
    connection.close()


if __name__ == "__main__":
    # HeartMonitor()
    __sendheartmessage()
