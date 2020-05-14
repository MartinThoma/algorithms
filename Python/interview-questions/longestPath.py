class Node:
    def __init__(self, value, children=None):
        if children is None:
            children = []
        self.value: str = value
        self.children = children  # type: List[Node]

    def __str__(self):
        return f"{self.value}, {self.children}"

    __repr__ = __str__


def longestPath(fileSystem):
    filenames = fileSystem.split("\f")

    # Build Tree
    root = Node(value="")
    stack = [root]
    for filename in filenames:
        depth = filename.count("\t") + 1
        filename = filename.replace("\t", "")
        node = Node(filename)
        if len(stack) < depth:
            stack[-1].children.append(node)
            stack.append(node)
        elif len(stack) >= depth:
            while len(stack) > depth:
                stack.pop()
            stack[-1].children.append(node)
            stack.append(node)
        else:
            print("WTF")

    print(root)

    # DFS
    return max(dfs(root))


def dfs(node, prefix_length=-1):
    if node:
        if node.value != "":
            prefix_length += len(node.value) + 1
        for child in node.children:
            yield from dfs(child, prefix_length)
        yield prefix_length
    else:
        yield prefix_length


print(longestPath("a"))
