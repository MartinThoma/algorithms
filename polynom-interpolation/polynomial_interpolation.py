#!/usr/bin/env python
# -*- coding: utf-8 -*-


def pprint_gaus(matrix):
    """
    Pretty print a n×n matrix with a result vector n×1.
    """
    n = len(matrix)
    for i in range(0, n):
        line = ""
        for j in range(0, n+1):
            line += str(matrix[i][j]) + "\t"
            if j == n-1:
                line += "| "
        print(line)
    print("")


def pprint_polynomial(x):
    """
    Pretty print a polynomial.

    Parameters
    ----------
    x : list
        A polynomial represented by a list of numbers. The first element is
        the coefficient of x^0, the second is the coefficient of x^1, ...
    """
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
    """
    Solve a system of linear equations given by a n×n matrix with a result
    vector n×1.
    """
    n = len(A)

    for i in range(0, n):
        # Search for maximum in this column
        max_el = abs(A[i][i])
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > max_el:
                max_el = abs(A[k][i])
                max_row = k

        # Swap maximum row with current row (column by column)
        for k in range(i, n+1):
            tmp = A[max_row][k]
            A[max_row][k] = A[i][k]
            A[i][k] = tmp

        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            c = -A[k][i]/A[i][i]
            for j in range(i, n+1):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]

    # Solve equation Ax=b for an upper triangular matrix A
    x = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = A[i][n]/A[i][i]
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return x


def set_gauss(points):
    """
    Create a system of equations for gaussian elimination from a set of points.
    """
    n = len(points) - 1
    A = [[0 for i in range(n+2)] for j in range(n+1)]
    for i in range(n+1):
        x = points[i]["x"]
        for j in range(n+1):
            A[i][j] = x**j
        A[i][n+1] = points[i]["y"]
    return A


def evaluate_polynomial(p, x):
    """
    Evaluate the polynomial p at position x.

    Parameters
    ----------
    p : list
        Polynomial as a list of coefficients.
    x : number
        Where the polynomial gets evaluated.

    Returns
    -------
    number
    """
    y = 0
    xi = 1
    for i, a in enumerate(p):
        y += a * xi
        xi *= x
    return y


def lagrange_interpolation(points):
    """
    Make a langrange interpolation of points.

    Parameters
    ----------
    points : list

    Returns
    -------
    list
    """
    p = []
    for i in range(len(points)):
        lagrange_i = {"y": points[i]["y"], "polynomial": []}
        for j in range(len(points)):
            if j == i:
                continue
            lagrange_i["polynomial"].append({
                "sub": points[j]["x"],
                "divisor": points[i]["x"] - points[j]["x"]
            })
        p.append(lagrange_i)
    return p


def evaluate_lagrange_polynomial(p, x):
    """
    Evaluate a lagrange polynomial `p` at `x`.

    Parameters
    ----------
    p : list
    x : float
    """
    y = 0
    for lagrange_i in p:
        prod = 1
        for term in lagrange_i["polynomial"]:
            prod *= (x - term["sub"])/term["divisor"]
        y += lagrange_i["y"]*prod
    return y


def get_gauss_system_for_newton(points):
    """
    Get a gaussian equation system: TODO - explain better

    Parameters
    ----------
    points : list

    Returns
    -------
    matrix
    """
    n = len(points) - 1
    A = [[0 for i in range(n+2)] for j in range(n+1)]
    for j in range(0, n+2):
        for i in range(j, n+1):
            if j == 0:
                A[i][j] = 1
            else:
                A[i][j] = A[i][j-1]*(points[i]["x"]-points[j-1]["x"])
        if j == n+1:
            for i in range(0, n):
                A[i][j] = points[i]["y"]
    return A

if __name__ == "__main__":
    from fractions import Fraction

    # Read input data
    points = []
    points.append({"x": Fraction(-80), "y": Fraction(10)})
    points.append({"x": Fraction(-70), "y": Fraction(20)})
    points.append({"x": Fraction(-30), "y": Fraction(10)})
    points.append({"x": Fraction(-10), "y": Fraction(-20)})
    points.append({"x": Fraction(+10), "y": Fraction(20)})
    points.append({"x": Fraction(+20), "y": Fraction(20)})

    A = get_gauss_system_for_newton(points)
    pprint_gaus(A)
    x = gauss(A)
    print(x)

    A = set_gauss(points)
    p = lagrange_interpolation(points)
    print("Lagrange at x=0: %.2f" % evaluate_lagrange_polynomial(p, 0))
    print("Lagrange at x=1: %.2f" % evaluate_lagrange_polynomial(p, 1))
    print("Lagrange at x=2: %.2f" % evaluate_lagrange_polynomial(p, 2))

    # Print input
    pprint_gaus(A)

    # Calculate solution
    x = gauss(A)

    # Print result
    pprint_polynomial(x)
    print("Gauss at x=0: %.2f" % evaluate_polynomial(x, 0))
    print("Gauss at x=1: %.2f" % evaluate_polynomial(x, 1))
    print("Gauss at x=2: %.2f" % evaluate_polynomial(x, 2))
