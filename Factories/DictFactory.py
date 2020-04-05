import json
from collections import Iterable

class BaseParser:
    def __init__(self, type:str, sep:str, info:str):
        self.type = type
        self.sep = sep
        self.info = info

    def get_dict(self):
        return []


class DictFactory:
    @staticmethod
    def get_parser(json_obj) -> BaseParser:
        type = json_obj['type']
        sep = ''
        if 'separate' in json_obj:
            sep = json_obj['separate']
        info = json_obj['info']
        ob = None
        if type == 'text':
            ob = TextParser(type,sep,info)
        elif type == 'separate':
            ob = SplitParser(type,sep,info)
        elif type == 'json':
            ob = JosnParser(type,sep,info)
        else:
            ob = BaseParser(type, sep, info)
        return ob


class TextParser(BaseParser):
    def get_dict(self):
        return self.info


class SplitParser(BaseParser):
    def get_dict(self):
        tmpdict = self.info.split(self.sep)
        return list(filter(None, tmpdict))


class JosnParser(BaseParser):
    def get_dict(self):
        obj = json.loads(self.info, encoding='utf-8')
        return obj

if __name__ == "__main__":
    tmp = {}
    tmp["key1"] = "123"
    if '123' in tmp:
        print("yes k")
    if 'key1' in tmp:
        print("yes keys")