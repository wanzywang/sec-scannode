from helpers import redishelper, filehelper
from Utils import mylog
import time, traceback, json, subprocess, importlib
log = mylog.Log().getInstance()


def __module_exist(module_name) -> bool:
    try:
        importlib.import_module(module_name)
        return True
    except:
        return False


def host_pip_install():
    while True:
        try:
            json_str = redishelper.get_pipupdate()
            if json_str is None:
                continue
            json_obj = json.loads(json_str, encoding='utf-8')
            # {"version":"1.0.0", "packages":[["install_name":"spyne","module_name":"spyne"],""], "mirror":"国内源"}
            local_ver = filehelper.readfirstline("package.ver").strip()
            all_suc = True
            if local_ver != json_obj['version']:
                log.info("pip有版本变化...")
                for p in json_obj["packages"]:
                    if p is None or len(p) == 0:
                        continue
                    if __module_exist(p['module_name']):   # 判断模块是否安装，也省得日志满天飞
                        continue
                    cmds = ["pip" + " install " + p['install_name'] + " -i " + json_obj['mirror']]
                    ret = subprocess.run(cmds, shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         encoding="utf-8")
                    log.info("pip_install: {}, return {},\nstderr:{},\nstdout:{}".format(cmds,
                              ret.returncode, ret.stderr, ret.stdout))

                    if ret.returncode != 0:
                        all_suc = False
                if all_suc:
                    filehelper.write("package.ver", json_obj['version'])
        except Exception as err:
            log.error("host_pip_install failed. {},\ndetail:{}".format(err,traceback.format_exc()))
        finally:
            time.sleep(60)


if __name__ == '__main__':
    json_str = '{"version":"1.0.0", "packages":[{"install_name":"spyne","module_name":"spyne1"},{}], "mirror":"国内源"}'
    import json
    obj =json.loads(json_str, encoding='utf-8')
    print(obj["packages"][0]["module_name"])


