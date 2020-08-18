from typing import List


def graphDistances(g: List[List[int]], s: int) -> List[int]:
    """
    >>> g = [[-1,3,2], [2,-1,0], [-1,0,-1]]
    >>> graphDistances(g, 0)
    [0, 2, 2]
    """
    min_dist = {i: float("inf") for i in range(len(g))}
    min_dist[s] = 0
    q = {s}
    while q:
        node = q.pop()
        node_dist = min_dist[node]
        if node_dist == float("inf"):
            continue
        for target_node, distance in enumerate(g[s]):
            if g[node][target_node] == -1:
                continue
            if min_dist[target_node] > node_dist + g[node][target_node]:
                min_dist[target_node] = node_dist + g[node][target_node]
                q.add(target_node)
    return [value for key, value in sorted(min_dist.items())]


if __name__ == "__main__":
    graphDistances([[-1, 3, 2], [2, -1, 0], [-1, 0, -1]], 0)
    import doctest

    doctest.testmod()
