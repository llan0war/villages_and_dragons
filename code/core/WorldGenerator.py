import random
import itertools

__author__ = 'a.libkind'


class WorldGenerator(object):
    def __init__(self, size=None):
        self.size = size or 100
        self.world = []

    def get_world(self):
        return self.world

    def generate_world(self):
        self.make_empty_world()
        self.randomize_all()
        self.make_points()
        self.clasterize()
        self.print_world()

    def make_empty_world(self):
        self.world = [[0 for x in xrange(self.size)] for x in xrange(self.size)]

    def rand_coord(self):
        return random.randint(0, self.size-1)

    def make_points(self):
        for _ in itertools.repeat(None, random.randint(int(self.size / 20), int(self.size / 5))):
            self.world[self.rand_coord()][self.rand_coord()] = 0

    def normalize(self):
        for _ in itertools.repeat(None, 1000):
            xcor = self.rand_coord()
            ycor = self.rand_coord()
            if xcor + 1 > self.size: xcor -= 1
            if xcor - 1 < 0: xcor += 1
            if ycor + 1 > self.size: ycor -= 1
            if ycor - 1 < 0: ycor += 1

            for k in range(-1, 1):
                for l in range(-1, 1):
                    if self.world[xcor][ycor] <> self.world[xcor + k][ycor + l]:
                        dif = self.world[xcor][ycor] - self.world[xcor + k][ycor + l]
                        self.world[xcor][ycor] -= int(dif/2)
                        self.world[xcor + k][ycor + l] += int(dif/2)

    def randomize_all(self):
        for _ in itertools.repeat(None, 10000):
            self.world[self.rand_coord()][self.rand_coord()] = random.randint(1, 9)

    def print_world(self):
        for line in self.world:
            res = ''
            for elem in line:
                res = res + str(elem)
            print res

    def clasterize(self):
        for _ in itertools.repeat(None, 1000):
            if random.randint(1, 10) == 9:
                self.make_points()
            for xcor in range(self.size-1):
                for ycor in range(self.size-1):
                    maked = False
                    if self.world[xcor][ycor] > 0:
                        for k in range(-1, 2):
                            for l in range(-1, 2):
                                if self.world[xcor][ycor] > self.world[xcor + k][ycor + l] + 1:
                                    self.world[xcor + k][ycor + l] +=  1
                                    maked = True
                        if maked:
                            self.world[xcor][ycor] -= 1
