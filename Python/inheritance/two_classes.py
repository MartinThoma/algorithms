class ParentA:
    def hello(self):
        print("ParentA")


class ParentB:
    def hello(self):
        print("ParentB")


class Child(ParentA, ParentB):
    pass


a = Child()
a.hello()
