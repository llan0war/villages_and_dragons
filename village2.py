import random

__author__ = 'a.libkind'


class Village(object):
    from dataobjects import load_all
    buildings = load_all()

    def __init__(self, name, wealth=125, settlers=5, coords=[0, 0]):
        self.name = name
        self.gold = wealth
        self.peoples = settlers
        self.coords = coords

        self.data_init()
        self.create()

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
        self.settler = {'ready': False}
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
        return prog

    def turn(self):
        print self.stat()
        if random.randint(1,10) == 5: self.recalc_needed = True
        if self.recalc_needed:
            self.re_calc()
            self.calc_EV()
            self.recalc_needed = False
        for key in self.structures.keys():
            self.enable_struct(key)
        self.calc()
        self.logic()

    def calc_EV(self):
        EV = self.gold * 0.1 + self.peoples
        for key in self.structures:
            EV += self.structures[key]['enabled'] * self.buildings[key][0] * 0.4
            EV += self.structures[key]['count'] * self.buildings[key][0] * 0.1

    def enable_struct(self, key):
        #gold check
        if self.buildings[key][3] < 0: #posibly lack of gold
            if self.structures[key]['enabled'] * self.buildings[key][3] + self.gold < 0: #possibly out of moneys
                if self.structures[key]['enabled'] > 0:
                    self.structures[key]['enabled'] -= 1
                    print self.name, ' disable ', key, ' by gold'
            elif self.structures[key]['enabled'] < self.structures[key]['count']:
                self.structures[key]['enabled'] += 1
                print self.name, ' enable ', key, ' by gold'
        if self.buildings[key][4] < 0: #same for peoples
            if self.structures[key]['enabled'] * self.buildings[key][4] + self.peoples < 0:
                if self.structures[key]['enabled'] > 0:
                    self.structures[key]['enabled'] -= 1
                    print self.name, ' disable ', key, ' by ppl'
            elif self.structures[key]['enabled'] < self.structures[key]['count']:
                self.structures[key]['enabled'] += 1
                print self.name, ' enable ', key, ' by ppl'

    def calc(self):
        self.gold += self.gold_inc
        if self.peoples < self.ppl_capacity:
            self.peoples += self.ppl_growth()
        if self.warriors < self.warr_capacity:
            self.warriors += self.warr_growth()

    def ppl_growth(self):
        if self.peoples < 1:
            if self.warriors > 0:
                self.warriors -= 1
                return 1
            else:
                return 0.01
        else:
            return float(int(self.peoples / 2)) / 30 + 0.01

    def warr_growth(self):
        if self.structures['smith']['enabled'] > 0:
            recrut = min(self.structures['smith']['enabled'], self.warr_capacity - self.warriors, self.peoples - 5)
            if recrut > 0:
                self.peoples -= recrut
                return recrut
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
                gold_loss = self.gold / 2
            if self.peoples > 10:
                ppl_loss = random.randint(0, int(self.peoples - 1))
            else:
                ppl_loss = 0
            print self.name, ' celebrating for ', gold_loss, ' gold with ', ppl_loss, ' casualities'
            self.gold -= gold_loss
            self.peoples -= ppl_loss
        else:
            pass

    def settle(self):
        print 'Village %s choose to settle new village ' % self.name,
        if self.gold > 500 and self.peoples > 30 and not self.settler['ready']:
            self.gold -= 300
            self.settler['gold'] = int(self.gold / 2)
            self.settler['peoples'] = int(self.peoples / 2)
            self.settler['name'] = self.name + ' - '
            self.settler['ready'] = True
            self.gold -= self.settler['gold']
            self.peoples -= self.settler['peoples']
            print 'with %s gold and %s peoples' % (self.settler['gold'], self.settler['peoples'])
        else:
            print ' but not have such resources'

    def choise_building(self):
        if self.ppl_capacity - self.peoples < 5:
            return 'house'
        elif self.gold < 50 or self.gold_inc < 5:
            return 'smith'
        elif self.warr_capacity - self.warriors < 3:
            return 'barracks'
        elif random.randint(1, 10) > 3:
            return 'farm'
        else:
            return random.choice(self.buildings.keys())

    def build(self, type):
        print 'Village %s choose to build %s' % (self.name, type),
        if type in self.buildings.keys():
            if self.gold >= self.buildings[type][0]:
                if self.peoples >= self.buildings[type][2]:
                    if self.structures[type]['count'] == self.structures[type]['enabled']:
                        print 'successfully'
                        self.structures[type]['count'] += 1
                        self.structures[type]['enabled'] += 1
                        self.gold -= self.buildings[type][0]
                        self.peoples -= self.buildings[type][2]
                        self.gold_inc += self.buildings[type][3]
                        self.ppl_capacity += self.buildings[type][4]
                        self.warr_capacity += self.buildings[type][5]
                    else:
                        print ' but not all enabled'
                else:
                    print ' but no such peoples'
            else:
                print ' but cannot affroid'