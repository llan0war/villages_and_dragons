import itertools

__author__ = 'a.libkind'

from code.core import WorldGenerator, Lair, Kingdom

class World(object):
    def __init__(self):
        self.world = []
        self.get_new_world()
        self._lairs = set()
        self._kingdoms = set()

    def add_lair(self):
        new_lair = Lair.Lair()
        for _ in itertools.repeat(None, 20): new_lair.add_dragon()
        self._lairs.add(new_lair)

    def add_kingdom(self):
        new_kingdom = Kingdom.Kingdom()
        for _ in itertools.repeat(None, 5): new_kingdom.add_village()
        self._kingdoms.add(new_kingdom)

    def get_new_world(self):
        gen = WorldGenerator.WorldGenerator(size=100)
        gen.generate_world()
        self.world = gen.get_world()
        del gen

    def turn(self):
        for lair in self._lairs:
            lair.turn(20)
        for kingdom in self._kingdoms:
            kingdom.turn()

if __name__ == '__main__':
    wrld = World()
    wrld.add_kingdom()
    wrld.add_lair()

    for _ in itertools.repeat(None, 5000): wrld.turn()