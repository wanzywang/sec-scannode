# -*-coding:utf-8-*-
from redis import Redis

def do(target):
    port = '6379'
    for pwd in SEC_PASSWORD:
        try:
            conn = Redis(host=target, port=port, password=pwd)
            if conn.ping():
                return True, ("弱口令: %s" % pwd)
        except Exception as e:
            print(e)
    return False, ''