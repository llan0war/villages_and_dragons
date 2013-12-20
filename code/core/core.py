import logging
import threading
from multiprocessing import Process
from code.network import connector

__author__ = 'a.libkind'


class Core(threading.Thread):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event

    def run(self):
        self.server_start()
        #while not self.stopped.wait(1):
        #    pass

    def server_start(self):
        server = Process(target=connector.serverInit, args=(connector.config,))
        server.start()
        print 'I\'l see server', server.is_alive()
        print 'Looks like a server started'