import Pyro4
thing = Pyro4.Proxy("PYRO:obj_e546476caf4b4e768e95fed5d60fdfa1@localhost:35758")
print(thing.method(42))   # prints 84
