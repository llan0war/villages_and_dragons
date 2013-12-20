import time
import json
import datetime
from code.core import village
from code.core import core
from code.network import connector
import logging
import threading
from villages_and_dragons.code.core.dataobjects import get_name
from villages_and_dragons.code.server import TaskProcessor
from villages_and_dragons.code.server.Runner import Runner

__author__ = 'a.libkind'

logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
logger = logging.getLogger('Main thread')
logger.setLevel(logging.DEBUG)
logger.info('Log started')

_VILLAGES = []
_LAIRS = []
_THREADS = []
STARTTIME = datetime.datetime.now()
init_villages = True
init_lairs = False
init_core = False
init_taskprocessor = False
stopped = threading.Event()
vill_backup = None


def sellte(village):
    add_vilage(village.settler['gold'], village.settler['peoples'], village.settler['name'])
    village.settler['ready'] = False
    village.settler['count'] -= 1


def add_vilage(gold=25000, ppl=130, name=''):
    _VILLAGES.append(village.Village(get_name(name), gold, ppl))


def start_log():
    name = str(STARTTIME).replace(':', '')
    print name


def init():
    if init_core:
        print 'Initializing core'
        _THREADS.append(core.Core(stopped))
        _THREADS[-1].start()
        time.sleep(3)
    if init_taskprocessor:
        print 'Initializing taskprocessor'
        _THREADS.append(TaskProcessor.TaskProcessor(stopped))
        _THREADS[-1].start()
    if init_villages:
        print 'Initializing villages'
        add_vilage()
        add_vilage()
        _THREADS.append(Runner(_VILLAGES, stopped, 'villages'))
        _THREADS[-1].start()
    if init_lairs:
        print 'Initializing dragons'
        _THREADS.append(Runner(_LAIRS, stopped, 'lairs'))
        _THREADS[-1].start()
    global comm_channel
    comm_channel = connector.clientInit(connector.config, 'comm')


if __name__ == '__main__':
    start_log()
    print 'yay, log started! '
    print connector.config
    with open('config') as f:
        cfg = json.load(f)
    print cfg
    init_villages = cfg['init_villages'] in ['True', 'true']
    init_lairs = cfg['init_lairs'] in ['True', 'true']
    init_core = cfg['init_core'] in ['True', 'true']
    init_taskprocessor = cfg['init_taskprocessor'] in ['True', 'true']
    logging.info('Starting')
    init()
    logging.info('Init complete')
    print 'Pony rules'