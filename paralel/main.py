import csv
import multiprocessing.pool
import random
import time

# 3rd party modules
from mpu import parallel_for


def calc_stuff(bla):
    time.sleep(3 * random.random())
    return bla**2


data = [['load', 'nb_threads', 'time_in_s']]
for nb_threads in [10, 100, 1000, 10000]:
    for load in [10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000,
                 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000,
                 9000, 10000, 20000]:
        parameters = list(range(load))
        t0 = time.time()
        out = parallel_for(calc_stuff, parameters, nb_threads)
        t1 = time.time()
        data.append([load, nb_threads, t1 - t0])
        print(data[-1])

# Write CSV file
with open('data.csv', 'w') as fp:
    writer = csv.writer(fp, delimiter=',')
    # writer.writerow(["your", "header", "foo"])  # write header
    writer.writerows(data)

print(list(out))
