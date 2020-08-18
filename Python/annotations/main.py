import inspect


def log_action(func, *args, **kwargs):
    print("=" * 80)
    print(func)
    print(args)
    print(kwargs)
    print("-" * 80)
    return func

def dump_args(func):
    """Decorator to print function call details - parameters names and effective values.
    """
    def wrapper(*args, **kwargs):
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str =  ', '.join('{} = {!r}'.format(*item) for item in func_args.items())
        print(f'{func.__module__}.{func.__qualname__} ( {func_args_str} )')
        return func(*args, **kwargs)
    return wrapper


from dataclasses import dataclass


@dataclass
class User:
    name: str
    health : int
    attack : int

    @dump_args
    def strike(self, other: "User"):
        print(f"{self.name} strikes {other.name} with {self.attack}!")
        other.health -= self.attack


a = User(name="Anna", health=12, attack=2)
b = User(name="Bob", health=5, attack=10)

print(a.__annotations__)
print(User.__annotations__)

print(getattr(a, "health"))

a.strike(b)
