import logging
import threading
from code.network import connector

__author__ = 'a.libkind'


class Core(threading.Thread):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self, event, module=None):
        threading.Thread.__init__(self)
        self.stopped = event
        self.module = module

    def run(self):
        for module in connector.modules:
            print 'Loading ', module
            self.server_start(module)
        #while not self.stopped.wait(1):
        #    pass

    def server_start(self, module):
        #server = Process(target=connector.serverInit, args=(connector.config, module,))
        threading.Thread(target=connector.serverInit, args=(connector.config, module,)).start()
        #server.start()
        #print 'I\'l see server', server.is_alive()
        #print 'Looks like a server started'