opening = "[{("
pair = {"(": ")", "[": "]", "{": "}"}
stack = []
for bracket in input():
    if bracket in opening:
        stack.append(bracket)
    else:
        if len(stack) == 0:
            print(0)
        popped = stack.pop()
        if pair[popped] != bracket:
            print(0)
print(len(stack) == 0)
