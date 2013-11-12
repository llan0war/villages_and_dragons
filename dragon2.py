__author__ = 'a.libkind'

class Lair(object):
    coords = [0, 0]
    gold = 0

    def __init__(self, name):
        self.name = name

    def create(self):
        coords = [0, 0]
        self.gold = self.wealth
        self.wealth = 0

    def turn(self):
        pass

    def logic(self):
        pass


class Dragon(object):
    def __init__(self):
        pass