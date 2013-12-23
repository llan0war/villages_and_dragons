import threading
from code.network import connector
import time

__author__ = 'a.libkind'


class TaskProcessor(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event
        self.comm = connector.clientInit(connector.config, 'comm')
        self.villages = connector.clientInit(connector.config, 'villages')
        self.lairs = connector.clientInit(connector.config, 'lairs')
        self.taskproc = connector.clientInit(connector.config, 'taskproc')
        self.world = connector.clientInit(connector.config, 'world')

    def run(self):
        while not self.stopped.wait(1):
            self.villages.put('Turn', False)
            print '--> i\'m taskprocessor and i\'m added one turn', self.villages.qsize()
            if not self.comm.empty():
                self.check_inc()
            time.sleep(5)

    def check_inc(self):
        while not self.comm.empty():
            task = self.comm.get(False)
            self.proceed(task)

    def proceed(self, task):
        print task

