import os
import time
import pygame

from window import Board
from console import Animation

FPS = 60
clock = pygame.time.Clock()

board = Board((400, 400))
waiting = Animation()

os.system('cls')

print()
print('Welcome to the Number Guesser!')
print()

while True:
    board.navigate()    
    board.render()

    if waiting.counter < FPS * (4 / 10):
        waiting.tick()
    else: 
        waiting.reset()

    if board.is_edited:
        print(f'The artist is painting {waiting.frame}', end="\r")
    else:
        print(f'Predicted number is {board.prediction}     ', end="\r")

    clock.tick(FPS)