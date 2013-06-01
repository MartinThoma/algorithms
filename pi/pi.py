#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fractions import Fraction
from decimal import *
digits = 500
getcontext().prec = digits

def Leibnitz(n):
    pi = Fraction(0)
    sign = 1
    for k in range(1,n,2):
        pi = pi + sign*Fraction(4,k)
        sign *= -1
    return pi;

def calcPi(n):
    pi = Fraction(0)
    for k in range(n):
        #print(Fraction(-1,4)**k)
        pi += Fraction(-1,4)**k * (Fraction(1,1+2*k) + Fraction(2,1+4*k) + Fraction(1,3+4*k))
    return pi

def getCorrectDigits(approx):
    pi = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
    for i, el in enumerate(pi):
        if len(approx) <= i:
            return i-1
        if el != approx[i]:
            return i
    return "good, indeed"

if __name__ == "__main__":
    #for n in range(1,180):
    #    approx = calcPi(n)
    #    dec =Decimal(approx.numerator) / Decimal(approx.denominator)
    #    #print(dec)
    #    print("correct digits: %s (n=%i)"  % (getCorrectDigits(str(dec)),n))

    n = digits
    approx = calcPi(n)
    dec =Decimal(approx.numerator) / Decimal(approx.denominator)
    print(dec)
