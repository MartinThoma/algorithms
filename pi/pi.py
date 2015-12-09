#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fractions import Fraction
from decimal import getcontext, Decimal
digits = 500
getcontext().prec = digits


def leibnitz(n):
    """
    Parameters
    ----------
    n : int

    Returns
    -------
    Fraction
        Approximation of pi.
    """
    pi = Fraction(0)
    sign = 1
    for k in range(1, n, 2):
        pi = pi + sign*Fraction(4, k)
        sign *= -1
    return pi


def calc_pi(n):
    """
    Calculate PI.

    Parameters
    ----------
    n : int
        Number of fractions.

    Returns
    -------
    Fraction
        Approximation of pi.
    """
    pi = Fraction(0)
    for k in range(n):
        # print(Fraction(-1,4)**k)
        pi += (Fraction(-1, 4)**k * (Fraction(1, 1+2*k)
               + Fraction(2, 1+4*k)
               + Fraction(1, 3+4*k)))
    return pi


def get_correct_digits(approx):
    """
    Get how many digits were correct.

    Parameters
    ----------
    approx : str
        String representation of an approximation of pi.

    Returns
    -------
    int
        The number of correct digits. If the number has too many correct
        digits, -1 is returned.
    """
    pi = ("3.14159265358979323846264338327950288419716939937510582097494459230"
          "78164062862089986280348253421170679")
    for i, el in enumerate(pi):
        if len(approx) <= i:
            return i-1
        if el != approx[i]:
            return i
    return -1  # Very good!

if __name__ == "__main__":
    # for n in range(1,180):
    #     approx = calc_pi(n)
    #     dec =Decimal(approx.numerator) / Decimal(approx.denominator)
    #     #print(dec)
    #     print("correct digits: %s (n=%i)" % (get_correct_digits(str(dec)),n))

    n = digits
    approx = calc_pi(n)
    dec = Decimal(approx.numerator) / Decimal(approx.denominator)
    print(dec)
