#!/usr/bin/env python
# -*- coding: utf-8 -*-


def nice_cubic_polynomial(p):
    """
    Get a nice string representation of the cubic polynomial `p`.

    Parameters
    ----------
    p : list
        cubic polynomial

    Returns
    -------
    str
    """
    tmp = ""
    if p["a"] == 1:
        tmp += " x^3"
    elif p["a"] != 0:
        tmp += "%.2fx^3" % p["a"]
    if p["b"] == 1:
        tmp += "\t+ x^2"
    elif p["b"] != 0:
        tmp += "\t+ %.2fx^2" % p["b"]
    else:
        tmp += "\t\t"
    if p["c"] == 1:
        tmp += "\t+ x"
    elif p["c"] != 0:
        tmp += "\t+ %.2fx" % p["c"]
    else:
        tmp += "\t\t"
    if p["d"] != 0:
        tmp += "\t+ %.2f" % p["d"]
    return tmp


def get_spline(points):
    """
    points should be a list of maps, where each map represents a point and has
    "x" and "y"
    """
    import numpy
    import scipy.linalg

    # sort points by x value
    points = sorted(points, key=lambda point: point["x"])

    n = len(points) - 1

    # Set up a system of equations of form Ax=b
    A = numpy.zeros(shape=(4*n, 4*n))
    b = numpy.zeros(shape=(4*n, 1))

    for i in range(0, n):
        # 2n equations from condtions (S2)
        A[i][4*i+0] = points[i]["x"]**3
        A[i][4*i+1] = points[i]["x"]**2
        A[i][4*i+2] = points[i]["x"]
        A[i][4*i+3] = 1
        b[i] = points[i]["y"]

        A[n+i][4*i+0] = points[i+1]["x"]**3
        A[n+i][4*i+1] = points[i+1]["x"]**2
        A[n+i][4*i+2] = points[i+1]["x"]
        A[n+i][4*i+3] = 1
        b[n+i] = points[i+1]["y"]

        # 2n-2 equations for (S3):
        if i == 0:
            continue
        # point i is an inner point
        A[2*n+(i-1)][4*(i-1)+0] = 3*points[i]["x"]**2
        A[2*n+(i-1)][4*(i-1)+1] = 2*points[i]["x"]
        A[2*n+(i-1)][4*(i-1)+2] = 1
        A[2*n+(i-1)][4*(i-1)+0+4] = -3*points[i]["x"]**2
        A[2*n+(i-1)][4*(i-1)+1+4] = -2*points[i]["x"]
        A[2*n+(i-1)][4*(i-1)+2+4] = -1
        b[2*n+(i-1)] = 0

        A[3*n+(i-1)][4*(i-1)+0] = 6*points[i]["x"]
        A[3*n+(i-1)][4*(i-1)+1] = 2
        A[3*n+(i-1)][4*(i-1)+0+4] = -6*points[i]["x"]
        A[3*n+(i-1)][4*(i-1)+1+4] = -2
        b[3*n+(i-1)] = 0
    # Natural spline:
    A[3*n-1+0][0+0] += 6*points[0]["x"]
    A[3*n-1+0][0+1] += 2
    b[3*n-1+0] += 0

    A[3*n+n-1][4*(n-1)+0] += 6*points[n]["x"]
    A[3*n+n-1][4*(n-1)+1] += 2
    b[3*n+n-1] += 0

    x = scipy.linalg.solve(A, b)
    spline = []
    for i in range(0, n):
        spline.append({"u": points[i]["x"], "v": points[i+1]["x"],
                       "a": float(x[4*i+0]),
                       "b": float(x[4*i+1]),
                       "c": float(x[4*i+2]),
                       "d": float(x[4*i+3])})
    return spline

if __name__ == "__main__":
    points = []
    points.append({"x": 0.0, "y": -4})
    points.append({"x": 1.0, "y": 9})
    points.append({"x": 2.0, "y": 35})
    points.append({"x": 3.0, "y": 70})
    spline = get_spline(points)
    for p in spline:
        tmp = "[%.2f, %.2f]:" % (p["u"], p["v"])
        tmp += nice_cubic_polynomial(p)
        print(tmp)
