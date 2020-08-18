import os
import time

pid = os.fork()
if pid:
    # parent
    while True:
        print(f"I'm the parent: pid={pid}")
        time.sleep(0.5)
else:
    # child
    while True:
        print(f"I'm just a child: pid={pid}")
        time.sleep(0.5)
