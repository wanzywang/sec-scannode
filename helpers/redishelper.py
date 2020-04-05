import redis, json, traceback, time, socket
from config import myconfig
import Utils.mylog
log = Utils.mylog.Log().getInstance()


def __get_connection():
    conn = redis.Redis(host=myconfig["default"].REDIS_URL, port=myconfig['default'].REDIS_PORT,
                       password=myconfig['default'].REDIS_PASS, db=myconfig['default'].REDIS_DB)
    return conn


def get_pipupdate():
    try:
        conn = __get_connection()
        tmp_val = conn.get("package_update")
        return tmp_val
    except Exception as err:
        log.error("get_pipupdate failed. {}, \ndetail:{}".format(err, traceback.format_exc()))
        return None



def needstop(taskid)->bool:
    try:
        conn = __get_connection()
        hostname = socket.gethostname()
        tmp_val = conn.get(hostname + "_action")
        conn.delete(hostname + "_action")
        # todo id action,以后再加操作吧
        if tmp_val is not None:
            json_obj = json.loads(tmp_val, encoding=True)
            if "id" in json_obj:
                return taskid == json_obj['id']
        return False
    except Exception as err:
        log.error("check task cancle failed. {}, \ndetail - {}".format(err,traceback))
        return False

def getonetask():
    while True:
        con = None
        try:
            con = __get_connection()
            scan_list = con.keys("task_*")
            for tmp_key in scan_list:
                tmp_val = con.get(tmp_key)
                if tmp_key is None:
                    continue
                if con.delete(tmp_key) == 0:
                    continue
                log.info("get task: {}".format(tmp_val))
                json_obj = json.loads(tmp_val, encoding='utf-8')
                return json_obj
            log.info("no task, sleep....")
            time.sleep(10)
            # json_str = con.blpop("tasklist")
            # log.info("get task: {}".format(json_str))
            # json_obj = json.loads(json_str, encoding='utf-8')
            # return json_obj
        except Exception as err:
            log.error("get one task failed.{},\ndetail - {}".format(err, traceback.format_exc()))
            time.sleep(60)
        finally:
            if con is not None:
                # log.info("close redis connection.")
                con.close()


def send_heart(heart_str, rkeyname) -> bool:
    """ 发送心跳到redis """
    try:
        conn = __get_connection()
        #conn.lpush(rkeyname, heart_str)
        extime = 3600 * 24 * 5
        conn.set(name="heart_" + socket.gethostname(), value=heart_str, ex=extime)
        conn.close()
    except Exception as err:
        log.error("send_heart failed. {}, \ndetail - {}".format(err, traceback))
        return False


def send_result(result_str, result_key) -> bool:
    """ 发送结果到结果list """
    try:
        conn = __get_connection()
        conn.rpush(result_key, result_str)
        log.info("send redis result:{},{}".format(result_key, result_str))
        conn.close()
    except Exception as err:
        log.error("send_result failed. {}, \ndetail - {}".format(err, traceback))
        return False


if __name__ == '__main__':
    c = __get_connection()
    print(c.get("packages"))
