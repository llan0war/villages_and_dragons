import os
import pickle
import random
import time

__author__ = 'a.libkind'

config = {'port': 5000, 'authkey': 'dragonone', 'server': 'localhost'}


def serverInit(config):
    from multiprocessing import managers
    class taskList(managers.BaseManager):
        pass

    lst = []
    taskList.register('tasks', callable=lambda: lst, proxytype=managers.ListProxy)

    m = taskList(address=('', config['port']), authkey=config['authkey'])
    s = m.get_server()
    s.serve_forever()


def clientInit(config):
    from multiprocessing import managers
    class taskList(managers.BaseManager):
        pass

    taskList.register('tasks')
    m = taskList(address=(config['server'], config['port']), authkey=config['authkey'])
    m.connect()
    tasklst = m.tasks()
    return tasklst

if __name__ == '__main__':
    serverInit(config)