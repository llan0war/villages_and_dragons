import random
import time
import datetime

__author__ = 'a.libkind'

import dragon2
import village2
import threading


_VILLAGES = []
_LAIRS = []
_THREADS = []
STARTTIME = datetime.datetime.now()
init_villages = True
init_lairs = False
stopped = threading.Event()

class Runner(threading.Thread):
    def __init__(self, data, event):
        threading.Thread.__init__(self)
        self.data = data
        self.stopped = event

    def run(self):
        while not self.stopped.wait(3):
            print 'next turn'
            settle_check = random.randint(1,10)
            for obj in self.data:
                obj.turn()
                if settle_check == 1:
                    if obj.settle:
                        add_vilage(obj)

            #if self.checktime(STARTTIME, random.randint(15, 60)):
            #    pass

    def checktime(self, prev, per):
        if (datetime.datetime.now() - prev) > datetime.timedelta(seconds=per):
            return True
        return False


def sellte(village):
    village.settle = False
    add_vilage()


def add_vilage(settlers=0):
    _VILLAGES.append(village2.Village(str(random.randint(10000, 99999)) + ' village'))


def init():
    if init_villages:
        _VILLAGES.append(village2.Village('First village'))
        #_VILLAGES.append(village2.Village('Second village'))
        _THREADS.append(Runner(_VILLAGES, stopped))
        _THREADS[-1].start()
    if init_lairs:
        _THREADS.append(Runner(_LAIRS, stopped))
        _THREADS[-1].start()


if __name__ == '__main__':
    print 'yay'
    init()
