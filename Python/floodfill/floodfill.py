from typing import Optional, Tuple


class Node:
    position: Tuple[int, int]
    color: int
    count: int

    def __init__(
        self, position: Tuple, color: int, neighbors=None, parent=None, count: int = 0
    ):
        if neighbors is None:
            neighbors = []
        self.neighbors = neighbors
        self.position = position
        self.color = color
        self.parent = parent
        self.count = count

    def __str__(self):
        return f"Node(position={self.position})"

    __repr__ = __str__


def init_graph(arr):
    graph = {}
    for x, a in enumerate(arr):
        for y, color in enumerate(a):
            position = (x, y)
            graph[position] = Node(position=position, color=color)
    for x, y in graph.keys():
        ns = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for neighbor in ns:
            if neighbor in graph:
                graph[(x, y)].neighbors.append(graph[neighbor])
    return graph


def get_components(graph):
    visited = set()
    new_candidates = set([(0, 0)])
    components = []
    while new_candidates:
        current_component = []
        current_component_queue = []
        seed = new_candidates.pop()
        if seed in visited:
            continue
        current_component_queue.append(seed)
        while current_component_queue:
            pos = current_component_queue.pop()
            current_component.append(pos)
            for neighbor in graph[pos].neighbors:
                if neighbor.position in visited:
                    continue
                if neighbor.color == graph[pos].color:
                    current_component_queue.append(neighbor.position)
                else:
                    new_candidates.add(neighbor.position)
            visited.add(pos)
        components.append(current_component)
    return components


def solve(arr):
    # init
    progress = []
    for x, a in enumerate(arr):
        line = []
        for y, color in enumerate(a):
            position = (x, y)
            line.append(Node(position=position, color=color))
        progress.append(line)

    progress[0][0].count = 1

    max_node = process(arr, progress, [progress[0][0]])
    print(max_node)
    print(progress)


def process(arr, progress, queue):
    biggest = None
    while len(queue) > 0:
        current = queue.pop()
        if biggest is None or biggest.count < current.count:
            biggest = current

        if len(progress[0]) > current.position[1] + 1:
            child1 = progress[current.position[0]][current.position[1] + 1]
        else:
            child1 = None

        if len(progress) > current.position[0] + 1:
            child2 = progress[current.position[0] + 1][current.position[1]]
        else:
            child2 = None

        if child1 is not None:
            if child1.color == current.color:
                if current.parent is not None:
                    child1.parent = current.parent
                    current.parent.count += 1
                    if current.parent.count > biggest.count:
                        biggest = current.parent
                else:
                    child1.parent = current
                    current.count += 1
                    if current.count > biggest.count:
                        biggest = current
            else:
                child1.count = 1
            queue.append(child1)
        if child2 is not None:
            if child2.color == current.color:
                if current.parent is not None:
                    child2.parent = current.parent
                    current.parent.count += 1
                    if current.parent.count > biggest.count:
                        biggest = current.parent
                else:
                    child2.parent = current
                    current.count += 1
                    if current.count > biggest.count:
                        biggest = current
            else:
                child2.count = 1
            queue.append(child2)
    return biggest


if __name__ == "__main__":
    arr = [[0, 0, 1, 2, 1], [0, 2, 1, 1, 1], [1, 1, 1, 0, 0]]
    for el in arr:
        print(el)
    # solve(arr)
    graph = init_graph(arr)
    print(graph)
    print(graph[(0, 0)].neighbors)
    print("## Components")
    for component in get_components(graph):
        print(f"{graph[component[0]].color}: {component}")
