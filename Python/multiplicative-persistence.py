def main():
    persistance_dict = {}
    for i in range(1, 100000):
        steps = get_persistence(i)
        if steps not in persistance_dict:
            persistance_dict[steps] = i
            print((steps, i))
    return persistance_dict

def get_persistence(i: int) -> int:
    steps = 0
    while len(str(i)) > 1:
        i = mult(i)
        steps += 1
    return steps

def mult(i: int) -> int:
    prod = 1
    for digit in [int(c) for c in str(i)]:
        prod *= digit
    return prod

if __name__ == "__main__":
    print(main())
