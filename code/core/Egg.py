import random

__author__ = 'Llanowar'


class Egg(object):
    def __init__(self, id=None, parent_genes=[[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]):
        self._age = 0
        self.id = id or random.randint(1000000, 10000000-1)
        self._parent_genes = []
        self._parent_genes = parent_genes
        self._genes = [0,0,0,0,0,0]
        self._hatch_time = int(self._genes[5])*2
        self.hatcheble = False
        self.new_one()

    def age(self):
        return int(self._age)

    def new_one(self):
        for gene_num in range(len(self._genes)):
            tmp = random.randint(1, 5)
            if tmp == 3:
                #middle of parents
                res_gene = int((int(self._parent_genes[0][gene_num]) + int(self._parent_genes[1][gene_num]))/2)
                self._genes[gene_num] = res_gene
            elif tmp < 3:
                self._genes[gene_num] = self._parent_genes[0][gene_num]
            else:
                self._genes[gene_num] = self._parent_genes[1][gene_num]
            self.mutate(gene_num)

    def mutate(self, gen_num):
        if random.randint(1, 100) == 100:
            if gen_num == 4:
                #modify color
                self._genes[gen_num] = random.randint(1, 10)
                #print "--> color changed", self._genes

            else:
                if self._genes[gen_num] < 5:
                    self._genes[gen_num] += 1
                elif random.randint(1, 100) == 50:
                    self._genes[gen_num] += 1

    def turn(self):
        self._age += 1
        if self._age > self._hatch_time:
            if random.randint(1,100) > 95:
                self._hatch_time = 2000
            else:
                self.hatcheble = True

    def hatch(self):
        return self._genes
