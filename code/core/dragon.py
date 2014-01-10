import random
from code.core import CoreData

__author__ = 'a.libkind'


class Dragon(object):
    def __init__(self, orders, id_pref=None, id=None, name=None, gene=None, age=0, sex=None):
        self.name = name or CoreData.get_dragon_name()
        self.id = id or self.get_id(id_pref or random.randint(10000, 99999))
        self._pair_cooldown = 0
        self._energy = 10
        self._orders = orders
        self.sex = sex or CoreData.dragon_sex[random.randint(0, 1)]
        self._gene = gene or [1, 1, 1, 1, 1, 1]
        self.color = ''
        self.color = CoreData.dragon_colors[self.get_gene(4)]
        self.age = 0
        self.age = age
        self.max_age = 300 + int(self.get_gene(5))*50
        self.dead = False
        self.pairing = False
        self._age_cat = 0

    def get_id(self, pref):
        return str(pref) + '#' + self.name

    def smart(self):
        return int(1 + self.get_gene(0)*self.age_cat())

    def age_cat(self):
        return self._age_cat

    def calc_age_cat(self):
        self._age_cat = int(self.age/100)

    def power(self):
        return int(1 + self.get_gene(1)*self.age_cat())

    def turn(self):
        self.age += 1
        self.reduce_energy(self.fatigue())
        if self._pair_cooldown > 0:
            self._pair_cooldown -= 1
        if not self.check_death():
            self.logic()
        if random.randint(1, 10) == 10:
            self.calc_age_cat()

    def check_death(self):
        if self.age > self.max_age:
            if random.randint(1, 100) > self.smart():
                self.dead = True
                self._orders.put([self.id, 'dead'], False)
        if self._energy < 0:
            self.dead = True
            self._orders.put([self.id, 'dead'], False)
        return self.dead

    def logic(self):
        if self._energy < 25:
            self._orders.put([self.id, 'hunt', self.smart()], False)
        if not self.pairing and self._pair_cooldown == 0 and self.age_cat() > 0 and self._energy > 20:
            self.enable_pairing()

    def fatigue(self):
        return (1 + float(1 + self.age_cat())/float(3*self.get_gene(3)))/5

    def reduce_energy(self, count):
        self._energy -= count

    def inc_energy(self, count):
        self._energy += count

    def pair(self):
        self.disable_pairing()
        if self._energy > 21:
            self.reduce_energy(20)
        else:
            self.reduce_energy(self._energy - 2)
        return self._gene

    def enable_pairing(self):
        self._orders.put([self.id, 'pair'], False)
        self.pairing = True

    def disable_pairing(self):
        self.pairing = False
        self.set_pair_cooldown()

    def set_pair_cooldown(self, cooldown=None):
        self._pair_cooldown = cooldown or max(int(100 - self.get_gene(5)*5), 15)

    def get_gene(self, num):
        return int(self._gene[num])

    def pair_stat(self):
        return {'sex': self.sex, 'smart': self.smart(), 'strength': self.power(), 'color': self.get_gene(4)}

    def hunt_complete(self, spoil):
        self.inc_energy(spoil)