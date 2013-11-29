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
        self.global_box = mail
        #active_queues.append(self.mailbox)

    def run(self):
        while True:
            data = self.mailbox.get()
            if data == 'shutdown':
                print self, 'shutting down'
                return
            print self, 'received a message:', data

    def stop(self):
        #active_queues.remove(self.mailbox)
        self.mailbox.put("shutdown")
        self.join()

class Village(Worker):
    gold = 75
    size = 0

    def addvilage(self):
        #self.mailbox.put(self.name + '_' + 'try sellte new')
        act = [self.name, 'sellte', 0]
        self.global_box.put(act)

    def pillage(self, val):
        self.gold -= val
        if self.gold < 0:
            self.gold = 0
            self.size -= 1
            self.check_life()

    def check_life(self):
        if self.size < 0:
            self.stop()


    def logic(self):
        choise = random.randint(1, 5)
        res = 0
        if choise == 1:
            if self.gold > 100:
                self.growth()
        elif choise == 2:
            if self.gold > 200:
                self.addvilage()
        elif choise == 3:
            if self.gold > 500:
                pass
        elif choise == 4:
            self.gold += (self.size ** 2) * 5
        self.gold += 1
        return res

    def growth(self):
        self.gold -= 100
        self.size += 1

    def get_status(self):
        res = str(self) + 'Size: ' + str(self.size) + ' Gold: ' + str(self.gold)
        return res

    def run(self):
        while True:
            #if self.mailbox.not_empty:
            #    data = self.mailbox.get()
            #    comm = self.parse(data)
            #if data == 'shutdown':
            #    print self, 'shutting down'
            #   return
            #print self, 'received a message:', data
            self.logic()
            time.sleep(1)
            #print self.get_status()
