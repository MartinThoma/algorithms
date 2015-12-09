#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This snippet makes checks on finite algebraic structures. It checks
* associativity
* kommutativity
* neutral element
* inverse elements

It also classifies structures according to the results (in German):
* (kommutatives) Magma
* (kommutatives) Halbgruppe
* (kommutatives) Monoid
* (kommutatives) Gruppe
"""


# http://stackoverflow.com/a/2267446/562769
def base_n(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz", pad=-1):
    """
    Parameters
    ----------
    num : int
    b : int
        Base
    numerals : str
    pad : int
    """
    number = (((num == 0) and numerals[0]) or
              (base_n(num // b, b, numerals, pad).lstrip(numerals[0]) +
               numerals[num % b]))
    if pad == -1:
        return number
    else:
        return number.zfill(pad)


def is_wellformed(conjunction):
    """
    Parameters
    ----------
    conjunction : list

    Returns
    -------
    bool
        True if it is wellformed, otherwise False.
    """
    nr_of_elements = len(conjunction)
    elements = set()
    for line in conjunction:
        if len(line) != nr_of_elements:
            return False
        for element in line:
            elements.add(element)
    if len(elements) > nr_of_elements:
        return False
    return True


def get_elements(conjunction):
    """
    Parameters
    ----------
    conjunction : list

    Returns
    -------
    set
        All elements on which the conjunction is defined.
    """
    elements = set()
    for line in conjunction:
        for element in line:
            elements.add(element)
    return elements


def is_kommutativ(conjunction, verbose=False):
    """
    Check if the conjunction is commutative.

    Parameters
    ----------
    conjunction
    verbose : bool

    Returns
    -------
    bool
        True if the conjunction is commutative, otherwise False.
    """
    is_kommutativ_flag = True
    counterexamples = []
    nr_of_elements = len(conjunction)
    for nr in range(0, nr_of_elements**2 - 1 + 1):
        a, b = base_n(nr, nr_of_elements, pad=2)
        a, b = int(a), int(b)
        ab = conjunction[a][b]
        ba = conjunction[b][a]
        if ab != ba:
            counterexamples.append((a, b))
            if verbose:
                print("Not kommutative:%s*%s = %s != %s = %s*%s" %
                      (a, b, ab, ba, a, b))
            is_kommutativ_flag = False
    return is_kommutativ_flag, counterexamples


def is_associativ(conjunction, verbose=False):
    """
    Check if the conjunction is associative.

    Parameters
    ----------
    conjunction
    verbose : bool

    Returns
    -------
    bool
        True if the conjunction is associative, otherwise False.
    """
    is_associativ_flag = True
    counterexamples = []
    nr_of_elements = len(conjunction)
    for nr in range(0, nr_of_elements**3 - 1 + 1):
        a, b, c = base_n(nr, nr_of_elements, pad=3)
        a, b, c = int(a), int(b), int(c)
        ab = conjunction[a][b]
        abc1 = conjunction[ab][c]
        bc = conjunction[b][c]
        abc2 = conjunction[a][bc]
        if abc1 != abc2:
            counterexamples.append((a, b, c))
            if verbose:
                print("Not associative:(%s*%s)*%s = %s != %s = %s * (%s*%s)" %
                      (a, b, c, abc1, abc2, a, b, c))
            is_associativ_flag = False
    return is_associativ_flag, counterexamples


def is_conjunction_symmetric(conjunction):
    """
    Check if the conjunction is symmetric.

    Parameters
    ----------
    conjunction

    Returns
    -------
    bool
        True if the conjunction is symmetric, otherwise False.
    """
    for zeile in range(len(conjunction)):
        for spalte in range(len(conjunction)):
            if conjunction[zeile][spalte] != conjunction[spalte][zeile]:
                return False
    return True


def generate_empty_conjunction(nr_of_elements):
    """
    Generate a conjunction which maps everything to 0.

    Parameters
    ----------
    nr_of_elements : int

    Returns
    -------
    list
    """
    conjunction = []
    for i in range(nr_of_elements):
        line = []
        for j in range(nr_of_elements):
            line.append(0)
        conjunction.append(line)
    return conjunction


def increase_conjunction(conjunction, nr_of_elements):
    """
    Parameters
    ----------
    conjunction
    nr_of_elements : int

    Returns
    -------
    bool
    """
    i = j = 0
    conjunction[i][j] += 1
    while conjunction[i][j] == nr_of_elements:
        conjunction[i][j] = 0
        j += 1
        if j == nr_of_elements:
            j = 0
            i += 1
        if i == nr_of_elements:
            return False
        conjunction[i][j] += 1
    return True


def print_conjunction(conjunction, nr_of_elements):
    """
    Display the conjunction.

    Parameters
    ----------
    conjunction
    nr_of_elements : int
    """
    title_line = " * ||"
    for i in range(nr_of_elements):
        title_line += " " + str(i) + " |"
    print(title_line)
    print("-"*len(title_line))
    for i, line in enumerate(conjunction):
        line_tmp = " " + str(i) + " ||"
        for el in line:
            line_tmp += " " + str(el) + " |"
        print(line_tmp)


def get_neutral_element(conjunction, nr_of_elements, verbose=False):
    """
    Find the neutral element of a conjunction.
    """
    left_neutrals = []
    right_neutrals = []
    for n in range(nr_of_elements):
        n_is_left_neutral = True
        n_is_right_neutral = True
        for el in range(nr_of_elements):
            if conjunction[n][el] != el:
                n_is_left_neutral = False
            if conjunction[el][n] != el:
                n_is_right_neutral = False
        if n_is_left_neutral:
            left_neutrals.append(n)
        if n_is_right_neutral:
            right_neutrals.append(n)
    neutral = set(left_neutrals).intersection(set(right_neutrals))
    if verbose:
        print(left_neutrals)
        print(right_neutrals)
    return list(neutral)


def check_inverse(conjunction, nr_of_elements, neutral_element):
    """
    Check if every element of the conjunction has an inverse element.

    Parameters
    ----------
    conjunction
    nr_of_elements : int
    neutral_element

    Returns
    -------
    tuple
        (bool, el) - if it is False, give a counter example. Otherwise
        (True, -1)
    """
    for el in range(nr_of_elements):
        has_inverse = False
        for possibleInverse in range(nr_of_elements):
            if conjunction[el][possibleInverse] == neutral_element and \
               conjunction[possibleInverse][el] == neutral_element:
                has_inverse = True
                break
        if not has_inverse:
            return False, el
    return True, -1


def complete_check(conjunction, nr_of_elements):
    """
    Make all checks for the conjunction and display the information.
    """
    wellformed = is_wellformed(conjunction)
    associative, associativeCounterexamples = is_associativ(conjunction)
    kommutativ, kommutativCounterexamples = is_kommutativ(conjunction)
    neutrals = get_neutral_element(conjunction, nr_of_elements)
    if len(neutrals) == 1:
        all_have_inverse, all_have_inverse_counterexamples = \
            check_inverse(conjunction, nr_of_elements, neutrals[0])
    else:
        all_have_inverse = False

    print("M = {"+",".join(map(str, list(range(nr_of_elements))))+"}")
    print_conjunction(conjunction, nr_of_elements)

    if wellformed and not associative:
        print("(M,*) ist ein Magma, aber keine Halbgruppe, da (M,*) "
              "nicht assoziativ ist:")
        a, b, c = associativeCounterexamples[0]
        ab = conjunction[a][b]
        bc = conjunction[b][c]
        print(u"\t(%i*%i)*%i = %i * %i = %i \u2260 %i = %i * %i = %i*(%i*%i)" %
              (a, b, c,
               ab, c, conjunction[ab][c],
               conjunction[a][bc], a, bc, a, b, c))
    if wellformed and associative and not len(neutrals) == 1:
        print("(M,*) ist eine Halbgruppe, aber kein Monoid, da (M,*) kein "
              "neutrales Element besitzt.")
    if wellformed and associative and len(neutrals) == 1 \
       and not all_have_inverse:
        print("(M,*) ist ein Monoid, aber keine Gruppe, da in (M,*) nicht "
              "alle Elemente ein Inverses haben:")
        print("\tNeutrals: %s" % str(neutrals))
        print("\t%i hat kein Inverses" % all_have_inverse_counterexamples)
    if wellformed and associative and len(neutrals) == 1 and all_have_inverse:
        print("(M,*) ist eine Gruppe.")

    if kommutativ:
        print("(M,*) ist kommutativ.")
    else:
        print("(M,*) ist nicht kommutativ:")
        a, b = kommutativCounterexamples[0]
        print(u"\t%i*%i = %i \u2260 %i = %i*%i" %
              (a, b, conjunction[a][b], conjunction[b][a], b, a))
    print("#"*80)

if __name__ == "__main__":
    # It is important that 0,1,2 is the order of lines and rows!
    #               0  1  2
    #               a  b  c
    conjunction = [[0, 1, 2],
                   [1, 2, 0],
                   [2, 0, 1]]
    complete_check(conjunction, 3)

    # print("(M, *) is a Magma:\t%s" % str(is_wellformed(conjunction)))
    # print("(M, *) is associative:\t%s" % str(is_associativ(conjunction)))

    # nr_of_elements = 4
    # conjunction = generate_empty_conjunction(nr_of_elements)
    # checkedConjunctions = 1
    """
    while increase_conjunction(conjunction, nr_of_elements):
        wellformed = is_wellformed(conjunction)
        associative = is_associativ(conjunction, False)
        kommutativ = is_kommutativ(conjunction, False)
        symmetric = is_conjunction_symmetric(conjunction)
        if not kommutativ and symmetric:
            print("M = {"+",".join(map(str,list(range(nr_of_elements))))+"}")
            print_conjunction(conjunction, nr_of_elements)
            print("(M, *) is a Magma:\t%s" % str(wellformed))
            print("(M, *) is associative:\t%s" % str(associative))
            print("(M, *) is kommutativ:\t%s" % str(kommutativ))
            is_associativ(conjunction, True)
            print("(M, *) is symmetric:\t%s" % str(symmetric))
            break
        checkedConjunctions += 1
        if checkedConjunctions % 100000 == 0:
            print("Checked %i conjunctions." % checkedConjunctions)
    print("Finished. Checked %i conjunctions." % checkedConjunctions)
    """
