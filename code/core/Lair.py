import Queue
import random
import operator
from code.core import Dragon, Egg, CoreData

__author__ = 'Llanowar'

class Lair(object):
    def __init__(self, coords=[0,0], gold=0):
        self._dragons = dict()
        self._dragons_orders = Queue.Queue()
        self.name = self.name()
        self._gold = 0
        self._gold = gold
        self.coords = []
        self.coords = coords
        self._eggs = dict()
        self._curr_dragon_id = 1
        self._curr_egg_id = 1
        self._pair_list = set()
        self._active_hunts = dict()
        self._dead_list = set()

    def check_egg_hatch(self):
        total_hatches = 0
        for egg in self._eggs.values():
            if egg.hatcheble:
                self.add_dragon(genes=egg.hatch())
                del self._eggs[str(egg.id)]
                total_hatches += 1
                del egg
            elif egg.age() > 100:
                del self._eggs[str(egg.id)]
                del egg
        return total_hatches

    def check_dragons_pairs(self):
        total_pairings = 0
        total_fail_pairings = 0
        total_pair_checks = 0
        #self._pair_list = list(set(self._pair_list))
        tmplst = list(self._pair_list)
        pair_one = iter(tmplst)
        try:
            while True:
                dragonne_id = pair_one.next()
                if self._dragons[str(dragonne_id)].pairing:
                    pair_id = self.find_pair(dragonne_id, tmplst)
                    total_pair_checks += 1
                    if pair_id:
                        total_pairings += 1
                        self.add_egg(parent_genes=[self._dragons[str(dragonne_id)].pair(), self._dragons[str(pair_id)].pair()])
                        tmplst.remove(dragonne_id)
                        tmplst.remove(pair_id)
                    else:
                        total_fail_pairings += 1
        except StopIteration:
            pass
        self._pair_list = set(tmplst)
        return total_pair_checks, total_pairings, total_fail_pairings


    def create(self):
        coords = [0, 0]

    def process_tasks(self):
        total_deaths = 0
        while not self._dragons_orders.empty():
            task = self._dragons_orders.get(False)
            if task[1] == 'dead':
                if self.check_one_dragon_dead(task[0]):
                    total_deaths += 1
            elif task[1] == 'pair':
                self._pair_list.add(task[0])
            elif task[1] == 'hunt':
                self._active_hunts[task[0]] = task[2]
        self.process_lists()
        return total_deaths

    def process_lists(self):
        killlist = []
        #find
        for id in self._active_hunts.keys():
            if self.already_dead(int(id)):
                killlist.append(int(id))
        for id in killlist:
            del self._active_hunts[id]
        self._pair_list.difference_update(self._dead_list)

    def make_hunt(self, id):
        target_hp = max(self._dragons[str(id)].age_cat() + random.randint(-1, 3), 1)
        target_power = 1 + target_hp*3
        dragon_attack = random.randint(1, 10) + self._dragons[str(id)].power() + self._dragons[str(id)].smart()
        if dragon_attack >= target_power:
            return target_hp * 5
        else:
            return None

    def print_all_stats(self, deaths, pair_stat, total_hatches, hunts, succ_hunts, fail_hunts):
        total_pair_checks, total_pairings, total_fail_pairings = pair_stat
        stat = self.sex_stat()
        pairs_counted = self.count_pairs()
        print 'Population %s eggs and %s dragons. %s dragons want to pair. %s males %s females. %s deaded %s hatched %s/%s of %s paired, %s/%s of %s hunts ' % \
              (len(self._eggs), len(self._dragons), pairs_counted, stat[0], stat[1], deaths, total_hatches,
               total_pairings, total_fail_pairings, total_pair_checks, succ_hunts, fail_hunts, hunts)

    def turn(self, resources_gain):
        deaths = self.process_tasks()
        pairing_stat = self.check_dragons_pairs()
        total_hatches = self.check_egg_hatch()
        remain_resource, hunts, succ_hunt, fail_hunt = self.check_hunts(resources_gain)
        #stat = self.check_lair()

        if random.randint(1, 42) == 42:
            self.print_all_stats(deaths, pairing_stat, total_hatches, hunts, succ_hunt, fail_hunt)
            print self.color_stat()

        for egg in self._eggs.values():
            egg.turn()

        for dragonne in self._dragons.values():
            dragonne.turn()

        return remain_resource

    def name(self):
        res = ' and '.join([dragon.name for dragon in self._dragons.values()]) + ' lair'
        return res

    def logic(self):
        pass

    def check_one_dragon_dead(self, id):
        #if id not in self._dead_list:
        if not self.already_dead(id):
            if self._dragons[str(id)].dead:
                dragonne = self._dragons[str(id)]
                del self._dragons[str(id)]
                self._dead_list.add(id)
                del dragonne
                return 1
        return 0

    def check_pair(self, dragonne):
        if dragonne.pairing:
            pair = self.find_pair(dragonne)
            if pair:
                return dragonne.pair(pair)
        return None

    def stat(self, dragonne):
        return '%s (%s %s) (int:%s str:%s)' % (dragonne.name, dragonne.sex, CoreData.dragon_colors[dragonne.get_gene(4)], dragonne.smart(), dragonne.power())

    def check_compatibility(self, d1_stats, d2_stats):
        diff = 0
        if d1_stats['sex'] == d2_stats['sex']: diff += 25 #sex
        diff += abs(d1_stats['color'] - d2_stats['color']) * 2 #color
        diff += abs(d1_stats['smart'] - d2_stats['smart']) #smart
        #diff -= abs(dragon1.smart() - dragon2.smart()) #strength
        if diff < 5 + d1_stats['smart'] + d2_stats['smart']:
            if d1_stats['sex'] == d2_stats['sex']: print '--> TWO MALES YIFFED %s try to yiff %s ' % (d1_stats, d2_stats)
            #if abs(dragon1.get_gene(4) - dragon2.get_gene(4)) > 0 : print '--> DIFFERENT COLORS YIFFED %s try to yiff %s ' % (self.stat(dragon1), self.stat(dragon2))
            #print ' %s try to yiff %s success with diff %s' % (stat(dragon1), stat(dragon2), diff)
            return True
        else:
            #print ' %s try to yiff %s but fail with diff %s' % (d1_stats, d2_stats, diff)
            return False

    def find_pair(self, id, pair_list):
        if len(pair_list) < 2:
            return None
        target_id = id
        tries = 0
        while target_id == id:
            target_id = random.choice(pair_list)
            tries += 1
            if tries > 3:
                return None
        if self.check_compatibility(self._dragons[str(id)].pair_stat(), self._dragons[str(target_id)].pair_stat()):
            return target_id
        return None

    def already_dead(self, id):
        return id in self._dead_list

    def count_pairs(self):
        res = 0
        for dragonne in self._dragons.values():
            if dragonne.pairing:
                res += 1
        return res

    def sex_stat(self, ):
        males = 0
        females = 0
        for dragonnee in self._dragons.values():
            if dragonnee.sex == 'male': males+=1
            elif dragonnee.sex == 'female': females+=1
            else: print 'someting strange'
        return males, females

    def color_stat(self):
        color_assembly = {}
        get = color_assembly.get
        for dragonne in self._dragons.values():
            color_assembly[str(dragonne.get_gene(4))] = get(str(dragonne.get_gene(4)), 0) + 1
        for key in color_assembly.keys():
            color_assembly[CoreData.dragon_colors[int(key)]] = color_assembly[key]
            color_assembly.pop(key, None)
        return color_assembly

    def gene_stat(self):
        def count_in(_drag, num):
            res = [0 for i in range(0, 20)]
            for drag in _drag:
                res[drag.get_gene(num)] += 1
            return res

        res_genes = {str(color): 0 for color in range(0, 5)}
        for one_gene in range(0, 6):
            res_genes[str(one_gene)] = count_in(self._dragons.values(), one_gene)
        return res_genes

    def add_dragon(self, dragonne=None, genes=None):
        genes = genes or self.gene_constructor()
        if dragonne:
            dragonne._orders = self._dragons_orders
            self._dragons[str(dragonne.id)] = dragonne
        else:
            self._dragons[str(self._curr_dragon_id)] = Dragon.Dragon(orders=self._dragons_orders, id=self._curr_dragon_id, gene=genes)
            self._curr_dragon_id += 1

    def add_egg(self, egg=None, parent_genes=None):
        parent_genes = parent_genes or [self.gene_constructor(), self.gene_constructor()]
        if egg:
            self._eggs[str(egg.id)] = egg
        else:
            self._eggs[str(self._curr_egg_id)] = Egg.Egg(id=self._curr_egg_id, parent_genes=parent_genes)
            self._curr_egg_id += 1

    def gene_constructor(self):
        return [1, 1, 1, 1, random.randint(1, 10), 1]

    def check_hunts(self, resource):
        total_hunts = 0
        succ_hunts = 0
        fail_hunts = 0
        if len(self._active_hunts) > 0:
            hunt_list = [i[0] for i in sorted(self._active_hunts.iteritems(), key=operator.itemgetter(1))]
            hunt_order = iter(hunt_list)
            try:
                while resource > 0:
                    id = hunt_order.next()
                    spoil = self.make_hunt(id)
                    total_hunts += 1
                    if spoil:
                        resource -= spoil
                        self._dragons[str(id)].hunt_complete(spoil)
                        succ_hunts += 1
                    else:
                        fail_hunts += 1
            except StopIteration:
                pass
            self._active_hunts = dict()

        return resource, total_hunts, succ_hunts, fail_hunts

    def full_stats(self):
        return self.color_stat(), self.gene_stat()