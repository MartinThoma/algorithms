#!/usr/bin/env python

"""The server."""

import logging
import sys

import Pyro.core

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


class Bartimaeus(Pyro.core.ObjBase):
    """The called class."""

    def __init__(self):
        """Constructor."""
        Pyro.core.ObjBase.__init__(self)
        self.counter = 0

    def count(self, up):
        """Count up."""
        logging.info("new up: %i", up)
        self.counter += up
        return f"I was called {self.counter} times."

Pyro.core.initServer()
daemon = Pyro.core.Daemon()
uri = daemon.connect(Bartimaeus(), "bartid")

print(f"The daemon runs on port: {daemon.port}")
print(f"The object's uri is: {uri}")

daemon.requestLoop()
