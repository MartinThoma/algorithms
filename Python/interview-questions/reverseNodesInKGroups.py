def reverseNodesInKGroups(l, k):
    n = get_list_length(l)
    current = l
    first = jump_k(current, k - 1)
    l = first  # outlier!
    next_block_start = jump_k(current, k)
    reverse_k(current, k)
    current.next = next_block_start
    last = current
    n -= k
    while n >= k:
        current = next_block_start
        first = jump_k(current, k - 1)
        next_block_start = jump_k(current, k)
        last.next = first
        reverse_k(current, k)
        current.next = next_block_start
        last = current
        n -= k
    return l


def get_list_length(current):
    n = 0
    while current:
        n += 1
        current = current.next
    return n


def reverse_k(current, k=None):
    previous = None
    while k or k is None:
        previous, current.next, current = current, previous, current.next
        k -= 1
    return previous


def jump_k(current, k):
    for _ in range(k):
        current = current.next
    return current


def print_list(current):
    values = []
    i = 0
    BREAKER = 30
    while current and i < BREAKER:
        values.append(current.value)
        current = current.next
        i += 1
    print(values)
    if i == BREAKER:
        print(f"!!!Breaker={BREAKER} was applied")


class Node:
    def __init__(self, x, next_=None):
        self.value = x
        self.next = next_

    def __repr__(self):
        if self.next is None:
            return f"Node({self.value})"
        else:
            return f"Node({self.value}->{self.next.value})"


def test_1():
    l = Node(1, Node(2, Node(3, Node(4, Node(5, Node(6, Node(7)))))))
    print_list(l)
    print("-" * 3)
    print_list(reverseNodesInKGroups(l, k=2))


def test_2():
    l = Node(1, Node(2, Node(3, Node(4))))
    print_list(l)
    print("-" * 3)
    print_list(reverseNodesInKGroups(l, k=2))


if __name__ == "__main__":
    test_2()
