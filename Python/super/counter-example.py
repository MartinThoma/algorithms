from collections import Counter, OrderedDict


class OrderedCounter(Counter):
     'Counter that remembers the order elements are first seen'
     def __repr__(self):
         return '{}({!r})'.format(self.__class__.__name__,
                            OrderedDict(self))
     def __reduce__(self):
         return self.__class__, (OrderedDict(self),)


print(Counter('rabarbabarbara'))
print(OrderedCounter('rabarbabarbara'))
