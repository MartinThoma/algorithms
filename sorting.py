#!/usr/bin/env python
# -*- coding: utf-8 -*-


def selectionsort(list_):
    """
    Idea: Get the minimum and swap it to the front.
    """
    n = len(list_)
    for i in range(0, n-1):
        minimum = i  # This is the index of the minimum!
        for j in range(i, n):
            if list_[j] < list_[minimum]:
                minimum = j
        # Swap
        list_[minimum], list_[i] = list_[i], list_[minimum]
    return list_


def bubblesort(list_):
    """
    Idea: The maximum value floats at the end of the list in every outer
          iteration.
    """
    n = len(list_)
    something_changed = True
    for i in range(0, n):
        something_changed = False
        for j in range(0, n-i-1):
            if list_[j] > list_[j+1]:
                # Swap
                list_[j], list_[j+1] = list_[j+1], list_[j]
                something_changed = True
        if not something_changed:
            break
    return list_


def insertionsort(list_):
    """
    Idea: If you have a list with one element, it is sorted. If you add an
          element in a sorted list, you have to search the place where you want
          to insert it.
    """
    n = len(list_)
    for i in range(1, n):
        value = list_[i]
        j = i
        while j > 0 and list_[j-1] > value:
            list_[j] = list_[j-1]
            j -= 1
        list_[j] = value
    return list_


def quicksort(list_):
    """
    Idea: look at the German wikipedia.
    """
    def teile(links, rechts):
        i = links
        # Starte mit j links vom Pivotelement
        j = rechts - 1
        pivot = list_[rechts]

        while True:
            # Suche von links ein Element,
            # welches größer als das Pivotelement ist
            while list_[i] <= pivot and i < rechts:
                i += 1

            # Suche von rechts ein Element,
            # welches kleiner als das Pivotelement ist
            while list_[j] >= pivot and j > links:
                j -= 1

            if i < j:
                list_[i], list_[j] = list_[j], list_[i]

            if not (i < j):
                break

        # Tausche Pivotelement (list_[rechts]) mit
        # neuer endgültiger Position (list_[i])
        if list_[i] > pivot:
            list_[i], list_[rechts] = list_[rechts], list_[i]
        # gib die Position des Pivotelements zurück
        return i

    def sort(links, rechts):
        if links < rechts:
            teiler = teile(links, rechts)
            sort(links, teiler-1)
            sort(teiler+1, rechts)
    sort(0, len(list_)-1)
    return list_


def heapsort(list_):
    """
    Heap sort
    TODO: Explain idea

    Parameters
    ----------
    list_ : list
        Sort this one

    Returns
    -------
    list
        Sorted list
    """
    import heapq

    h = []
    for value in list_:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))]


def mergesort(list_):
    """
    Merge sort
    TODO: Explain idea

    Parameters
    ----------
    list_ : list
        Sort this one

    Returns
    -------
    list
        Sorted list
    """
    def merge(linke_liste, rechte_liste):
        neue_liste = []
        while len(linke_liste) != 0 and len(rechte_liste) != 0:
            if linke_liste[0] <= rechte_liste[0]:
                neue_liste.append(linke_liste[0])
                linke_liste = linke_liste[1:]
            else:
                neue_liste.append(rechte_liste[0])
                rechte_liste = rechte_liste[1:]

        while len(linke_liste) != 0:
            neue_liste.append(linke_liste[0])
            linke_liste = linke_liste[1:]

        while len(rechte_liste) != 0:
            neue_liste.append(rechte_liste[0])
            rechte_liste = rechte_liste[1:]
        return neue_liste

    def sort(list_):
        if len(list_) <= 1:
            return list_
        else:
            halb = len(list_)/2
            linke_liste = list_[0:halb]
            rechte_liste = list_[halb:]
            linke_liste = sort(linke_liste)
            rechte_liste = sort(rechte_liste)
            return merge(linke_liste, rechte_liste)

    return sort(list_)


def gnomesort(list_):
    """
    Gnomesort - TODO: Explain idea

    Parameters
    ----------
    list_ : list
        Sort this one

    Returns
    -------
    list
        Sorted list
    """
    position = 0
    while position < len(list_) - 1:
        i = position
        if list_[i] <= list_[i + 1]:  # correct order
            position += 1
        else:
            list_[i], list_[i + 1] = list_[i + 1], list_[i]  # swap
            if position != 0:
                position -= 1
            else:
                position += 1
    return list_


def countingsort(list_a):
    """
    Sort the list list_a. list_a has to be a list of integers.

    Every element of the list list_a has to be non-negative.

    Parameters
    ----------
    list_a :
        Should get sorted

    Returns
    -------
    list
        Sorted list with same elements as list_a.
    """
    if len(list_a) == 0:
        return []

    list_c = [0] * (max(list_a)+1)
    list_b = [""] * len(list_a)

    # Count the number of elements
    for el in list_a:
        list_c[el] += 1
    # Now list_c[i] contains how often i is in list_a

    for index in range(1, len(list_c)):
        list_c[index] += list_c[index-1]

    for el in list_a[::-1]:
        list_b[list_c[el]-1] = el
        list_c[el] -= 1

    return list_b


def radixsort(list_, k=10, d=0):
    """
    Sort the list.
    This method has been used to sort punched cards.

    Parameters
    ----------
    k : int
        Number different characters in a number (base).
    d : int
        Maximum number of digits of list elements.
    """

    if len(list_) == 0:
        return []
    elif d == 0:
        d = max(map(lambda x: len(str(abs(x))), list_))

    for x in range(d):
        # create an empty bin for each possible digit
        bins = [[] for i in range(k)]

        # sort the number according to the digits in the bins
        for el in list_:
            bins[(el / 10**x) % k].append(el)

        # merge all bins to one list_
        list_ = []
        for section in bins:
            list_.extend(section)

    return list_


def test(algorithm, negatives=True):
    """
    Some testcases to make sure, that the implementations are not completely
    wrong.
    """
    assert algorithm([]) == []
    assert algorithm([1]) == [1]
    assert algorithm([6, 1, 1]) == [1, 1, 6]
    assert algorithm([1, 2, 3, 4, 5, 6]) == [1, 2, 3, 4, 5, 6]
    assert algorithm([6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6]
    assert algorithm([1, 3, 7, 4, 8, 9]) == [1, 3, 4, 7, 8, 9]
    assert algorithm([1, 3, 8, 4, 7, 9]) == [1, 3, 4, 7, 8, 9]
    if negatives:
        assert algorithm([1, -3, 8, 4, 7, 9]) == [-3, 1, 4, 7, 8, 9]

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
