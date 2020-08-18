# Core Library modules
import logging
import random
import sys
import time

import pympler.asizeof
from mpu.datastructures.char_trie import Trie
# First party modules
from mpu.datastructures.trie import Trie

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)
logging.getLogger("mpu").setLevel(logging.WARNING)

t0 = time.time()
with open("words.txt") as f:
    data = f.read()
t1 = time.time()
logger.info(
    f"Word string (not splitted) has a size of {pympler.asizeof.asizeof(data):,} byte"
)
words = [word.strip() for word in data.split("\n")]

words = sorted([word for word in words], key=lambda n: n.lower())
logger.info(f"Word list has a size of {pympler.asizeof.asizeof(words):,} byte")
word_set = set(words)
logger.info(f"Word set has a size of {pympler.asizeof.asizeof(word_set):,} byte")
with open("words-sorted.txt", "w") as f:
    for word in words:
        f.write(word + "\n")

logger.info(f"Read words in {t1 - t0:0.1f}s")
t0 = time.time()
trie = Trie(words)
t1 = time.time()
logger.info(f"Created Trie in {t1 - t0:0.1f}s")
logger.info(f"Trie has a size of {pympler.asizeof.asizeof(trie):,} byte")
words_trie = sorted([word for word in trie], key=lambda n: n.lower())
with open("words-trie.txt", "w") as f:
    for word in words_trie:
        f.write(word + "\n")

random.shuffle(words)
t0 = time.time()
for word in words:
    assert word in trie.autocomplete(word), f"'{word}' was not found in Trie"
assert "foobarbanana" not in trie
t1 = time.time()
logger.info(f"Checking all words in {t1-t0:0.1f}s")
print("-" * 80)

from mpu.datastructures.autocomplete import Autocompleter

t0 = time.time()
autocompleter = Autocompleter(words)
t1 = time.time()
logger.info(f"Created Autocompleter in {t1 - t0:0.1f}s")
logger.info(
    f"Autocompleter has a size of {pympler.asizeof.asizeof(autocompleter):,} byte"
)

t0 = time.time()
for word in words:
    assert word in autocompleter, f"'{word}' was not found in autocompleter"
t1 = time.time()
logger.info(f"Checking all words in {t1-t0:0.1f}s")
print("-" * 80)

import pygtrie

t0 = time.time()
trie = pygtrie.CharTrie()
for word in words:
    trie[word] = True
t1 = time.time()
logger.info(f"Created pygtrie in {t1 - t0:0.1f}s")
logger.info(f"pygtrie has a size of {pympler.asizeof.asizeof(trie):,} byte")

t0 = time.time()
for word in words:
    assert word in trie.iterkeys(prefix=word), f"'{word}' was not found in pygtrie"
t1 = time.time()
logger.info(f"Checking all words in {t1-t0:0.1f}s")
