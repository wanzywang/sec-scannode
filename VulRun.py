# coding=utf-8
import redis, json, traceback, importlib, json
from config import myconfig
from Utils import mylog
from Factories import *
log = mylog.Log().getInstance()


def get_config()->dict:
    """
    获取字典列表
    value: json data, type=text,json,separate, info=str, ep{type:"separate", separate:"|"  info:"hahah"}
    """
    # log.info(myconfig["default"].REDIS_URL)
    # log.info(myconfig["default"].REDIS_PORT)
    # log.info(myconfig["default"].REDIS_PASS)
    # log.info(myconfig["default"].REDIS_DB)
    conn = redis.Redis(host=myconfig["default"].REDIS_URL, port=myconfig['default'].REDIS_PORT,
                       password=myconfig['default'].REDIS_PASS, db=myconfig['default'].REDIS_DB)
    # conn.set("x1", "hello", ex=5)  # ex代表seconds，px代表ms
    keylist = conn.keys("SEC_*")
    internalDict = {}

    for key in keylist:
        r_value = conn.get(key)
        if r_value is None:
            continue
        json_value = json.loads(r_value)
        pars = DictFactory.get_parser(json_value)
        dict_value = pars.get_dict()
        internalDict[key] = dict_value

    return internalDict


def check(module_name, ip) -> (bool, str):
    """ 扫描的通用入口 """
    status = False              # 执行脚本，是否出现了不可控的异常
    script_check_status = False  # 脚本检查返回结果-True 存在异常， False - 不存在异常
    ret = ""
    try:
        _dic = get_config()
        scrip = importlib.import_module('scripts.' + module_name)
        for k, v in _dic.items():
            # log.info('set attr ', str(k), v)
            # print("set attr ", str(k), v)
            setattr(scrip, bytes(k).decode(encoding='utf-8'), v)
        # setattr(scrip, "PASSWORD_DIC", PASSWORD_DIC)  # 给插件声明密码字典
        # setattr(scrip, "log", log)
        log.info("准备执行啦....   " + module_name)
        script_check_status, ret = scrip.do(ip)
        log.info('执行完了.........   ' + module_name)
        status = True
    except Exception as err:
        log.info("VulRun-check failed:  {},\ndetail - {}".format(err, traceback.format_exc()))
        status = False
        ret = str(err.args)
    return status, script_check_status, ret


if __name__ == "__main__":
    log.info("asdf")
    # check()
    # conn = redis.Redis(host=myconfig["default"].REDIS_URL, port=myconfig['default'].REDIS_PORT,
    #                    password=myconfig['default'].REDIS_PASS, db=0)
    _dic = get_config()
    log.info('获取字典完成,共计: {}'.format( len(_dic)))
    scrip = __import__('scripts.' + 'ftpweakscan', fromlist=('ftpweakscan',))
    print('导入模块完成')
    for k, v in _dic.items():
        # log.info('set attr ', str(k), v)
        print("set attr ", bytes(k).decode(encoding='utf-8'), v)
        setattr(scrip, bytes(k).decode(encoding='utf-8'), v)
    # setattr(scrip, "PASSWORD_DIC", PASSWORD_DIC)  # 给插件声明密码字典
    setattr(scrip,"log", log)
    print("准备执行啦....")
    script_check_status, ret = scrip.do("ip")
    print('执行完了.........')