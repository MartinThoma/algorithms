#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Solution for problem B to Codejam 2016, Round 1B of Martin Thoma."""


def try_equal(C, J):
    """Try if it is possible to make both equal."""
    equal_possible = True
    for i in range(len(C)):
        if C[i] != J[i]:
            equal_possible = False
    if not equal_possible:
        return C, J
    for i in range(len(C)):
        if C[i] == '?':
            C = list(C)
            C[i] = J[i]
            C = "".join(C)
        elif J[i] == '?':
            J = list(J)
            J[i] = C[i]
            J = "".join(J)
    return C, J


def fill(C, J, number):
    counter = 0
    for i in range(len(C)):
        if C[i] == '?':
            C = list(C)
            C[i] = number[counter]
            C = "".join(C)
            counter += 1
    for i in range(len(J)):
        if J[i] == '?':
            J = list(J)
            J[i] = number[counter]
            J = "".join(J)
            counter += 1
    return C, J


def brute(C, J):
    qmarks = C.count('?') + J.count('?')
    min_c, min_j, diff = None, None, None
    for i in range(10**qmarks):
        c_tmp, j_tmp = fill(C, J, str(i).zfill(qmarks))
        diff_tmp = abs(int(c_tmp) - int(j_tmp))
        if diff is None or (diff_tmp < diff) or (diff_tmp == diff and int(c_tmp) < int(min_c)):
            min_c = c_tmp
            min_j = j_tmp
            diff = diff_tmp
    return min_c, min_j


def save_fill(C, J):
    """Fill question marks at beginning, up to one before the first digit."""
    first_digit = 0
    for c, j in zip(C, J):
        if c != '?' or j != '?':
            break
        first_digit += 1
    for i in range(first_digit-1):
        if C[i] == '?':
            C = list(C)
            C[i] = "0"
            C = "".join(C)
        if J[i] == '?':
            J = list(J)
            J[i] = "0"
            J = "".join(J)
    return C, J


def brute_two(C, J):
    first = 0
    for i in range(len(C)):
        if C[i] != '?' or J[i] != '?':
            first = i
            break
    if first == 0:
        c_tmp, j_tmp = brute(C[0], J[0])
        C = list(C)
        C[0] = c_tmp[0]
        C = "".join(C)
        J = list(J)
        J[0] = j_tmp[0]
        J = "".join(J)
    else:
        c_tmp, j_tmp = brute(C[first-1:first+1], J[first-1:first+1])
        C = list(C)
        C[first-1] = c_tmp[0]
        C[first] = c_tmp[1]
        C = "".join(C)
        J = list(J)
        J[first-1] = j_tmp[0]
        J[first] = j_tmp[1]
        J = "".join(J)
    return C, J


def brute_prefix(C, J):
    while ('?' in C) or ('?' in J):
        qcounter = 0
        index = len(C)-1
        break_next = False
        for i in range(len(C)):
            if (C[i] == '?' or J[i] == '?') and break_next:
                index = i - 1
                break
            if C[i] == '?':
                qcounter += 1
            if J[i] == '?':
                qcounter += 1
            if qcounter >= 3:
                index = i
                break_next = True
                # break
        c_tmp, j_tmp = brute(C[:index+1], J[:index+1])
        for i in range(index+1):
            C = list(C)
            C[i] = c_tmp[i]
            C = "".join(C)
            J = list(J)
            J[i] = j_tmp[i]
            J = "".join(J)
    # if first == 0:
    #     c_tmp, j_tmp = brute(C[0], J[0])
    #     C = list(C)
    #     C[0] = c_tmp[0]
    #     C = "".join(C)
    #     J = list(J)
    #     J[0] = j_tmp[0]
    #     J = "".join(J)
    # elif first == len(C)-1:
    #     c_tmp, j_tmp = brute(C[-1], J[-1])
    #     C = list(C)
    #     C[-1] = c_tmp[0]
    #     C = "".join(C)
    #     J = list(J)
    #     J[-1] = j_tmp[0]
    #     J = "".join(J)
    # else:
    #     c_tmp, j_tmp = brute(C[first-1:first+2], J[first-1:first+2])
    #     C = list(C)
    #     C[first-1] = c_tmp[0]
    #     C[first] = c_tmp[1]
    #     C[first+1] = c_tmp[2]
    #     C = "".join(C)
    #     J = list(J)
    #     J[first-1] = j_tmp[0]
    #     J[first] = j_tmp[1]
    #     J[first+1] = j_tmp[2]
    #     J = "".join(J)
    return C, J


def solve(C, J):
    """Solve."""
    C, J = try_equal(C, J)
    C, J = save_fill(C, J)
    if False and (C.count('?') + J.count('?') <= 4):
        C, J = brute(C, J)
    else:
        C, J = brute_prefix(C, J)
        #C, J = brute(C, J)
    if not "?" in C and not "?" in J:
        return C, J
    return C, J
    c_bigger = None
    stopped_at = None
    for i in range(len(C)):
        if C[i] == J[i]:
            if C[i] == '?':
                C = list(C)
                C[i] = "0"
                C = "".join(C)
                J = list(J)
                J[i] = "0"
                J = "".join(J)
        elif C[i] == '?':
            C = list(C)
            C[i] = J[i]
            C = "".join(C)
        elif J[i] == '?':
            J = list(J)
            J[i] = C[i]
            J = "".join(J)
        else:
            c_bigger = C[i] > J[i]
            stopped_at = i
            break
    if not "?" in C and not "?" in J:
        return C, J
    for i in range(stopped_at+1, len(C)):
        if C[i] == '?':
            if c_bigger:
                C = list(C)
                C[i] = "0"
                C = "".join(C)
            else:
                C = list(C)
                C[i] = "9"
                C = "".join(C)
        if J[i] == '?':
            if c_bigger:
                J = list(J)
                J[i] = "9"
                J = "".join(J)
            else:
                J = list(J)
                J[i] = "0"
                J = "".join(J)
    return C, J


if __name__ == "__main__":
    testcases = input()

    for caseNr in xrange(1, testcases+1):
        cipher = raw_input()
        C, J = cipher.split(" ")
        print("Case #%i: %s" % (caseNr, " ".join(solve(C, J))))
