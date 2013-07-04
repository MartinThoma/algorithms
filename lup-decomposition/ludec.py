#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Derived from http://rosettacode.org/wiki/LU_decomposition#Python

from fractions import Fraction

def standardMatrixProduct(A, B):
    """Returns A*B for two square matrices A, B in R^(nxn)."""
    n = len(A)
    C = [[Fraction(0) for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C
 
def pivotize(A):
    """Creates the pivoting matrix P for A."""
    n = len(A)
    # Create identity
    P = [[Fraction(i == j) for i in range(n)] for j in range(n)]
    for j in range(n):
        row = max(range(j, n), key=lambda i: A[i][j])
        if j != row:
            P[j], P[row] = P[row], P[j]
    return P

def luDecomposition(A):
    """Decomposes a nxn matrix A by PA=LU and returns L, U and P."""
    n = len(A)
    L = [[Fraction(0)] * n for i in range(n)]
    U = [[Fraction(0)] * n for i in range(n)]
    P = pivotize(A)
    A2 = standardMatrixProduct(P, A)
    for j in range(n):
        L[j][j] = Fraction(1)

        for i in range(j+1):
            s1 = sum(U[k][j] * L[i][k] for k in range(i))
            U[i][j] = A2[i][j] - s1

        for i in range(j, n):
            s2 = sum(U[k][j] * L[i][k] for k in range(j))
            L[i][j] = (A2[i][j] - s2) / U[j][j]
    return (L, U, P)

def pprint(A, name=""):  
    n = len(A)
    for x, line in enumerate(A):
        pLine = ""
        for i, el in enumerate(line):
            if i == 0:
                if x == n/2:
                    pLine += name + " = "
                pLine += "\t" + str(el)
            else:
                pLine += "\t" + str(el)
        print pLine
    print ""

if __name__ == "__main__":
    A = [[10, 9, 8, 7, 6],
         [2, 5, 4, 3, 2],
         [7, 1, 1, 0, 1],
         [8, 2, 8, 2, 3],
         [1, 8, 2, 8, 4]]
    A =[map(Fraction, line) for line in A]
    L, U, P = luDecomposition(A)
    pprint(L, "L")
    pprint(U, "U")
    pprint(P, "P")
    pprint(standardMatrixProduct(L, U),"L*U")
