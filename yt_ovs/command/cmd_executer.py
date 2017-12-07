from abc import ABCMeta,abstractmethod
import Queue

class CmdExecuter(object):
    __metaclass__ = ABCMeta

    def __init__(self, connection):
        self.results = Queue.Queue(1)
        self.con = connection

    @abstractmethod
    def execute(self):pass

    def set_result(self, result):
        self.results.put(result)


    def get_result(self, timeout=10):
        return self.results.get(timeout=timeout)