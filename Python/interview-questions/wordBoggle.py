from collections import defaultdict


def wordBoggle(board, words):
    """
    >>> board = [["R","L","D"], ["U","O","E"], ["C","S","O"]]
    >>> words = ["CODE", "SOLO", "RULES", "COOL"]
    >>> wordBoggle(board, words)
    ['CODE', 'RULES']
    """
    a = PrefixAutocompleter(words)
    words = set(words)
    solutions = []
    n = len(board)
    m = len(board[0])
    queue = [((x, y), "", set()) for x in range(n) for y in range(m)]
    while queue:
        (x, y), prefix, positions = queue.pop()
        if prefix in words:
            solutions.append(prefix)
        if a.has_prefix(prefix):
            for position in get_neigbors(x, y, n, m):
                xn, yn = position
                char = board[xn][yn]
                new_prefix = prefix + char
                if position not in positions and a.has_prefix(new_prefix):
                    queue.append(
                        ((xn, yn), new_prefix, set(positions).union({position}))
                    )
    return sorted(set(solutions))


def get_neigbors(x, y, n, m):
    """
    >>> list(get_neigbors(1, 1, 3, 3))
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    """
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            xn = x + i
            yn = y + j
            if 0 <= xn < n and 0 <= yn < m:
                yield (xn, yn)


class PrefixAutocompleter:
    # Use a trie if this becomes huge
    def __init__(self, words):
        self.prefix2word = defaultdict(set)
        for word in words:
            for i in range(0, len(word) + 1):
                self.prefix2word[word[:i]].add(word)

    def has_prefix(self, prefix):
        return prefix in self.prefix2word


if __name__ == "__main__":
    import doctest

    doctest.testmod()
