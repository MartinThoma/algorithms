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
def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz",pad=-1):
    number = ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals, pad).lstrip(numerals[0]) + numerals[num % b])
    if pad == -1:
        return number
    else:
        return number.zfill(pad)
 
def isWellformed(conjunction):
    nrOfElements = len(conjunction)
    elements = set()
    for line in conjunction:
        if len(line) != nrOfElements:
            return False
        for element in line:
            elements.add(element)
    if len(elements) > nrOfElements:
        return False
    return True
 
def getElements(conjunction):
    elements = set()
    for line in conjunction:
        for element in line:
            elements.add(element)
    return elements
 
def getResult(a, b, conjunction):
    return conjunction[a][b]
 
def isKommutativ(conjunction, verbose=False):
    isKommutativFlag = True
    counterexamples = []
    nrOfElements = len(conjunction)
    for nr in range(0, nrOfElements**2 - 1 + 1):
        a,b = baseN(nr, nrOfElements, pad=2)
        a,b = int(a), int(b)
        ab = conjunction[a][b]
        ba = conjunction[b][a]
        if ab != ba:
            counterexamples.append((a,b))
            if verbose:
                print("Not kommutative:%s*%s = %s != %s = %s*%s" % (a,b,ab,ba,a,b))
            isKommutativFlag = False
    return isKommutativFlag, counterexamples
 
def isAssociativ(conjunction, verbose=False):
    isAssociativFlag = True
    counterexamples = []
    nrOfElements = len(conjunction)
    for nr in range(0, nrOfElements**3 - 1 + 1):
        a,b,c = baseN(nr, nrOfElements, pad=3)
        a,b,c = int(a), int(b), int(c)
        ab = conjunction[a][b]
        abc1 = conjunction[ab][c]
        bc = conjunction[b][c]
        abc2 = conjunction[a][bc]
        if abc1 != abc2:
            counterexamples.append((a,b,c))
            if verbose:
                print("Not associative:(%s*%s)*%s = %s != %s = %s * (%s*%s)" % (a,b,c,abc1, abc2, a,b,c))
            isAssociativFlag = False
    return isAssociativFlag, counterexamples
 
def isConjunctionSymmetric(conjunction):
    for zeile in range(len(conjunction)):
        for spalte in range(len(conjunction)):
            if conjunction[zeile][spalte] != conjunction[spalte][zeile]:
                return False
    return True
    
def generateEmptyConjunction(nrOfElements):
    conjunction = []
    for i in range(nrOfElements):
        line = []
        for j in range(nrOfElements):
            line.append(0)
        conjunction.append(line)
    return conjunction
 
def increaseConjunction(conjunction, nrOfElements):
    i = j = 0
    conjunction[i][j] += 1
    while conjunction[i][j] == nrOfElements:
        conjunction[i][j] = 0
        j += 1
        if j == nrOfElements:
            j = 0
            i += 1
        if i == nrOfElements:
            return False
        conjunction[i][j] += 1
    return True
 
def printConjunction(conjunction, nrOfElements):
    titleLine = " * ||"
    for i in range(nrOfElements):
        titleLine += " " + str(i) + " |"
    print(titleLine)
    print("-"*len(titleLine))
    for i, line in enumerate(conjunction):
        lineTmp = " " + str(i) + " ||"
        for el in line:
            lineTmp += " " + str(el) + " |"
        print(lineTmp)
 
def getNeutralElement(conjunction, nrOfElements, verbose=False):
    leftNeutrals = []
    rightNeutrals = []
    for n in range(nrOfElements):
        nIsLeftNeutral = True
        nIsRightNeutral = True
        for el in range(nrOfElements):
            if conjunction[n][el] != el:
                nIsLeftNeutral = False
            if conjunction[el][n] != el:
                nIsRightNeutral = False
        if nIsLeftNeutral:
            leftNeutrals.append(n)
        if nIsRightNeutral:
            rightNeutrals.append(n)
    neutral = set(leftNeutrals).intersection(set(rightNeutrals))
    if verbose:
       print leftNeutrals
       print rightNeutrals
    return list(neutral)
 
def checkInverse(conjunction, nrOfElements, neutralElement):
    for el in range(nrOfElements):
        hasInverse = False
        for possibleInverse in range(nrOfElements):
            if conjunction[el][possibleInverse] == neutralElement and \
               conjunction[possibleInverse][el] == neutralElement:
                hasInverse = True
                break
        if not hasInverse:
            return False, el
    return True, -1
 
def completeCheck(conjunction, nrOfElements):
    wellformed = isWellformed(conjunction)
    associative, associativeCounterexamples = isAssociativ(conjunction)
    kommutativ, kommutativCounterexamples = isKommutativ(conjunction)
    neutrals = getNeutralElement(conjunction, nrOfElements)
    if len(neutrals) == 1:
        allHaveInverse, allHaveInverseCounterexamples = checkInverse(conjunction, nrOfElements, neutrals[0])
    else:
        allHaveInverse = False
 
    print("M = {"+",".join(map(str,list(range(nrOfElements))))+"}")
    printConjunction(conjunction, nrOfElements)
 
    if wellformed and not associative:
        print("(M,*) ist ein Magma, aber keine Halbgruppe, da (M,*) nicht assoziativ ist:")
        a,b,c = associativeCounterexamples[0]
        ab = conjunction[a][b]
        bc = conjunction[b][c]
        print(u"\t(%i*%i)*%i = %i * %i = %i \u2260 %i = %i * %i = %i*(%i*%i)" % (a,b,c,ab,c,conjunction[ab][c],conjunction[a][bc],a,bc,a,b,c))
    if wellformed and associative and not len(neutrals) == 1:
        print("(M,*) ist eine Halbgruppe, aber kein Monoid, da (M,*) kein neutrales Element besitzt.")
    if wellformed and associative and len(neutrals) == 1 and not allHaveInverse:
        print("(M,*) ist ein Monoid, aber keine Gruppe, da in (M,*) nicht alle Elemente ein Inverses haben:")
        print("\tNeutrals: %s" % str(neutrals))
        print("\t%i hat kein Inverses" % allHaveInverseCounterexamples)
    if wellformed and associative and len(neutrals) == 1 and allHaveInverse:
        print("(M,*) ist eine Gruppe.")
 
    if kommutativ:
        print("(M,*) ist kommutativ.")
    else:
        print("(M,*) ist nicht kommutativ:")
        a,b = kommutativCounterexamples[0]
        print(u"\t%i*%i = %i \u2260 %i = %i*%i" % (a,b,conjunction[a][b],conjunction[b][a],b,a))
    print("#"*80)
 
if __name__ == "__main__":
    # It is important that 0,1,2 is the order of lines and rows!
    #               0  1  2
    #               a  b  c 
    conjunction = [[0, 1, 2],
                   [1, 2, 0],
                   [2, 0, 1]]
    completeCheck(conjunction,3)
 
    #print("(M, *) is a Magma:\t%s" % str(isWellformed(conjunction)))
    #print("(M, *) is associative:\t%s" % str(isAssociativ(conjunction)))
 
    #nrOfElements = 4
    #conjunction = generateEmptyConjunction(nrOfElements)
    #checkedConjunctions = 1
    """
    while increaseConjunction(conjunction, nrOfElements):
        wellformed = isWellformed(conjunction)
        associative = isAssociativ(conjunction, False)
        kommutativ = isKommutativ(conjunction, False)
        symmetric = isConjunctionSymmetric(conjunction)
        if not kommutativ and symmetric:
            print("M = {"+",".join(map(str,list(range(nrOfElements))))+"}")
            printConjunction(conjunction, nrOfElements)
            print("(M, *) is a Magma:\t%s" % str(wellformed))
            print("(M, *) is associative:\t%s" % str(associative))
            print("(M, *) is kommutativ:\t%s" % str(kommutativ))
            isAssociativ(conjunction, True)
            print("(M, *) is symmetric:\t%s" % str(symmetric))
            break
        checkedConjunctions += 1
        if checkedConjunctions % 100000 == 0:
            print("Checked %i conjunctions." % checkedConjunctions)
    print("Finished. Checked %i conjunctions." % checkedConjunctions)
    """
