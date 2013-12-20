import threading
from villages_and_dragons.code.network import connector
import time

__author__ = 'a.libkind'


class TaskProcessor(threading.Thread):
    def __init__(self, incoming):
        threading.Thread.__init__(self)
        self.incoming = incoming
        self.comm = connector.clientInit(connector.config, 'comm')
        self.villages = connector.clientInit(connector.config, 'villages')
        self.lairs = connector.clientInit(connector.config, 'lairs')
        self.taskproc = connector.clientInit(connector.config, 'taskproc')

    def run(self):
        while True:
            self.villages.put('Turn', False)
            print '--> i\'m taskprocessor and i\'m added one turn'
            time.sleep(5)

    def check_inc(self):
        pass

    def proceed(self):
        pass

