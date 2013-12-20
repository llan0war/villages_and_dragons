from Queue import Queue

__author__ = 'a.libkind'

config = {'port': 5000, 'authkey': 'dragonone', 'server': 'localhost'}
modules = ['comm', 'villages', 'lairs', 'taskproc', 'world']


def serverInit(config):
    from multiprocessing import managers

    class comm_channel(managers.BaseManager):
        pass

    lst = dict()
    for module in modules:
        lst[module] = Queue()
        comm_channel.register(module, callable=lambda: lst[module])

    m = comm_channel(address=('', config['port']), authkey=config['authkey'])
    s = m.get_server()
    s.serve_forever()


def clientInit(config, module):
    if module in modules:
        from multiprocessing import managers

        class comm_channel(managers.BaseManager):
            pass

        print 'Initiqalizing channel ', module
        comm_channel.register(module)
        m = comm_channel(address=(config['server'], config['port']), authkey=config['authkey'])
        m.connect()
        #TODO change that crap
        if module == 'comm':
            res = m.comm()
        elif module == 'villages':
            res = m.villages()
        elif module == 'lairs':
            res = m.lairs()
        elif module == 'taskproc':
            res = m.taskproc()
        elif module == 'world':
            res = m.world()
        return res
    else:
        raise

if __name__ == '__main__':
    serverInit(config)
    #clientInit(config)