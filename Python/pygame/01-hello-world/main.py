import pygame
import sys
from dataclasses import dataclass
from typing import Tuple
import random

BALL_DEFAULT_SPEED = 2
PADDLE_WIDTH = 10
MAX_Y_BOARD = 500
MAX_X_BOARD = 500

@dataclass
class Position:
    x: int
    y: int

    def size(self):
        return (self.x**2 + self.y**2)**0.2

@dataclass
class Ball:
    position : Position
    direction: Position

    def reset(self):
        self.position = Position(MAX_X_BOARD//2, MAX_Y_BOARD//2)
        self.direction = Position(3, random.randint(-3, 3))
        self.set_speed(BALL_DEFAULT_SPEED)

    def set_speed(self, desired_speed: float):
        speed = self.direction.size()
        if speed == 0:
            self.direction = Position(3, 5)
        else:
            factor = desired_speed / speed
            self.direction = Position(self.direction.x * factor, self.direction.y * factor)

@dataclass
class Paddle:
    position : Position
    points : int = 0
    size: int = 100
    speed: int = 10

    def sanitize_position(self):
        if self.position.y < 0:
            self.position.y = 0
        if self.position.y > MAX_Y_BOARD:
            self.position.y = MAX_Y_BOARD

def has_overlap(i1: Tuple[int, int], i2: Tuple[int, int]) -> bool:
    if not i1[0] <= i1[1]:
        i1 = (i1[1], i1[0])
    if not i2[0] <= i2[1]:
        i2 = (i2[1], i2[0])
    i1_left_of_i2 = i1[1] < i2[0]
    i2_left_of_i1 = i2[1] < i1[0]
    return not (i1_left_of_i2 or i2_left_of_i1)


@dataclass
class Game:
    player1 = Paddle(position=Position(10, MAX_Y_BOARD // 2))
    player2 = Paddle(position=Position(MAX_X_BOARD, MAX_Y_BOARD // 2))
    ball = Ball(position=Position(150, 150), direction=Position(3, -5))

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = pygame.display.set_mode([600, 600])
        self.clock = pygame.time.Clock()
        self.ball.set_speed(BALL_DEFAULT_SPEED)

    def clear(self):
        self.screen.fill((0, 0, 0))

    def render(self):
        self.clear()
        pygame.draw.rect(self.screen, (255, 255, 0), (self.player1.position.x, self.player1.position.y, PADDLE_WIDTH, self.player1.size))
        pygame.draw.rect(self.screen, (255, 255, 0), (self.player2.position.x, self.player2.position.y, PADDLE_WIDTH, self.player2.size))
        pygame.draw.circle(self.screen, (255, 255, 0), (self.ball.position.x, self.ball.position.y), radius=10)
        text_surface = self.my_font.render(f'Score {self.player1.points} : {self.player2.points}', False, (255, 0, 0))
        self.screen.blit(text_surface, (MAX_X_BOARD //2, MAX_Y_BOARD + 10))
        pygame.display.update()

    def tick(self):
        # Update the human player
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player1.position.y -= self.player1.speed
        if pressed[pygame.K_DOWN]:
            self.player1.position.y += self.player1.speed
        self.player1.sanitize_position()

        # Update second player
        if pressed[pygame.K_w]:
            self.player2.position.y -= self.player2.speed
        if pressed[pygame.K_s]:
            self.player2.position.y += self.player2.speed
        self.player2.sanitize_position()

        # Update the ball
        x_prev = self.ball.position.x
        y_prev = self.ball.position.y
        self.ball.position.x += self.ball.direction.x
        self.ball.position.y += self.ball.direction.y
        if self.ball.position.y <= 0 or self.ball.position.y >= MAX_Y_BOARD:
            # Ball goes of to the top / bottom
            self.ball.direction.y *= -1

        x_after = self.ball.position.x
        y_after = self.ball.position.y

        if min(x_prev, x_after) <= self.player1.position.x <= max(x_prev, x_after):
            # Potential hit if the paddle was in the right position
            if has_overlap((y_prev, y_after), (self.player1.position.y, self.player1.position.y + self.player1.size)):
                if self.ball.direction.x < 0:
                    self.ball.direction.x *= -1

        if min(x_prev, x_after) <= self.player2.position.x <= max(x_prev, x_after):
            # Potential hit if the paddle was in the right position
            if has_overlap((y_prev, y_after), (self.player2.position.y, self.player2.position.y + self.player2.size)):
                if self.ball.direction.x > 0:
                    self.ball.direction.x *= -1

        ball_x = self.ball.position.x
        if ball_x <= self.player1.position.x - 50:
            self.player2.points += 1
            self.ball.reset()

        if ball_x >= self.player2.position.x + 50:
            self.player1.points += 1
            self.ball.reset()

        self.clock.tick(60)

if __name__ == "__main__":
    game = Game()

    go = True
    while go:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        game.render()
        game.tick()

