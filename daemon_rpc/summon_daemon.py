#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        return "I was called {count} times.".format(count=self.counter)

Pyro.core.initServer()
daemon = Pyro.core.Daemon()
uri = daemon.connect(Bartimaeus(), "bartid")

print("The daemon runs on port: {port}".format(port=daemon.port))
print("The object's uri is: {uri}".format(uri=uri))

daemon.requestLoop()
