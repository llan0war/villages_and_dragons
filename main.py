import json
import logging
import datetime
import threading
import time
import sys
from code.core import CoreData, Village, CoreModule, Dragon
from code.network import connector
from code.server import TaskProcessor, Runner

__author__ = 'a.libkind'

logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
logger = logging.getLogger('Main thread')
logger.setLevel(logging.DEBUG)
logger.info('Log started')

buildings = CoreData.load_all()
_VILLAGES = []
_LAIRS = []
_THREADS = []
STARTTIME = datetime.datetime.now()
init_villages = False
init_lairs = False
init_core = False
init_taskprocessor = False
init_world = False
stopped = threading.Event()
vill_backup = None


def sellte(village):
    add_vilage(village.settler['gold'], village.settler['peoples'], village.settler['name'])
    village.settler['ready'] = False
    village.settler['count'] -= 1


def add_vilage(gold=25000, ppl=130, name=''):
    _VILLAGES.append(Village.Village(name=CoreData.get_village_name(name), wealth=gold, settlers=ppl, buildings=buildings))


def add_lairs():
    _LAIRS.append(Dragon.Lair())

def start_log():
    name = str(STARTTIME).replace(':', '')
    print name


def init():
    if init_core:
        print 'Initializing core'
        _THREADS.append(CoreModule.Core(stopped))
        _THREADS[-1].start()
        time.sleep(3)
    if init_taskprocessor:
        print 'Initializing taskprocessor'
        _THREADS.append(TaskProcessor.TaskProcessor(stopped))
        _THREADS[-1].start()
    if init_world:
        pass
    if init_villages:
        print 'Initializing villages'
        add_vilage()
        add_vilage()
        _THREADS.append(Runner.Runner(_VILLAGES, stopped, 'villages'))
        _THREADS[-1].start()
    if init_lairs:
        print 'Initializing dragons'
        _THREADS.append(Runner.Runner(_LAIRS, stopped, 'lairs'))
        _THREADS[-1].start()
    global comm_channel
    comm_channel = connector.clientInit(connector.config, 'comm')


if __name__ == '__main__':
    start_log()
    print 'yay, log started! '
    print connector.config
    config = sys.argv[1]
    with open(config) as f:
        cfg = json.load(f)
    print cfg
    init_villages = cfg['init_villages'] in ['True', 'true']
    init_lairs = cfg['init_lairs'] in ['True', 'true']
    init_core = cfg['init_core'] in ['True', 'true']
    init_taskprocessor = cfg['init_taskprocessor'] in ['True', 'true']
    init_world = cfg['init_world'] in ['True', 'true']
    logging.info('Starting')
    init()
    logging.info('Init complete')
    print 'Pony rules'