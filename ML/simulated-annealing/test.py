"""Optimize a combinatoric problem with simulated annealing."""

import time
import random
import logging

import numpy as np

random.seed(0)
np.random.seed(0)


class AnnealingProblem(object):
    """ABstract definition of simulated annealing."""

    def mutate(self):
        pass

    def score(self):
        pass


class PermutationProblem(object):
    def __init__(self, edges):
        self.edges = edges
        self.nb_nodes = len(edges)

    def mutate(self):
        permutation = np.random.permutation(list(range(self.nb_nodes)))
        return permutation

    def score(self):
        assert len(solution) == len(set(solution)) == len(edges)
        value = 0.0
        for source_node, target_node in enumerate(solution):
            value += edges[source_node][target_node]
        return value


def simulated_annealing(current_solution,
                        score,
                        steps=2 * 10**5,
                        temp=100.0,
                        cooling_factor=0.99,
                        deterministic=False):
    """
    Optimize current_cm by randomly swapping elements.

    Parameters
    ----------
    current_cm : numpy array
    current_perm : None or iterable, optional (default: None)
    current_solution : AnnealingProblem
    score : function on AnnealingProblem that returns a float
        The lower, the better
    steps : int, optional (default: 2 * 10**4)
    temp : float > 0.0, optional (default: 100.0)
        Temperature
    cooling_factor: float in (0, 1), optional (default: 0.99)
    """
    assert temp > 0
    assert cooling_factor > 0
    assert cooling_factor < 1

    current_score = score(current_solution)
    best_solution = current_solution
    best_score = current_score
    print("## Starting Score: {:0.2f}%".format(current_score * 100))
    for step in range(steps):
        tmp_solution = best_solution.mutate()
        tmp_score = score(tmp_solution)
        if deterministic:
            chance = 1.0
        else:
            chance = random.random()
            temp *= 0.99
        hot_prob = min(1, np.exp(-(tmp_score - current_score) / temp))
        if chance <= hot_prob:
            if best_score > tmp_score:  # Minimize the score
                best_solution = tmp_solution
                best_score = tmp_score
            current_score = tmp_score
            logging.info(("Current: %0.2f%% (best: %0.2f%%, hot_prob=%0.2f%%, "
                          "step=%i)"),
                         (current_score * 100),
                         (best_score * 100),
                         (hot_prob * 100),
                         step)
    return best_solution


def optimize_simple(edges, nb_tries=100):
    """
    Super stupid optimization: Try random solutions and take better ones.

    nb_tries=10000, solution score=7566, Execution time=7.0s
    nb_tries=100000, solution score=7566, Execution time=74.7s

    Parameters
    ----------
    edges : ndarray
        matrix of edge weights
    nb_tries : positive int
        Execution time scales linearly with this value
    """
    assert nb_tries >= 1
    nb_nodes = len(edges)
    best_solution = np.random.permutation(list(range(nb_nodes)))
    best_score = evaluate_solution(edges, best_solution)
    for i in range(nb_tries):
        solution = np.random.permutation(list(range(nb_nodes)))
        score = evaluate_solution(edges, solution)
        if score > best_score:
            best_score = score
            best_solution = solution
    return best_solution


def optimize_swap(edges, nb_tries=100):
    """
    Simulated-annealing based optimization.

    Try random solutions, swap and use if it improved.

    nb_tries=    100, solution score= 7354, Execution time=  0.06s
    nb_tries=   1000, solution score= 9252, Execution time=  0.46s
    nb_tries=  10000, solution score=12607, Execution time=  4.50s
    nb_tries= 100000, solution score=13779, Execution time= 51.77s
    nb_tries=1000000, solution score=13996, Execution time=540.69s

Found solution: 13996
Execution time: 540.69s


    Parameters
    ----------
    edges : ndarray
        matrix of edge weights
    nb_tries : positive int
        Execution time scales linearly with this value
    """
    assert nb_tries >= 1
    n = len(edges)
    best_solution = np.random.permutation(list(range(n)))
    best_score = evaluate_solution(edges, best_solution)
    for try_i in range(nb_tries):
        i = random.randint(0, n - 1)
        j = i
        while j == i:
            j = random.randint(0, n - 1)
        solution = swap_1d(np.copy(best_solution), i, j)
        score = evaluate_solution(edges, solution)
        if score > best_score:
            best_score = score
            best_solution = solution
            print('{}: {}'.format(try_i, best_score))
    return best_solution


def evaluate_solution(edges, solution):
    assert len(solution) == len(set(solution)) == len(edges)
    value = 0.0
    for source_node, target_node in enumerate(solution):
        value += edges[source_node][target_node]
    return value


def swap_1d(perm, i, j):
    """
    Swap two elements of a 1-D numpy array in-place.

    Examples
    --------
    >>> perm = np.array([2, 1, 2, 3, 4, 5, 6])
    >>> swap_1d(perm, 2, 6)
    array([2, 1, 6, 3, 4, 5, 2])
    """
    perm[i], perm[j] = perm[j], perm[i]
    return perm


def main(nb_nodes):
    edges = np.random.randint(low=0, high=15, size=(nb_nodes, nb_nodes),
                              dtype='l')
    t0 = time.time()
    solution = optimize_swap(edges, nb_tries=1000000)
    t1 = time.time()
    value = evaluate_solution(edges, solution)
    print('Found solution: {:0.0f}'.format(value))
    print('Execution time: {:0.2f}s'.format(t1 - t0))


if __name__ == '__main__':
    main(nb_nodes=1000)
