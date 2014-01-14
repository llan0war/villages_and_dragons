import logging

__author__ = 'a.libkind'

class LogMe:
    def getlog(self, id):
        logger = logging.getLogger(id)
        logger.setLevel(logging.DEBUG)
        return logger