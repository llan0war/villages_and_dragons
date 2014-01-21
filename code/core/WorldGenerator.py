import random
import itertools
import math
from code.core import WorldTile

__author__ = 'a.libkind'


class WorldGenerator(object):
    def __init__(self, size=None):
        self.size = size or 2048
        self.world = []
        self.size = self.correct_size(self.size)

    def correct_size(self, num):
        if num < 4 or num > 4096:
            res = 256
        else:
            if int(math.log(num, 2)) == math.log(num, 2):
                res = int(num)
            else:
             res = int(math.pow(2, int(math.log(num, 2))))
        return int(res)

    def get_world(self):
        return self.world

    def generate_world(self):
        self.make_empty_world()
        self.DiamondSquareWorld()
        #self.randomize_all()
        #self.make_points()
        #self.clasterize()
        self.print_world()

    def make_empty_world(self):
        self.world = [[WorldTile.WorldTile() for _ in xrange(self.size + 1)] for _ in xrange(self.size + 1)]

    def rand_coord(self):
        return random.randint(0, self.size-1)

    def make_points(self):
        for _ in itertools.repeat(None, random.randint(int(self.size / 20), int(self.size / 5))):
            self.world[self.rand_coord()][self.rand_coord()].resource = 0

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
            self.world[self.rand_coord()][self.rand_coord()].resource = random.randint(1, 9)

    def print_world(self):
        for line in self.world:
            res = ''
            for elem in line:
                res = res + str(elem)
            print res

    def clasterize(self):
        for _ in itertools.repeat(None, 100):
            if random.randint(1, 10) == 9:
                self.make_points()
            for xcor in range(self.size-1):
                for ycor in range(self.size-1):
                    maked = False
                    if self.world[xcor][ycor] > 0:
                        for k in range(-1, 2):
                            for l in range(-1, 2):
                                if self.world[xcor][ycor] > self.world[xcor + k][ycor + l] + 1:
                                    self.world[xcor + k][ycor + l] += 1
                                    maked = True
                        if maked:
                            self.world[xcor][ycor] -= 1

    #diamond-square realization
    def DiamondSquareWorld(self):
        distro = self.size / 2 #setting default distortion
        cornerheight = 4

        def makecorners(wrld):
            wrld[0][0].resource = cornerheight
            wrld[0][self.size].resource = cornerheight
            wrld[self.size][0].resource = cornerheight
            wrld[self.size][self.size].resource = cornerheight
            return wrld

        def squared(wrld, cx, cy, r0, dist):
            if r0 >= 1:
                rn = random.randint(dist/2, dist)
                #diamond step
                wrld[cx][cy].resource = (wrld[cx - r0][cy - r0].resource + wrld[cx - r0][cy + r0].resource + wrld[cx + r0][cy - r0].resource + wrld[cx + r0][cy + r0].resource) / 4 + rn
                #square step
                wrld[cx - r0][cy].resource = (wrld[cx - r0][cy - r0].resource + wrld[cx - r0][cy + r0].resource) / 2
                wrld[cx + r0][cy].resource = (wrld[cx + r0][cy + r0].resource + wrld[cx + r0][cy + r0].resource) / 2
                wrld[cx][cy + r0].resource = (wrld[cx - r0][cy + r0].resource + wrld[cx + r0][cy + r0].resource) / 2
                wrld[cx][cy - r0].resource = (wrld[cx - r0][cy - r0].resource + wrld[cx + r0][cy - r0].resource) / 2

                #iterate it
                wrld = squared(wrld, cx + r0/2, cy + r0/2, r0/2, rn)
                wrld = squared(wrld, cx - r0/2, cy + r0/2, r0/2, rn)
                wrld = squared(wrld, cx + r0/2, cy - r0/2, r0/2, rn)
                wrld = squared(wrld, cx - r0/2, cy - r0/2, r0/2, rn)
            return wrld

        self.world = makecorners(self.world)
        self.world = squared(self.world, self.size/2, self.size/2, self.size/2, distro)

if __name__ == '__main__':
    wrld = WorldGenerator()
    wrld.generate_world()
    print type(wrld.world[1][1])
