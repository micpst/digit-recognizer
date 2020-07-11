import os
import time
import pygame

from window import Board

board = Board(resolution=(400, 400))

clock = pygame.time.Clock()
FPS = 60

counter = 0
index = 0
animation = [
    '.  ',
    '.. ',
    '...',
]

os.system('cls')

print('Welcome to the Number Guesser!')
print()

while True:
    board.navigate()    
    board.render()

    if counter < FPS * (4 / 10):
        counter += 1
    else: 
        counter = 0
        index = index + 1 if index < len(animation) - 1 else 0

    if board.is_edited:
        print(f'The artist is painting {animation[index]}', end="\r")
    else:
        print(f'Predicted number is {board.prediction}     ', end="\r")

    clock.tick(FPS)
