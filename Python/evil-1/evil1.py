class NotMe:
    def __eq__(self, other):
        return False

    def __hash__(self):
        return 0


a = NotMe()
print(a == a)

d = {}
d["a"] = a

print(a in d)
