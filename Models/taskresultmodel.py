# coding=utf-8


class TaskResultModel:
    def __init__(self, taskid, taskstatus, scriptstatus, result, tasktime, node=''):
        self.taskid = taskid
        self.taskstatus = taskstatus
        self.scriptstatus = scriptstatus
        self.result = result
        self.tasktime = tasktime
        self.node = node
