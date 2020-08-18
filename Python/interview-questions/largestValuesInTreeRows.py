class Tree:
    def __init__(self, x):
        self.value = x
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Tree({self.value}, left={self.left}, right={self.right})"


def largestValuesInTreeRows(t):
    depth2value = {}
    depth = 0
    l = [(t, depth)]
    while l:
        print(l)
        print(depth2value)
        current, current_depth = l.pop(0)
        if current is None:
            continue
        if current_depth not in depth2value:
            depth2value[current_depth] = current.value
        if depth2value[current_depth] < current.value:
            depth2value[current_depth] = current.value
        l.append((current.left, current_depth + 1))
        l.append((current.right, current_depth + 1))
    return [value for _, value in sorted(depth2value.items())]


t = Tree(-1)
t.left = Tree(5)
t.right = Tree(7)
t.right.right = Tree(1)

print(largestValuesInTreeRows(t))
