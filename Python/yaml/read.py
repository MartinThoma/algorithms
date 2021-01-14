import pprint

import yaml

with open("example.yaml") as fp:
    data = fp.read()

pp = pprint.PrettyPrinter(indent=2)

parsed = yaml.safe_load_all(data)
pp.pprint(list(parsed))

#import json
#print(json.dumps(parsed))
