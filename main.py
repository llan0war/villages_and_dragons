import pickle
import random
import datetime
from villages_and_dragons.code.core import village2
import logging
import threading

__author__ = 'a.libkind'

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info('Log started')


_VILLAGES = []
_LAIRS = []
_THREADS = []
STARTTIME = datetime.datetime.now()
init_villages = True
init_lairs = False
stopped = threading.Event()
vill_backup = None


class Runner(threading.Thread):
    def __init__(self, data, event):
        threading.Thread.__init__(self)
        self.data = data
        self.stopped = event
        self.turn_id = 0

    def run(self):
        while not self.stopped.wait(1):
            logging.info(self.turn_id, ' turn for %s villages and %s settlers' % (len(self.data), self.get_settlers_num(self.data)))
            settle_check = random.randint(1, 10)
            self.turn_id += 1
            for obj in self.data:
                obj.turn()
                if settle_check == 1:
                    if obj.settler['ready']:
                        sellte(obj)
            if self.turn_id == 42:
                name = 'db\\' + str(random.randint(10000, 99999)) + '.' + self.data[-1].name + '.dump'
                with open(name, 'w+') as f:
                    pickle.dump(self.data[-1], f)
                vill_backup = name
                print '--> backuped', self.data[-1].name
            '''if self.turn_id == 84:
                print '--> restoring ', vill_backup, ' to ', self.data[0].name
                with open(vill_backup, 'r') as f:
                    self.data[0] = pickle.load(f)'''


    def checktime(self, prev, per):
        if (datetime.datetime.now() - prev) > datetime.timedelta(seconds=per):
            return True
        return False


    def get_settlers_num(self, obj):
        res = 0
        for vill in obj:
            if vill.settler['ready']:
                res += 1
        return res


def sellte(village):
    add_vilage(village.settler['gold'], village.settler['peoples'], village.settler['name'])
    village.settler['ready'] = False
    village.settler['count'] -= 1


def get_name(pref=''):
    from villages_and_dragons.code.core.dataobjects import vill_name_dict

    def all_names():
        return [vill.name for vill in _VILLAGES]

    def check_history(name):
        if name.split(' - ') > 2:
            return name.split(' - ')[-1]
        else:
            return name

    found = False
    tries = 0
    res = check_history(pref + random.choice(vill_name_dict['part1']) + random.choice(vill_name_dict['part2']))
    while not found:
        #for vill in _VILLAGES:
        #   if vill.name == res:
        #       res = random.choice(vill_name_dict['part1']) + random.choice(vill_name_dict['part2'])
        if res in all_names():
            res = check_history(pref + random.choice(vill_name_dict['part1']) + random.choice(vill_name_dict['part2']))
            tries += 1
        else:
            found = True
        if tries > 10:
            res = 'temp' + str(random.randint(100000, 999999))
            found = True
    return res


def add_vilage(gold=25000, ppl=130, name=''):
    _VILLAGES.append(village2.Village(get_name(name), gold, ppl))


def start_log():
    name = str(STARTTIME).replace(':', '')
    print name
    logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.info('Log started')


def init():
    if init_villages:
        add_vilage()
        add_vilage()
        _THREADS.append(Runner(_VILLAGES, stopped))
        _THREADS[-1].start()
    if init_lairs:
        _THREADS.append(Runner(_LAIRS, stopped))
        _THREADS[-1].start()


if __name__ == '__main__':
    start_log()
    print 'yay'
    logging.info('Starting')
    init()
    logging.info('Init complete')
    print'yay'