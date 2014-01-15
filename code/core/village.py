import random
from code.core import CoreData
from code.server import Logger

__author__ = 'a.libkind'


class Village(Logger.LogMe):
    def __init__(self, orders, localmap=None, id_pref=None, name=None, gold=None, peoples=None, coords=[0, 0], id=None, buildings=None):
        self.name = name or CoreData.get_village_name()
        self.gold = gold or 125
        self.peoples = peoples or 5
        self.coords = coords
        self._orders = orders
        self._localmap = localmap
        self.buildings = buildings or CoreData.load_all()
        self.id = id or self.get_id(id_pref or random.randint(10000, 99999))
        self.data_init()
        self.logger = self.getlog(self.id)
        self.create()

    def get_id(self, pref):
        return str(pref) + '#' + self.name

    def data_init(self):
        self._warriors = 0
        self.gold_inc = 0
        self.ppl_capacity = 0
        self.warr_capacity = 0
        self.EV = 0 #economic value
        self.data_array = {}
        self.structures = {}
        self.buffs = {}
        self.ready_to_settle = False
        for key in self.buildings.keys():
            self.structures[key] = {'count': 0, 'enabled': 0}
        self.data_array["coords"] = self.coords
        self.data_array["gold"] = self.gold
        self.data_array["peoples"] = self.peoples
        self.data_array["warriors"] = self._warriors
        self.data_array["structures"] = self.structures
        self.data_array["buffs"] = self.buffs
        self.settl_num = 0

    def create(self):
        coords = [0, 0]
        self.build('house')
        self.build('farm')

    def stat(self):
        prog = 'Village %s with %s (%s) gold %s (%s) peoples' % \
               (self.name, str(int(self.gold)), str(self.gold_inc), str(int(self.peoples)), str(self.ppl_capacity))
        if self.get_warriors() > 0 or self.warr_capacity > 0:
            prog = prog + ' and %s (%s) warriors' % (str(int(self.get_warriors())), str(self.warr_capacity))
        for i, j in self.structures.iteritems():
            if j['count'] > 0:
                prog = prog + ' ' + i + ':' + str(j['enabled']) + '/' + str(j['count'])
        prog = prog + ' with total EV ' + str(int(self.EV))
        prog = prog + ' and sended settlers ' + str(self.settl_num)
        return prog

    def turn(self):
        self.logger.debug(self.stat())
        if random.randint(1, 10) == 5:
            self.re_calc()
            self.calc_EV()
        self.check_disabled_buildings()
        self.calc()
        self.logic()

    def get_warriors(self):
        return self._warriors

    def add_warrior(self, count):
        self._warriors += count

    def add_gold(self, count):
        self.gold += count

    def calc_EV(self):
        EV = self.gold * 0.1 + self.peoples + self.get_warriors() * 2
        for key in self.structures:
            EV += self.structures[key]['enabled'] * self.buildings[key][0] * 0.4
            EV += self.structures[key]['count'] * self.buildings[key][0] * 0.1
        self.EV = EV

    def enable_struct(self, key):
        #gold check
        if self.buildings[key][3] < 0: #posibly lack of gold
            if self.structures[key]['enabled'] * self.buildings[key][3] + self.gold < 0: #possibly out of moneys
                if self.structures[key]['enabled'] > 0:
                    self.structures[key]['enabled'] -= 1
                    self.logger.warning(self.name, ' disable ', key, ' by gold')
            elif self.structures[key]['enabled'] < self.structures[key]['count']:
                self.structures[key]['enabled'] += 1
                self.logger.warning(self.name, ' enable ', key, ' by gold')
        if self.buildings[key][4] < 0: #same for peoples
            if self.structures[key]['enabled'] * self.buildings[key][4] + self.peoples < 0:
                if self.structures[key]['enabled'] > 0:
                    self.structures[key]['enabled'] -= 1
                    self.logger.warning(self.name, ' disable ', key, ' by ppl')
            elif self.structures[key]['enabled'] < self.structures[key]['count']:
                self.structures[key]['enabled'] += 1
                self.logger.warning(self.name, ' enable ', key, ' by ppl')

    def check_disabled_buildings(self):
        for key in self.structures.keys():
            if self.structures[key]['enabled'] - self.structures[key]['count'] < 0:
                self.enable_struct(key=key)

    def calc(self):
        self.gold += self.gold_inc
        if self.peoples < self.ppl_capacity:
            self.peoples += self.ppl_growth()
        if self.get_warriors() < self.warr_capacity:
            self.add_warrior(self.warr_growth())

    def ppl_growth(self):
        if self.peoples < 10:
            if self.get_warriors() > 0:
                self.add_warrior(-1)
                return 1
            else:
                return 0.5
        else:
            return float(int(self.peoples / 2) + int(self.get_warriors() / 4)) / 30 + 0.01 * self.structures['house']['count']

    def warr_growth(self):
        if self.structures['smith']['enabled'] > 0:
            recrut = min(self.structures['smith']['enabled'], self.warr_capacity - self.get_warriors(), self.peoples - 10)
            if recrut > 0:
                self.peoples -= recrut
                return recrut
            else:
                return 0
        else:
            return 0

    def re_calc(self):
        gold_inc = 0 #3
        for key in self.structures.keys():
            gold_inc = gold_inc + self.structures[key]['enabled'] * self.buildings[key][3]
        self.gold_inc = gold_inc

    def logic(self):
        decision = random.randint(0, 10)
        #build
        if decision == 1:
            self.build(self.choise_building())
        elif decision == 2:
            if random.randint(1, 6) > self.settl_num:
                self._start_settle()
        elif decision == 3:
            self.celebrate()
        elif decision == 4:
            self._make_raid()
        else:
            pass

    def celebrate(self):
        if self.gold > 50:
            gold_loss = random.randint(1, int(self.gold))
        else:
            gold_loss = int(self.gold / 2)
        if self.peoples > 25:
            ppl_loss = random.randint(0, int(self.peoples / 2 - 1))
        else:
            ppl_loss = 0
        self.logger.debug('%s celebrating for %s gold with %s casualities', self.name, gold_loss, ppl_loss)
        self.gold -= gold_loss
        self.peoples -= ppl_loss

    def _make_raid(self):
        if self.get_warriors() > 0:
            self._orders.put([self.id, 'raid', None, int(self.get_warriors())], False)

    def _start_settle(self):
        if self.EV > 1000 and not self.ready_to_settle and self.gold > 500 and self.peoples > 50:
            self._orders.put([self.id, 'settle'], False)
            self.ready_to_settle = True
            self.gold -= 300

    def complete_settle(self):
        if self.ready_to_settle:
            settl_gold = min(int(self.gold / 2), 1000)
            settl_ppl = min(int(self.peoples / 2), 20)
            self.peoples -= settl_ppl
            self.gold -= settl_gold
            self.ready_to_settle = False
            self.settl_num += 1
            return [settl_gold, settl_ppl]
        else:
            return None

    def choise_building(self):
        if self.ppl_capacity - self.peoples < 5:
            return 'house'
        elif self.gold < 50 or self.gold_inc < 5:
            return 'smith'
        elif self.warr_capacity - self.get_warriors() < 2:
            return 'barracks'
        elif random.randint(1, 10) > 3:
            return 'farm'
        else:
            return random.choice(self.buildings.keys())

    def build(self, type_build):
        if type_build in self.buildings.keys():
            build_template = self.buildings[type_build]
            cost_g = build_template[0] * (1.03 ** self.structures[type_build]['count'])
            cost_p = build_template[2]
            if self.gold >= cost_g:
                if self.peoples >= cost_p:
                    if self.structures[type_build]['count'] == self.structures[type_build]['enabled']:
                        res = 'successfully'
                        self.add_structure(build_template, type_build, cost_g, cost_p)
                    else:
                        res = 'but not all enabled'
                else:
                    res = 'but no such peoples'
            else:
                res = 'but cannot affroid'
            self.logger.debug('Village %s choose to build %s %s', self.name, type_build, res)

    def add_structure(self, templ, type_build, cost_g, cost_p):
        self.gold -= cost_g
        self.peoples -= cost_p
        self.gold_inc += templ[3]
        self.ppl_capacity += templ[4]
        self.warr_capacity += templ[5]
        self.structures[type_build]['count'] += 1
        self.structures[type_build]['enabled'] += 1