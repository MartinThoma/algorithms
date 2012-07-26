#!/usr/bin/python
# -*- coding: utf-8 -*-

def selectionsort(list):
    """ Idea: Get the minimum and swap it to the front. """
    n = len(list)
    for i in xrange(0, n-1):
        minimum = i # This is the index of the minimum!
        for j in xrange(i, n):
            if list[j] < list[minimum]:
                minimum = j
        # Swap
        list[minimum], list[i] = list[i], list[minimum]
    return list

def bubblesort(list):
    """ Idea: The maximum value floats at the end of the list in
              every outer iteration. """
    n = len(list)
    somethingChanged = True
    for i in xrange(0, n):
        somethingChanged = False
        for j in xrange(0, n-i-1):
            if list[j] > list[j+1]:
                # Swap
                list[j], list[j+1] = list[j+1], list[j]
                somethingChanged = True
        if not somethingChanged:
            break
    return list

def insertionsort(list):
    """ Idea: If you have a list with one element, it is sorted.
        If you add an element in a sorted list, you have to search
        the place where you want to insert it. """
    n = len(list)
    for i in xrange(1, n):
        value = list[i]
        j = i
        while j > 0 and list[j-1] > value:
            list[j] = list[j-1]
            j -= 1
        list[j] = value
    return list

def quicksort(list):
    """ Idea: look at the german wikipedia. """
    def teile(links, rechts):
        i = links
        # Starte mit j links vom Pivotelement
        j = rechts - 1
        pivot = list[rechts]

        while True:
            # Suche von links ein Element, 
            # welches größer als das Pivotelement ist
            while list[i] <= pivot and i < rechts:
                i += 1

            # Suche von rechts ein Element, 
            # welches kleiner als das Pivotelement ist
            while list[j] >= pivot and j > links:
                j -= 1

            if i < j:
                list[i], list[j] = list[j], list[i]

            if not (i < j):
                break

        # Tausche Pivotelement (list[rechts]) mit 
        # neuer endgültiger Position (list[i])
        if list[i] > pivot:
            list[i], list[rechts] = list[rechts], list[i]
        # gib die Position des Pivotelements zurück
        return i

    def sort(links, rechts):
        if links < rechts:
            teiler = teile(links, rechts)
            sort(links, teiler-1)
            sort(teiler+1, rechts)
    sort(0, len(list)-1)
    return list

def heapsort(list):
    import heapq

    h = []
    for value in list:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))]

def mergesort(list):
    def merge(linkeListe, rechteListe):
        neueListe = []
        while len(linkeListe) != 0 and len(rechteListe) != 0:
            if linkeListe[0] <= rechteListe[0]:
                neueListe.append(linkeListe[0])
                linkeListe = linkeListe[1:]
            else:
                neueListe.append(rechteListe[0])
                rechteListe = rechteListe[1:]

        while len(linkeListe) != 0:
            neueListe.append(linkeListe[0])
            linkeListe = linkeListe[1:]

        while len(rechteListe) != 0:
            neueListe.append(rechteListe[0])
            rechteListe = rechteListe[1:]
        return neueListe

    def sort(list):
        if len(list) <= 1:
            return list
        else:
            halb = len(list)/2
            linkeListe  = list[0:halb]
            rechteListe = list[halb:]
            linkeListe  = sort(linkeListe)
            rechteListe = sort(rechteListe)
            return merge(linkeListe, rechteListe)

    return sort(list)

def gnomesort(list):
    position = 0
    while position < len(list) - 1:
        i = position
        if list[i] <= list[i + 1]: # correct order
            position += 1
        else:
            list[i], list[i + 1] = list[i + 1], list[i] # swap
            if position != 0:
                position -= 1
            else:
                position += 1
    return list

def countingsort(A):
    """ 
        Sort the list A. A has to be a list of integers.

        Every element of the list A has to be non-negative.

        @param A: the list that should get sorted
        @return the sorted list
    """
    if len(A) == 0:
        return []

    C = [0] * (max(A)+1)
    B = [""] * len(A)

    # Count the number of elements
    for el in A:
        C[el] += 1
    # Now C[i] contains how often i is in A

    for index in xrange(1, len(C)):
        C[index] += C[index-1]

    for el in A[::-1]:
        B[C[el]-1] = el
        C[el] -= 1

    return B

# see also: http://www.koders.com/python/fidF772268CB8176B16FFA7B81B012D0253E894DBEB.aspx?s=sort#L1
def radixsort(list, n=10, maxLen=0):
    """ Sort the list.

        @param n: number of bins
        @param maxLen: maximum number of digits of list elements
    """

    if len(list) == 0:
        return []
    elif maxLen == 0:
        maxLen = max(map(lambda x : len(str(abs(x))), list))

    for x in range(maxLen):
        bins = [[] for i in xrange(n)]

        for el in list:
            bins[(el / 10**x ) % n].append(el)

        list = []

        for section in bins:
            list.extend(section)

    return list

def test(algorithm, negatives=True):
    """ Some testcases to make sure, that the implementations are 
        not completely wrong. """
    assert algorithm([]) == []
    assert algorithm([1]) == [1]
    assert algorithm([6,1,1]) == [1,1,6]
    assert algorithm([1,2,3,4,5,6]) == [1,2,3,4,5,6]
    assert algorithm([6,5,4,3,2,1]) == [1,2,3,4,5,6]
    assert algorithm([1,3,7,4,8,9]) == [1,3,4,7,8,9]
    assert algorithm([1,3,8,4,7,9]) == [1,3,4,7,8,9]
    if negatives:
        assert algorithm([1,-3,8,4,7,9]) == [-3,1,4,7,8,9]

if __name__ == "__main__":
    test(selectionsort)
    test(bubblesort)
    test(insertionsort)
    test(quicksort)
    test(heapsort)
    test(mergesort)
    test(countingsort, False)
    test(radixsort, False)
    test(gnomesort)
