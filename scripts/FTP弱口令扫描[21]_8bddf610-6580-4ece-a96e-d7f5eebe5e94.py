# -*-coding:utf-8-*-
from ftplib import FTP

def do(target):
    port = 21
    for user in SEC_USER_NAME:
        print(user)
        for pwd in SEC_PASSWORD:
            print(pwd)
            try:
                ftp = FTP(target)
                ftp.connect(target, port, 20)
                if ftp.login(user, pwd).startswith('2'):
                    return True, user + '存在弱口令: ' + pwd
            except Exception as e:
                if not str(e).startswith('530'):
                    print(e)
                else:
                    print(e)
    return False, ''