__author__ = 'a.libkind'


class WorldTile:
    def __init__(self, val=None, obj=None):
        self.resource = val or 0
        self.objects = obj or dict()

    def __repr__(self):
        return '%s' % (str(self.resource))

    def __str__(self):
        return '%s' % (str(self.resource))

    def __cmp__(self, other):
        return cmp(self.resource, other)

    def __iadd__(self, other):
        self.resource += other
        return self

    def __isub__(self, other):
        self.resource -= other
        return self

    def __add__(self, other):
        return WorldTile(self.resource + other)

    def __sub__(self, other):
        self.resource -= other
        return self.resource

