import os


def readfirstline(filename) -> str:
    ver = ""
    try:
        if not os.path.exists(filename):
            os.mknod(filename)
        with open(filename, 'r') as f:
            ver = f.readline()
            f.close()
        return ver
    except:
        return ""


def write(filename, content=""):
    try:
        with open(filename, 'w') as f:
            f.write(content)
            f.close()
    except Exception as err:
        print("write file failed.", err)

