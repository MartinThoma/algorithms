#!/usr/bin/env python

"""Create benchmark for k nearest neighbor on unit sphere in R^k."""
# Scroll down to line 90 to "Adjust this" to add your experiment

import random
import numpy as np
import os.path
import logging
import sys
import Queue as queue
import h5py
import time

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def create_point(n):
    """Create a random point on the unit sphere in R^n."""
    p = np.array([random.uniform(-1, 1) for _ in range(n)])
    return p / np.linalg.norm(p)


def create_points(n, number):
    """Create number random points on the unit sphere in R^n."""
    return [create_point(n) for _ in range(number)]


def get_dist(a, b):
    """Get the Euclidean distance of two points a and b."""
    return np.linalg.norm(a - b)


def run_q_at_a_time(candidates, queries, k, n, algorithm):
    """
    Run every single query in queries.

    Parameters
    ----------
    candidates : object
        Datastructure which contains the nearest neighbor candidates.
    queries : list
        List of points
    k : int
        How many points should be found
    n : int
        Dimension of each point / query
    """
    assert k >= 1
    assert n >= 1
    solution = np.zeros((len(queries), k, n))
    for i, query in enumerate(queries):
        solution[i] = algorithm(D, query, k, n)
    return solution


def brute_force_search(candidates, query, k, n):
    """Find the k nearest neighbors by brute force search."""
    solution = np.zeros((k, n))
    knn = queue.PriorityQueue()
    for candidate in candidates:
        dist = get_dist(candidate, query)
        # insert time to prevent errors as 'candidate' is not sortable.
        knn.put((dist, time.time(), candidate))
    for j in range(k):
        dist, _, item = knn.get()
        solution[j] = item
    return solution


def build_datastructure(candidates):
    """Make something sophisticated to speed up k-nn queries."""
    return candidates


# parameters
k = 5  # get k closest points
n = 128  # dimensionality of each point / query
m = 10**5  # candidates for closest points
T = 10**2  # number of queries
query_batch_size = 10**1  # should divide T
assert T % query_batch_size == 0

# paths
query_file = "queries.hdf5"
candidates_file = "candidates.hdf5"

###############################################################################
# Adjust this
# gets the candidates as argument and should return a datastructure D
create_datastructure_algorithm = build_datastructure

# Gets D, query, k, n as arguments
search_algorithm = brute_force_search

###############################################################################

# Create query and candidate files if not exist or load them otherwise
if not os.path.isfile(candidates_file):
    logging.info("Start creating %i candidates." % m)
    candidates = create_points(n, m)
    with h5py.File(candidates_file, 'w') as f:
        dset = f.create_dataset('candidates',
                                data=np.array(candidates),
                                # maxshape=(None, n),
                                dtype='float32')
else:
    with h5py.File(candidates_file, 'r') as f:
        candidates = np.array(f.get('candidates'))

if not os.path.isfile(query_file):
    logging.info("Start creating %i queries." % T)
    with h5py.File(query_file, 'w') as f:
        dset = f.create_dataset('queries',
                                shape=(query_batch_size, n),
                                maxshape=(None, n),
                                dtype='float32',
                                chunks=(query_batch_size, n))
        for i in range(T / query_batch_size):
            logging.info("\tQuery batch%i of %i." %
                         (i + 1, T / query_batch_size))
            queries = np.array(create_points(n, query_batch_size))
            if i > 0:
                dset.resize((dset.shape[0] + query_batch_size, n))
            dset[-query_batch_size:dset.shape[0], :] = queries


# Evaluate
logging.info("Start evaluation.")
total_time = 0
D = create_datastructure_algorithm(candidates)

with h5py.File(query_file, 'r') as f:
    queries = f.get('queries')
    for i in range(T / query_batch_size):
        logging.info("\tQuery batch %i of %i." % (i + 1, T / query_batch_size))
        q = queries[i * query_batch_size:(i + 1) * query_batch_size]
        t0 = time.time()
        solution = run_q_at_a_time(D, q, k, n, search_algorithm)  # TODO
        # Store the solution and compare against brute force to check if
        # it is correct
        t1 = time.time()
        total_time += t1 - t0
logging.info("Needed %i seconds in total." % (total_time))
logging.info("k={k}, n={n}, m={m}, T={T}: {time:.2f}s per query."
             .format(k=k,
                     n=n,
                     m=m,
                     T=T,
                     time=float(total_time) / T))
