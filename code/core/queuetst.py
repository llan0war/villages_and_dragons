__author__ = 'a.libkind'

import random
import Queue
import time
import datetime

from villages_and_dragons.code.core.village import Village


stat_check = datetime.datetime.now()
active_queues = []
villages = []
dragons = []
glob_mailbox = Queue.Queue()


def checktime(per):
    if (datetime.datetime.now() - stat_check) > datetime.timedelta(seconds=per):
        return True
    return False


def status():
    if checktime(5):
        stat_check = datetime.datetime.now()
        print 'Current villages ', str(len(villages))
        for v in villages:
            print 'Village %s(%s) with %s gold  \\ %s' % (v.name, str(v.size), str(v.gold), str(glob_mailbox.qsize()))


def broadcast_event(data):
    for q in active_queues:
        q.put(data)
        #print 'messages: ', q.qsize()


def addvillage():
    villages.append(Village(randname()))
    init()

def adddragon():
    pass

def randname():
    res = ''
    for i in range(1, 10):
        res = res + str(random.randint(1, 10))
    return res


def main():
    pass


def init():
    for v in villages:
        if not v.ident:
            v.start()
            active_queues.append(v.mailbox)

def end():
    for v in villages:
        v.stop()


def messaging():
    #print glob_mailbox.empty()
    if not glob_mailbox.empty():
        data = glob_mailbox.get()
        print data

if __name__ == '__main__':
    main()
    #t1 = Worker('Yay')
    #2 = Worker('Nope')
    villages.append(Village('Hope', glob_mailbox))
    init()
    #t1.start()
    #t2.start()
    #v1.start()
    #broadcast_event("first event")
    #broadcast_event("second event")
    #broadcast_event("shutdown")

    #t1.stop()
    #t2.stop()
    while len(villages) > 0:
        time.sleep(1)
        #broadcast_event("pass")
        status()
        messaging()
        #print str()
    end()
