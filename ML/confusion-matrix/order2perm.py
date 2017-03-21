#!/usr/bin/env python

import json
from visualize import read_symbols
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str


with open("order.json") as f:
    order = json.load(f)

symbols = read_symbols()
perm = [symbols.index(el) for el in order]

with io.open('perm-manual.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(perm,
                      indent=4, sort_keys=True,
                      separators=(',', ':'), ensure_ascii=False)
    outfile.write(to_unicode(str_))
