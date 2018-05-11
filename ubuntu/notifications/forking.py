import os
import time

pid = os.fork()
if pid:
    # parent
    while True:
        print("I'm the parent: pid={}".format(pid))
        time.sleep(0.5)
else:
    # child
    while True:
        print("I'm just a child: pid={}".format(pid))
        time.sleep(0.5)
