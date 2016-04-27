#!/usr/bin/env python

"""A chat server."""

import Pyro.core


class Chat(Pyro.core.ObjBase):
    """The called class."""

    def __init__(self):
        """Constructor."""
        Pyro.core.ObjBase.__init__(self)
        self.msgs = []
        self.clients = []

    def receive(self, sender, msg, last_msg):
        """Receive a message."""
        self.msgs.append((sender, msg))
        print("[{sender}] {msg}".format(sender=sender, msg=msg))
        return (self.msgs[last_msg:], len(self.msgs))


Pyro.core.initServer()
pydaemon = Pyro.core.Daemon()
uri = pydaemon.connect(Chat(), "chat")

print("The daemon runs on port: {port}".format(port=pydaemon.port))
print("The object's uri is: {uri}".format(uri=uri))

pydaemon.requestLoop()
