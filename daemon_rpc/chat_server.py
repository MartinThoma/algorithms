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
        print(f"[{sender}] {msg}")
        return (self.msgs[last_msg:], len(self.msgs))


Pyro.core.initServer()
pydaemon = Pyro.core.Daemon()
uri = pydaemon.connect(Chat(), "chat")

print(f"The daemon runs on port: {pydaemon.port}")
print(f"The object's uri is: {uri}")

pydaemon.requestLoop()
