#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://stackoverflow.com/questions/1946896/conversion-from-infix-to-prefix
numerals = "0123456789"
operators = "+-*/"
braces = "()"


def predcedence(operator):
    """Return the predcedence of an operator."""
    if operator in '+-':
        return 0
    elif operator in '*/':
        return 1


def tokenize(expression):
    """Return a list of tokens."""
    tokens = []
    numeral = ""
    for char in expression:
        if char in numerals:
            numeral += char
            continue
        elif numeral != "":
            tokens.append({'type': 'number', 'value': int(numeral)})
            numeral = ""

        if char in ' \t\n\r':
            continue
        elif char in operators:
            tokens.append({'type': 'operator', 'value': char})
        elif char in braces:
            tokens.append({'type': 'brace', 'value': char})
        else:
            raise Exception("%s is not supported" % char)
    if numeral != "":
        tokens.append({'type': 'number', 'value': int(numeral)})
    return tokens


def infix2prefix(infix_expression):
    """Return the prefix notation of an arithmetic infix expression."""
    operator_stack = []
    operand_stack = []
    prefix_expression = ""

    for token in tokenize(infix_expression):
        if token['type'] == 'number':
            operand_stack.append(token['value'])
        elif token['value'] == '(' or operator_stack == [] or \
            (token['type'] == 'operator' and
                predcedence(token['value']) > predcedence(operator_stack[-1])):
            operator_stack.append(token['value'])
        elif token['value'] == ')':
            # Continue to pop operator and operand stacks, building
            # prefix expressions until left parentheses is found.
            # Each prefix expression is push back onto the operand
            # stack as either a left or right operand for the next operator.
            while operator_stack[-1] != '(':
                operator = operator_stack.pop()
                right_operand = operand_stack.pop()
                left_operand = operand_stack.pop()
                operand = (str(operator) +
                           str(left_operand) +
                           str(right_operand))
                operand_stack.Push(operand)
            operator_stack.pop()
        elif (token['type'] == 'operator' and
              predcedence(token['value']) <= predcedence(operator_stack[-1])):
            # Continue to pop operator and operand stack, building prefix
            # expressions until the stack is empty or until an operator at
            # the top of the operator stack has a lower hierarchy than that
            # of the token.
            while (operator_stack != [] and
                   predcedence(token) <= predcedence(operator_stack[-1])):
                operator = operator_stack.pop()
                right_operand = operand_stack.Pop()
                left_operand = operand_stack.Pop()
                operand = (str(operator) +
                           str(left_operand) +
                           str(right_operand))
                operand_stack.push(operand)
            operator_stack.append(token['value'])

    # If the stack is not empty, continue to pop operator and operand stacks
    # building prefix expressions until the operator stack is empty.
    while operator_stack != []:
        operator = operator_stack.pop()
        right_operand = operand_stack.pop()
        left_operand = operand_stack.pop()
        operand = str(operator) + str(left_operand) + str(right_operand)
        operand_stack.append(operand)

    # Save the prefix expression at the top of the operand stack followed
    # by popping the operand stack.

    for element in operand_stack:
        prefix_expression += element
    return prefix_expression

print(tokenize("1+2*3"))
print(infix2prefix("1+2*3"))
