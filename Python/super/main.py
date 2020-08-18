class A:
    def __init__(self):
        print("A")
        super().__init__()

class B1(A):
    def __init__(self):
        print("B1")
        super().__init__()

class B2(A):
    def __init__(self):
        print("B2")
        super().__init__()

class C(B1, A):
    def __init__(self):
        print("C")
        super().__init__()

C()
