import os
import pickle
import random
import time

__author__ = 'a.libkind'

import socket

requestlib = {'info': 'got info', 'data': 'got data', 'command': 'got command', 'village': 0}
config = {"server": "localhost", "port": 6543}


def handleme(req):
    if req in requestlib.keys():
        if req == 'village':
            with open('../db/10565.Warren.dump', 'r') as f:
                data = f.read()
            return data
        else:
            return requestlib[req]


def server(cfg):
    s = socket.socket()
    s.bind((cfg['server'], cfg['port']))
    s.listen(1)
    while True:
        c, addr = s.accept()
        data = c.recv(1024)
        if data:
            print 'Got connection from', addr, ' with request', data
            c.send(handleme(data))
            c.close()


def client(cfg):
    while True:
        s = socket.socket()
        s.connect((cfg['server'], cfg['port']))
        req = random.choice(requestlib.keys())
        s.send(req)
        data = s.recv(1024)
        print data
        s.close
        time.sleep(1)



if __name__ == '__main__':
    print 'yay'

    #print os.listdir('..\\db')

    #server(config)
    client(config)
