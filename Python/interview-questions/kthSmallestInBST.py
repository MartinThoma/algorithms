#
# Binary trees are already defined with this interface:


class Tree:
    def __init__(self, x, left=None, right=None):
        self.value = x
        self.left = left
        self.right = right


def kthSmallestInBST(t, k, level=0, values=None):
    if values is None:
        values = []
    if t.left is not None:
        kthSmallestInBST(t.left, k, level + 1, values)
    values += [t.value]
    if len(values) >= k:
        print(f"done: {values}")
        if level > 0:
            return values
        else:
            return values[k - 1]
    if t.right is not None:
        kthSmallestInBST(t.right, k, level + 1, values)
    if len(values) >= k:
        if level > 0:
            return values
        else:
            return values[k - 1]
    return values


t = Tree(1, None, Tree(2, None, Tree(3, None, Tree(4, None, Tree(5)))))
print(kthSmallestInBST(t, 4))

t = Tree(1, Tree(0), Tree(2))
print(kthSmallestInBST(t, 3))
