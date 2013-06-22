#!/usr/bin/env python
# -*- coding: utf-8 -*-
  
def pprintGaus(A):
    """ Pretty print a n×n matrix with a result vector n×1. """
    n = len(A)
    for i in range(0, n):
        line = ""
        for j in range(0, n+1):
            line += str(A[i][j]) + "\t"
            if j == n-1:
                line +=  "| "
        print(line)
    print("")

def pprintPolynomial(A):
    """ Pretty print a polynomial. """
    line = ""
    for i in range(len(x)-1, -1, -1):
        if x[i] != 0:
            if i == 0:
                line += "+" + str(x[i])
            else:
                if x[i] == 1:
                    line += "+ x^" + str(i) + "\t"
                elif x[i] == -1:
                    line += "- x^" + str(i) + "\t"
                else:
                    line += "+" + str(x[i]) + "·x^" + str(i) + "\t"
    print(line)

def gauss(A):
    """ Solve a linear sysem of equations given by a n×n matrix 
        with a result vector n×1. """
    n = len(A)
  
    for i in range(0,n):
        # Search for maximum in this column
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i+1,n):
            if abs(A[k][i]) > maxEl:
                maxEl = A[k][i]
                maxRow = k
  
        # Swap maximum row with current row (column by column)
        for k in range(i,n+1):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp
  
        # Make all rows below this one 0 in current column
        for k in range(i+1,n):
            c = -A[k][i]/A[i][i]
            for j in range(i,n+1):
                if i==j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]
  
    # Solve equation Ax=b for an upper triangular matrix A
    x=[0 for i in range(n)]
    for i in range(n-1,-1,-1):
        x[i] = A[i][n]/A[i][i]
        for k in range(i-1,-1,-1):
            A[k][n] -= A[k][i] * x[i]
    return x

def setGauss(points):
    """ Create a system of equations for gaussian elimination from 
        a set of points. """
    n = len(points) - 1
    A = [[0 for i in range(n+2)] for j in range(n+1)]
    for i in range(n+1):
        x = points[i]["x"]
        for j in range(n+1):
            A[i][j] = x**j
        A[i][n+1] = points[i]["y"]
    return A
  
if __name__ == "__main__":
    from fractions import Fraction
  
    # Read input data
    points = []
    points.append({"x": Fraction(-1), "y": Fraction(1)})
    points.append({"x": Fraction(1), "y": Fraction(1)})
    points.append({"x": Fraction(2), "y": Fraction(2)})

    A = setGauss(points)
  
    # Print input
    pprintGaus(A)
  
    # Calculate solution
    x = gauss(A)
  
    # Print result
    pprintPolynomial(x)
