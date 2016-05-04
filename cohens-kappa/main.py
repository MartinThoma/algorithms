#!/usr/bin/env python

"""Check the value of Cohens Kappa."""


def margin1(contingency_table, i):
    """Calculate the margin distribution of classifier 1."""
    return sum([contingency_table[j][i]
                for j in range(len(contingency_table))])


def margin2(contingency_table, i):
    """Calculate the margin distribution of classifier 2."""
    return sum([contingency_table[i][j]
                for j in range(len(contingency_table))])


def kappa(contingency_table):
    """Get the value of Cohens Kappa."""
    n = sum([el for row in contingency_table for el in row])
    print("n=%i" % n)
    p_0 = (1.0 / n) * sum([contingency_table[i][i]
                           for i in range(len(contingency_table))])
    p_c = (1.0 / (n**2)) * (margin1(contingency_table, i) *
                            margin2(contingency_table, i))
    return (p_0 - p_c) / (1 - p_c)


a = 0
b = 1001
c = 1000
d = 0
contingency_table = [[a, b], [c, d]]
print(kappa(contingency_table))
print("#"*10)

a = 0
b = 10
c = 10
d = 10
e = 0
f = 10
g = 10
h = 10
j = 0
contingency_table = [[a, b, c], [d, e, f], [g, h, j]]
print(kappa(contingency_table))
