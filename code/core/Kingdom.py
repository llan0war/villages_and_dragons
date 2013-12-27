import Queue
from code.core import Village, CoreData

__author__ = 'a.libkind'

class Kingdom(object):
    def __init__(self):
        self._orders = Queue.Queue()
        self._village_cur_id = 1
        self._villages = []
        self.settlers = []

    def turn(self):
        #process tasks
        #find dead
        #make new
        for vill in self._villages:
            vill.turn()

    def logic(self):
        pass

    def process_tasks(self):
        pass

    def add_village(self, vill=None):
        if vill:
            pass
        else:
            self._villages.append(Village.Village(orders=self._orders, name=CoreData.get_village_name(), id=self._village_cur_id))
            self._village_cur_id += 1

    def remove_village(self):
        pass

    def check_settlers(self):
        pass