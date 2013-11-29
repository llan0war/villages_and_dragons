__author__ = 'a.libkind'

import threading
import random
import Queue
import time

class Worker(threading.Thread):
    def __init__(self, nam, mail):
        threading.Thread.__init__(self, name=nam)
        self.mailbox = Queue.Queue()
        self.name = nam
        active_queues.append(self.mailbox)

    def run(self):
        while True:
            data = self.mailbox.get()
            if data == 'shutdown':
                print self, 'shutting down'
                return
            print self, 'received a message:', data

    def stop(self):
        active_queues.remove(self.mailbox)
        self.mailbox.put("shutdown")
        self.join()


class Dragon(Worker):
    level = 1
    gold = 0

    def logic(self):
        choise = random.randint(1, 10)
        res = 0
        if choise == 1:
            if self.gold > 100:
                self.growth()
        elif choise == 2:
            if self.gold > 100 and len(villages) < 5:
                self.gold -= 100
                addvillage()
        elif choise == 3:
            pass
        elif choise == 4:
            self.gold += (self.size ** 2) * 5
        self.gold += 1
        return res

    def run(self):
        while True:
            self.logic()
