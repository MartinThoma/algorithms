from collections import defaultdict


def findSubstrings(words, parts):
    parts_set = set(parts)
    prefixer = Prefixer(parts)
    return [substitute(word, prefixer) for word in words]


def substitute(word, prefixer):
    subsitutes = list(get_substitutes(word, prefixer))

    # Longest ones
    len2sub = defaultdict(list)
    for sub in subsitutes:
        length = get_longest(sub)
        len2sub[length].append(sub)
    subsitutes = len2sub[max(len2sub.keys())]

    # Most subsitues
    c2sub = defaultdict(list)
    for sub in subsitutes:
        length = get_substitution_count(sub)
        c2sub[length].append(sub)
    subsitutes = c2sub[max(c2sub.keys())]

    # TODO: take best one
    subsitute = subsitutes[0]
    return subsitute


def get_substitution_count(sub):
    return sub.count("[")


def get_longest(sub):
    start = None
    end = None
    max_len = 0
    for i, char in enumerate(sub):
        if char == "[":
            start = i
        elif char == "]":
            end = i
            if end - start > max_len:
                max_len = end - start
            start = None
            end = None
    return max_len


def get_substitutes(word, prefixer, multiple=False):
    for start_index in range(len(word)):
        for end_index in range(start_index + 1, len(word) + 1):
            prefix = word[start_index:end_index]
            parts_complete = list(prefixer.autocomplete(prefix))
            parts_exact = [
                part for part in parts_complete if len(part) == end_index - start_index
            ]
            if len(parts_complete) == 0:
                break
            elif len(parts_exact) == 1 and is_prefix(word, start_index, parts_exact[0]):
                part = parts_exact[0]
                remainder = word[start_index + len(part) :]
                if multiple:
                    for remainder_sub in get_substitutes(remainder, prefixer):
                        yield apply_part(word, start_index, part) + remainder_sub
                else:
                    yield apply_part(word, start_index, part) + remainder
    yield word


def is_prefix(word, start_index, prefix) -> bool:
    return word[start_index : start_index + len(prefix)] == prefix


def apply_part(word, start_index, part):
    left = word[:start_index]
    right = word[start_index + len(part) :]
    return f"{left}[{part}]"


class Prefixer:
    def __init__(self, words):
        self.prefix2word = defaultdict(set)
        for word in words:
            self.insert(word)

    def insert(self, word):
        for i in range(len(word) + 1):
            prefix = word[:i]
            self.prefix2word[prefix].add(word)

    def autocomplete(self, prefix):
        return self.prefix2word[prefix]


# print(findSubstrings(words=["Watermelon"], parts=["a", "mel", "lon", "el", "An"]))
# print(findSubstrings(words=["Melon"], parts=["a", "mel", "lon", "el", "An"]))
print(findSubstrings(words=["b"], parts=["b"]))
# print(
#     findSubstrings(
#         words=["myopic"],
#         parts=[
#             "aaaaa",
#             "Aaaa",
#             "E",
#             "z",
#             "Zzzzz",
#             "a",
#             "mel",
#             "lon",
#             "el",
#             "An",
#             "ise",
#             "d",
#             "g",
#             "wnoVV",
#             "i",
#             "IUMc",
#             "P",
#             "KQ",
#             "QfRz",
#             "Xyj",
#             "yiHS",
#         ],
#     )
# )
