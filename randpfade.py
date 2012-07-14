#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser

def isNaht(liste):
    pre = liste[0]
    for el in liste:
        if abs(pre - el) > 1:
            return False
        pre = el
    return True

def increaseByOne(liste, n):
    """ @return: True, if it can continue. False, if not. """
    i = 1
    liste[-i] += 1
    while i <= len(liste) and liste[-i] == n:
        liste[-i] = 0
        i += 1
        if (i == len(liste) and liste[0] == n-1) or i > len(liste):
            return False
        liste[-i] += 1
    return i <= len(liste)

def increase(liste, n):
    """ @return: True, if it can continue. False, if not. """
    p = increaseByOne(liste, n)
    
    while (not isNaht(liste)) and p:
        p = increaseByOne(liste, n)


    return p

def pfade(m, n):
    # jedes der m elemente (1 pro zeile) repräsentiert die spalte
    # adjazente elemente dürfen sich nur um 1 unterscheiden
    arr = [0 for el in xrange(m)]
    pfade = 1
    randpfade = 1
    while increase(arr, n):
        pfade += 1
        if arr[-m] == 0 or arr[-m] == (n-1):
            randpfade += 1
    return (pfade, randpfade)

def f(m, n):
    if m == 0:
        return 2
    else:
        sum = 3*f(m-1,n)
        i = 2
        while m-i >= 0:
            sum += (-1)**(i+1) * f(m-i, n)
            i += 1
        sum += ((-1)**(n%2))*(m % 2)
        return sum

if '__main__' == __name__:
    parser = OptionParser()
    parser.add_option("-n", type="int", dest="n")
    (options, args) = parser.parse_args()

    n = options.n
    qSum = 0
    for m in xrange(1,10+1):
        p, q = pfade(m, n)
        print "%i x %i hat\t%i Pfade,\t%i davon sind Randpfade. (%i, %i)" % (m, n, p, q, qSum, f(m, n))
        qSum += q
