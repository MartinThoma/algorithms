# Core Library modules
import enum
from typing import List, Tuple, cast, Union

# Third party modules
import numpy as np


def main():
    game = Game(n=10, m=10, nb_mines=10)
    while game.is_running:
        game.take_step()


class PlayerFieldState(enum.Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    UNDISCOVERED = 9
    EXPLODED_BOMB = 10
    MARKED = 11


class PlayerAction(enum.Enum):
    EXPLORE = 0
    MARK = 1


field_state2str = {
    0: "  ",
    1: "1 ",
    2: "2 ",
    3: "3 ",
    4: "4 ",
    5: "5 ",
    6: "6 ",
    7: "7 ",
    8: "8 ",
    PlayerFieldState.UNDISCOVERED: "? ",
    PlayerFieldState.EXPLODED_BOMB: "💥",
    PlayerFieldState.MARKED: "📌",
}


class Game:
    def __init__(self, n: int, m: int, nb_mines: int):
        self.mine_field = Game.create_field(n, m, nb_mines)
        self.player_field: List[List[Union[int, PlayerFieldState]]] = [
            [PlayerFieldState.UNDISCOVERED for _ in range(m)] for _ in range(n)
        ]
        self.is_running = True
        self.nb_mines = nb_mines
        self.nb_marked = 0

    @staticmethod
    def create_field(n: int, m: int, nb_mines: int) -> List[List[bool]]:
        field = np.zeros(n * m, dtype=bool)
        for i in range(nb_mines):
            field[i] = True
        np.random.shuffle(field)
        field = field.reshape((n, m))
        return field.tolist()

    def print_field(self, uncover: bool = False):
        top_line = ["  "] + [str(y) + " " for y in range(len(self.player_field[0]))]
        top_line_str = " ".join(top_line)
        print(top_line_str)
        print("-" * len(top_line_str))
        for x, line in enumerate(self.player_field):
            to_print = [str(x) + "|"]
            for y, field in enumerate(line):
                el = field_state2str[field]
                if uncover:
                    if (
                        self.mine_field[x][y]
                        and field != PlayerFieldState.EXPLODED_BOMB
                    ):
                        el = "💣"
                    if field == PlayerFieldState.MARKED:
                        if not self.mine_field[x][y]:
                            el = "😖"
                        else:
                            el = "📌"
                to_print.append(el)
            print(" ".join(to_print))
        print("-" * len(top_line_str))
        print(top_line_str)

    def take_step(self):
        self.print_field()
        x, y, step_type = self.get_valid_input()
        if step_type == PlayerAction.MARK:
            self.take_step_mark_bomb(x, y)
        elif step_type == PlayerAction.EXPLORE:
            self.take_step_explore(x, y)
        else:
            raise ValueError(f"step_type={step_type} is not known")

    def take_step_mark_bomb(self, x: int, y: int):
        if self.player_field[x][y] == PlayerFieldState.MARKED:
            self.player_field[x][y] = PlayerFieldState.UNDISCOVERED
            self.nb_marked -= 1
        elif self.player_field[x][y] == PlayerFieldState.UNDISCOVERED:
            self.player_field[x][y] = PlayerFieldState.MARKED
            self.nb_marked += 1
            self.check_win_condition()

    def take_step_explore(self, x: int, y: int):
        if self.player_field[x][y] == PlayerFieldState.MARKED:
            print(f"Please unmark ({x},{y}) before you hit it.")
        elif self.mine_field[x][y]:
            self.player_field[x][y] = PlayerFieldState.EXPLODED_BOMB
            self.is_running = False
            print("Game over")
            self.print_field(uncover=True)
        else:
            self.uncover(x, y)

    def check_win_condition(self):
        if self.nb_marked == self.nb_mines:
            print(
                f"You have marked {self.nb_marked} fields with mines. "
                "This is equal to the number of hidden mines."
            )
            stop_game = get_yes_no("Do you want to finish the game?")
            if stop_game:
                self.is_running = False
                if self.are_mines_marked_correctly():
                    print("You won!")
                else:
                    print("You lose!")
                    self.print_field(uncover=True)

    def uncover(self, x: int, y: int):
        adjacent_mines = self.get_adjacent_mines(x, y)
        self.player_field[x][y] = adjacent_mines
        if adjacent_mines == 0:
            for xn, yn in self.get_neighbors(x, y):
                if self.player_field[xn][yn] == PlayerFieldState.UNDISCOVERED:
                    self.uncover(xn, yn)

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors = []
        for xd in [-1, 0, 1]:
            for yd in [-1, 0, 1]:
                if xd == 0 and yd == 0:
                    continue
                if self.is_on_field(x + xd, y + yd):
                    neighbors.append((x + xd, y + yd))
        return neighbors

    def get_adjacent_mines(self, x: int, y: int) -> int:
        adjacent_mines = 0
        for xn, yn in self.get_neighbors(x, y):
            adjacent_mines += self.is_mine(xn, yn)
        return adjacent_mines

    def is_on_field(self, x: int, y: int) -> bool:
        return 0 <= x < len(self.mine_field) and 0 <= y < len(self.mine_field[0])

    def is_mine(self, x: int, y: int) -> bool:
        if not self.is_on_field(x, y):
            return False
        return self.mine_field[x][y]

    def get_valid_input(self) -> Tuple[int, int, PlayerAction]:
        position = None
        while not self.is_valid_input(position):
            position = input(
                "Where would you like to hit " "(add ',m' if you want to mark a bomb)? "
            )
        position = cast(str, position)
        splitted = position.split(",")
        x = int(splitted[0])
        y = int(splitted[1])
        if len(splitted) == 3:
            if splitted[2] == "m":
                t = PlayerAction.MARK
            else:
                t = PlayerAction.EXPLORE
        else:
            t = PlayerAction.EXPLORE
        return x, y, t

    def is_valid_input(self, position):
        if position is None:
            return False
        if "," not in position:
            return False
        splitted = position.split(",")
        x = splitted[0]
        y = splitted[1]
        if len(splitted) == 3:
            t = splitted[2]
            if t not in ["m", "b"]:
                return False
        try:
            x = int(x)
            y = int(y)
            if not self.is_on_field(x, y):
                return False
            return True
        except:
            return False

    def are_mines_marked_correctly(self):
        for x, line in enumerate(self.mine_field):
            for y, is_mine in enumerate(line):
                if is_mine:
                    if self.player_field[x][y] != PlayerFieldState.MARKED:
                        return False
                else:
                    if self.player_field[x][y] == PlayerFieldState.MARKED:
                        return False
        return True


def get_yes_no(message: str) -> bool:
    value = input(message)
    while value not in ["Y", "y", "N", "n", "yes", "no", "1", "0"]:
        value = input(message + " [y/n] ")
    return value in ["Y", "y", "yes", "1"]


if __name__ == "__main__":
    main()
