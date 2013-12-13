import random
import logging

__author__ = 'a.libkind'


class Village(object):
    from code.core.dataobjects import load_all
    buildings = load_all()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self, name, wealth=125, settlers=5, coords=[0, 0], id=0):
        self.name = name
        self.gold = wealth
        self.peoples = settlers
        self.coords = coords
        self.id = self.get_id(id)
        self.data_init()
        self.create()

    def get_id(self, id):
        if id != 0:
            return id
        return str(random.randint(10000,99999)) + '#' + self.name

    def data_init(self):
        self.warriors = 0
        self.gold_inc = 0
        self.ppl_capacity = 0
        self.warr_capacity = 0
        self.EV = 0 #economic value
        self.recalc_needed = False
        self.data_array = {}
        self.structures = {}
        self.buffs = {}
        self.settler = {'ready': False, 'count': 2}
        for key in self.buildings.keys():
            self.structures[key] = {'count': 0, 'enabled': 0}
        self.data_array["coords"] = self.coords
        self.data_array["gold"] = self.gold
        self.data_array["peoples"] = self.peoples
        self.data_array["warriors"] = self.warriors
        self.data_array["structures"] = self.structures
        self.data_array["settler"] = self.settler
        self.data_array["buffs"] = self.buffs

    def create(self):
        coords = [0, 0]
        self.build('house')
        self.build('farm')

    def stat(self):
        prog = 'Village %s with %s (%s) gold %s (%s) peoples' % \
               (self.name, str(int(self.gold)), str(self.gold_inc), str(int(self.peoples)), str(self.ppl_capacity))
        if self.warriors > 0 or self.warr_capacity > 0:
            prog = prog + ' and %s (%s) warriors' % (str(int(self.warriors)), str(self.warr_capacity))
        for i, j in self.structures.iteritems():
            if j['count'] > 0:
                prog = prog + ' ' + i + ':' + str(j['enabled']) + '/' + str(j['count'])
        if self.settler['ready']:
            prog = prog + ' and settler'
        prog = prog + ' with total EV ' + str(self.EV)
        prog = prog + ' and free settlers ' + str(self.settler['count'])
        return prog

    def turn(self):
        self.logger.debug(self.stat())
        if random.randint(1,10) == 5:
            self.recalc_needed = True
        if self.recalc_needed:
            self.re_calc()
            self.calc_EV()
            self.recalc_needed = False
        for key in self.structures.keys():
            self.enable_struct(key)
        self.calc()
        self.logic()

    def calc_EV(self):
        EV = self.gold * 0.1 + self.peoples + self.warriors * 2
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

    def calc(self):
        self.gold += self.gold_inc
        if self.peoples < self.ppl_capacity:
            self.peoples += self.ppl_growth()
        if self.warriors < self.warr_capacity:
            self.warriors += self.warr_growth()

    def ppl_growth(self):
        if self.peoples < 10:
            if self.warriors > 0:
                self.warriors -= 1
                return 1
            else:
                return 0.5
        else:
            return float(int(self.peoples / 2) + int(self.warriors / 4)) / 30 + 0.01 * self.structures['house']['count']

    def warr_growth(self):
        if self.structures['smith']['enabled'] > 0:
            recrut = min(self.structures['smith']['enabled'], self.warr_capacity - self.warriors, self.peoples - 10)
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
            if self.EV > 100:
                self.settle()
        elif decision == 3:
            if self.gold > 50:
                gold_loss = random.randint(1, int(self.gold))
            else:
                gold_loss = int(self.gold / 2)
            if self.peoples > 25:
                ppl_loss = random.randint(0, int(self.peoples / 2 - 1))
            else:
                ppl_loss = 0
            self.logger.info('%s celebrating for %s gold with %s casualities', self.name, gold_loss, ppl_loss)
            self.gold -= gold_loss
            self.peoples -= ppl_loss
        elif decision == 4:
            if self.warriors > 0:
                self.raid()
        elif decision == 10:
            self.logic()
            self.logic()
        else:
            pass

    def raid(self):
        chance_find_target = self.EV - random.randint(0, 1000)
        if chance_find_target > 0: #target found
            enemy_strength = random.randint(0, 100)
            if self.warriors * random.randint(1, 5) - enemy_strength > 0:
                prize_gold = random.randint(10, 50) * enemy_strength * 0.1
                prize_ppl = 0
                if random.randint(1,10) > 5:
                    prize_ppl = random.randint(1, 5)
                self.logger.info('%s found enemy and win for %s gold and %s ppl', self.name, str(prize_gold), str(prize_ppl))
                self.gold += prize_gold
                self.peoples += prize_ppl
            else:
                self.warriors = int(self.warriors * random.randint(1,5) / 10)
                self.logger.info(' %s found enemy and fail', self.name )

    def settle(self):
        if self.settler['count'] > 0:
            if self.gold > 500 and self.peoples > 30 and not self.settler['ready']:
                self.gold -= 300
                self.settler['gold'] = int(self.gold / 2)
                self.settler['peoples'] = int(self.peoples / 2)
                self.settler['name'] = self.name + ' - '
                self.settler['ready'] = True
                self.gold -= self.settler['gold']
                self.peoples -= self.settler['peoples']
                self.logger.info(' %s send settler with %s gold and %s peoples', self.name, self.settler['gold'], self.settler['peoples'])
            else:
                self.logger.info(' %s not have such resources to make settler', self.name)

    def choise_building(self):
        if self.ppl_capacity - self.peoples < 5:
            return 'house'
        elif self.gold < 50 or self.gold_inc < 5:
            return 'smith'
        elif self.warr_capacity - self.warriors < 2:
            return 'barracks'
        elif random.randint(1, 10) > 3:
            return 'farm'
        else:
            return random.choice(self.buildings.keys())

    def build(self, type_build):
        if type_build in self.buildings.keys():
            if self.gold >= self.buildings[type_build][0] * (1.03 ** self.structures[type_build]['count']):
                if self.peoples >= self.buildings[type_build][2]:
                    if self.structures[type_build]['count'] == self.structures[type_build]['enabled']:
                        self.logger.info('Village %s choose to build %s successfully', self.name, type_build)
                        self.gold -= self.buildings[type_build][0] * (1.03 ** self.structures[type_build]['count'])
                        self.peoples -= self.buildings[type_build][2]
                        self.gold_inc += self.buildings[type_build][3]
                        self.ppl_capacity += self.buildings[type_build][4]
                        self.warr_capacity += self.buildings[type_build][5]
                        self.structures[type_build]['count'] += 1
                        self.structures[type_build]['enabled'] += 1
                    else:
                        self.logger.info('Village %s choose to build %s but not all enabled', self.name, type_build)
                else:
                    self.logger.info('Village %s choose to build %s but no such peoples', self.name, type_build)
            else:
                self.logger.info('Village %s choose to build %s but cannot affroid', self.name, type_build)