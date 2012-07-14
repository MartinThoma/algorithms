#!/usr/bin/python
# -*- coding: utf-8 -*-

def selectionsort(list):
    """ Idea: Get the minimum and swap it to the front. """
    n = len(list)
    for i in xrange(0, n-1):
        minimum = i
        for j in xrange(i+1, n):
            if list[j] < list[i]:
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

def test(algorithm):
    """ Some testcases to make sure, that the implementations are 
        not completely wrong. """
    assert algorithm([]) == []
    assert algorithm([1]) == [1]
    assert algorithm([1,2,3,4,5,6]) == [1,2,3,4,5,6]
    assert algorithm([6,5,4,3,2,1]) == [1,2,3,4,5,6]
    assert algorithm([1,3,7,4,8,9]) == [1,3,4,7,8,9]

if __name__ == "__main__":
    test(selectionsort)
    test(bubblesort)
    test(insertionsort)
    test(quicksort)

