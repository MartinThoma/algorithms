from dataclasses import dataclass, field
from typing import List


@dataclass
class Peg:
    name: str
    values: List[int] = field(default_factory=lambda: [])

    def __str__(self):
        return self.name


def solve(n, source_peg, target_peg, auxillary_peg):
    if n == 1:
        print(f"Move disk 1 from {source_peg} to {target_peg}")
        return [(source_peg.name, target_peg.name)]
    else:
        moves = solve(n - 1, source_peg, auxillary_peg, target_peg)
        moves.append((source_peg.name, target_peg.name))
        print(f"Move disk {n} from {source_peg} to {target_peg}")
        moves += solve(n - 1, auxillary_peg, target_peg, source_peg)
        return moves


if __name__ == "__main__":
    moves = solve(
        3,
        source_peg=Peg("Peg1", [1, 2, 3]),
        target_peg=Peg("Peg2"),
        auxillary_peg=Peg("Peg3"),
    )
    print(moves)
    print(len(moves))
