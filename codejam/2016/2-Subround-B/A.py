#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Solution for problem B to Codejam 2016, Round 1B of Martin Thoma."""


def solve(cipher):
    """Solve."""
    letters = {}
    digits = []
    for letter in cipher:
        if letter in letters:
            letters[letter] += 1
        else:
            letters[letter] = 1
    if 'X' in letters and letters['X'] > 0:
        for i in range(letters['X']):
            digits.append(6)
        letters['S'] -= letters['X']
        letters['I'] -= letters['X']
        letters['X'] -= letters['X']
    if 'Z' in letters and letters['Z'] > 0:
        for i in range(letters['Z']):
            digits.append(0)
        letters['E'] -= letters['Z']
        letters['R'] -= letters['Z']
        letters['O'] -= letters['Z']
        letters['Z'] -= letters['Z']
    if 'W' in letters and letters['W'] > 0:
        for i in range(letters['W']):
            digits.append(2)
        letters['T'] -= letters['W']
        letters['O'] -= letters['W']
        letters['W'] -= letters['W']
    if 'S' in letters and letters['S'] > 0:
        for i in range(letters['S']):
            digits.append(7)
        letters['E'] -= letters['S']
        letters['V'] -= letters['S']
        letters['N'] -= letters['S']
        letters['S'] -= letters['S']
    if 'V' in letters and letters['V'] > 0:
        for i in range(letters['V']):
            digits.append(5)
        letters['F'] -= letters['V']
        letters['I'] -= letters['V']
        letters['E'] -= letters['V']
        letters['V'] -= letters['V']
    if 'U' in letters and letters['U'] > 0:
        for i in range(letters['U']):
            digits.append(4)
        letters['F'] -= letters['U']
        letters['O'] -= letters['U']
        letters['R'] -= letters['U']
        letters['U'] -= letters['U']
    if 'R' in letters and letters['R'] > 0:
        for i in range(letters['R']):
            digits.append(3)
        # "THREE",
        letters['T'] -= letters['R']
        letters['H'] -= letters['R']
        letters['E'] -= letters['R']
        letters['R'] -= 2*letters['R']
    if 'O' in letters and letters['O'] > 0:
        for i in range(letters['O']):
            digits.append(1)
        # "ONE",
        letters['N'] -= letters['O']
        letters['E'] -= letters['O']
        letters['O'] -= letters['O']
    if 'G' in letters and letters['G'] > 0:
        for i in range(letters['G']):
            digits.append(8)
        # "EIGHT",
        letters['E'] -= letters['G']
        letters['I'] -= letters['G']
        letters['H'] -= letters['G']
        letters['T'] -= letters['G']
        letters['G'] -= letters['G']
    if 'I' in letters and letters['I'] > 0:
        for i in range(letters['I']):
            digits.append(9)
    return "".join([str(el) for el in sorted(digits)])


if __name__ == "__main__":
    testcases = input()

    for caseNr in xrange(1, testcases+1):
        cipher = raw_input()
        print("Case #%i: %s" % (caseNr, solve(cipher)))
