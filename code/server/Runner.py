import pickle
import random
import threading
import datetime
import logging
from code.network import connector


__author__ = 'a.libkind'


class Runner(threading.Thread):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self, data, event, model):
        threading.Thread.__init__(self)
        self.data = data
        self.stopped = event
        self.turn_id = 0
        self.model = model
        self.incoming = connector.clientInit(connector.config, self.model)

    def run(self):
        while not self.stopped.wait(1):
            if not self.incoming.empty():
                command = self.incoming.get(False)
                if command == 'Turn':
                    self.make_turn()

    def make_turn(self):
        self.logger.info(' %s turn for %s villages and %s settlers', self.turn_id, len(self.data), self.get_settlers_num(self.data))
        #settle_check = random.randint(1, 10)
        self.turn_id += 1
        for obj in self.data:
            obj.turn()
            #if settle_check == 1:
            #    if obj.settler['ready']:
            #        sellte(obj)
            #if self.turn_id == 42:
            #    self.save_and_load(obj)

    def save_and_load(self, obj):
        name = 'db\\' + str(random.randint(10000, 99999)) + '.' + obj.name + '.dump'
        with open(name, 'w+') as f:
            pickle.dump(obj, f)
            #vill_backup = name
            print '--> backuped', obj.name
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