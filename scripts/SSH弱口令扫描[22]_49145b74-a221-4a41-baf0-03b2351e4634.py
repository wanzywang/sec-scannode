# -*-coding:utf-8-*-
from paramiko import SSHClient, AutoAddPolicy


def do(target):
    port = 22
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    for user in SEC_USER_NAME:
        print(user)
        for pwd in SEC_PASSWORD:
            print(pwd)
            try:
                client.connect(target, port, user, pwd, banner_timeout=3000, auth_timeout=10)
                return True, ("弱口令:%s, %s" % (user, pwd))
            except Exception as e:
                print(e)
    return False, ''