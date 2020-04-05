import HeartBeatHandler
from  helpers import redishelper
import pipmanage


if __name__ == '__main__':
    # c = redishelper.__get_connection()
    # print(redishelper.get_pipupdate())
    pipmanage.host_pip_install()