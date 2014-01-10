import Queue
import random
import time
from code.core import Village, CoreData

__author__ = 'a.libkind'

class Kingdom(object):
    def __init__(self):
        self._orders = Queue.Queue()
        self._village_cur_id = 10000
        self._villages = dict()
        self.settlers = []
        self._raidlist = dict()
        self._settlelist = set()

    def turn(self):
        #process tasks
        self.process_tasks()
        #find dead
        #make new
        self.check_settlers()
        #make raids
        self.check_raids()
        #make turns
        for vill in self._villages.keys():
            self._villages[vill].turn()

    def logic(self):
        pass

    def process_tasks(self):
        while not self._orders.empty():
            task = self._orders.get(False)
            if task[1] == 'raid':
                self._raidlist[task[0]] = [task[2], task[3]] # id: [target, power]
            if task[1] == 'settle':
                self._settlelist.add(task[0])

    def check_raids(self):
        for vill_id in self._raidlist.keys():
            vill = self._villages[vill_id]
            if not self._raidlist[vill_id][0]:
                prize_gold, loss = self.event_raid(self._raidlist[vill_id][1])
            else:
                prize_gold, loss = 0, 0
            if prize_gold > 0:
                vill.logger.info(' %s found enemy and win for %s gold ', vill.name, str(prize_gold))
                vill.add_gold(prize_gold)
            else:
                vill.logger.info(' %s found enemy and fail', vill.name)
                vill.add_warrior(-loss)
        self._raidlist.clear()

    def event_raid(self, power):
        prize_gold = 0
        loss = 0
        if random.randint(1, 10) > 3: #target found
            enemy_strength = random.randint(0, 100)
            if power * random.randint(1, 5) - enemy_strength > 0:
                prize_gold = random.randint(1, 5) * enemy_strength
            else:
                prize_gold = 0
                loss = int(power * random.randint(1, 5) / 10)
        return prize_gold, loss

    def add_village(self, vill=None, gold=None, ppl=None):
        if vill:
            pass
        else:
            new_vill = Village.Village(gold=gold, peoples=ppl, orders=self._orders, name=CoreData.get_village_name(), id_pref=self._village_cur_id)
            self._villages[new_vill.id] = new_vill
            self._village_cur_id += 1

    def remove_village(self):
        pass

    def check_settlers(self):
        for vill_id in self._settlelist:
            if self._villages[vill_id].ready_to_settle:
                settl = self._villages[vill_id].complete_settle()
                if settl:
                    self.add_village(gold=settl[0], ppl=settl[1])
        self._settlelist.clear()