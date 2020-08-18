#!/usr/bin/env python

import signal
import time
from multiprocessing import Process

import Pyro4


@Pyro4.expose
class Thing:
    def method(self, arg):
        return arg * 2


def start_server():
    daemon = Pyro4.Daemon()
    uri = daemon.register(Thing)
    print(f"uri={uri}")
    daemon.requestLoop()
    # ------ alternatively, using serveSimple -----
    Pyro4.Daemon.serveSimple(
        {
            Thing: "mythingy"
        },
        ns=True, verbose=True, host="yourhostname")


def main():
    p = Process(target=start_server)
    p.daemon = True  # Need to inform Process that this should run as a daemon
    p.start()

    # Important when running this program stand alone: Must wait long enough
    # for start_server to get into the daemon context before the main program
    # exits or Process will take down the subprocess before it detaches
    time.sleep(3.0)


if __name__ == '__main__':
    start_server()
