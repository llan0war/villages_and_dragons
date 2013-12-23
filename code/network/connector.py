from Queue import Queue

__author__ = 'a.libkind'

config = {'port': 5005, 'authkey': 'dragonone', 'server': 'localhost'}
modules = ['comm', 'villages', 'lairs', 'taskproc', 'world']


def serverInit(config, module):
    from multiprocessing import managers

    class comm_channel(managers.BaseManager):
        pass

    port = config['port'] + modules.index(module)

    loc_lst = Queue()
    comm_channel.register(module, callable=lambda: loc_lst)

    m = comm_channel(address=('', port), authkey=config['authkey'])
    print 'Starting %s channel at %s port' % (module, port)
    s = m.get_server()
    s.serve_forever()


def clientInit(config, module):
    if module in modules:
        from multiprocessing import managers

        class comm_channel(managers.BaseManager):
            pass

        print 'Initializing channel %s at port %s' % (module, config['port'] + modules.index(module))
        comm_channel.register(module)
        m = comm_channel(address=(config['server'], config['port'] + modules.index(module)), authkey=config['authkey'])
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