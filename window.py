import sys
import cv2
import pygame
import numpy as np

from typing import Tuple, Generator
from tensorflow.keras.models import load_model

class Pointer:

    def __init__(
        self, 
        window: pygame.Surface,
        position: Tuple[int, int],
        color: Tuple[int, int, int], 
        thickness: int
    ) -> None:

        '''
        Constructor for the `Pointer` class.
        Constructor arguments:
        :param window: ref to the window that pointer belongs to.
        :param position: current position of the pointer.
        :param color: color of the pointer.
        :param thickness: thickness of the pointer.
        '''

        self.color = color
        self.window = window
        self.position = position
        self._thickness = thickness

    @property
    def thickness(self) -> int:
        
        return self._thickness

    @thickness.setter
    def thickness(self, val: int) -> None:
        
        if 5 < val < 20:
            self._thickness = val

    def draw(self, position: Tuple[int, int]) -> None:
        
        self.position = position
        pygame.draw.circle(self.window, self.color, self.position, self.thickness)


class Board:

    COLORS = {
        'white': (255, 255, 255),
        'red':   (255, 0  , 0  ),
        'green': (0  , 255, 0  ),
        'blue':  (0  , 0  , 255),
        'black': (0  , 0  , 0  ),
    }

    def __init__(self, resolution: Tuple[int, int]) -> None:

        '''
        Constructor for the `Board` class.
        Constructor argument:
        :param resolution: resolution of the system window.
        '''
        
        self.width, self.heigth = resolution
        self.window = pygame.display.set_mode(resolution)
        self._background = self.COLORS['white']

        self.pen    = Pointer(self.window, None, self.COLORS['black'], 10)
        self.rubber = Pointer(self.window, None, self.COLORS['white'], 10)

        self.pointer = self.pen

        self.is_active = False
        self.is_edited = True
        self.CTRL_hold = False

        self.window.fill(self._background)
        pygame.display.set_caption('Number guesser')

    @property
    def canvas(self) -> pygame.PixelArray:

        surface = pygame.display.get_surface()
        pxarray = pygame.PixelArray(surface)
        
        return pxarray

    @property
    def background(self) -> Tuple[int, int, int]:
        
        return self._background

    @background.setter
    def background(self, color: Tuple[int, int, int]) -> None:

        for y in range(self.heigth):
            for x in range(self.width):
                if self.canvas[x, y] == self.canvas.surface.map_rgb(self.background):
                    self.canvas[x, y] = color

        self._background = color

    def navigate(self) -> None:

        '''
        Reads user input and updates app state.
        '''

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

                elif e.key == pygame.K_RETURN: 
                    self.is_edited = False

                elif e.key == pygame.K_LCTRL: 
                    self.CTRL_hold = True

                elif e.key == pygame.K_n and self.CTRL_hold: 
                    self.window.fill(self.background)

                elif e.key == pygame.K_1 and self.CTRL_hold: 
                    self.background = self.COLORS['black']
                    self.rubber.color = self.COLORS['black']

                elif e.key == pygame.K_2 and self.CTRL_hold: 
                    self.background = self.COLORS['white']
                    self.rubber.color = self.COLORS['white']
  
                elif e.key == pygame.K_q: self.pen.color = self.COLORS['black']
                elif e.key == pygame.K_w: self.pen.color = self.COLORS['white']
                elif e.key == pygame.K_r: self.pen.color = self.COLORS['red']               
                elif e.key == pygame.K_g: self.pen.color = self.COLORS['green']        
                elif e.key == pygame.K_b: self.pen.color = self.COLORS['blue']

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: 
                    self.pointer = self.pen
                    self.is_active = True
                    self.is_edited = True

                elif e.button == 3: 
                    self.pointer = self.rubber
                    self.is_active = True
                    self.is_edited = True

                elif e.button == 4 and self.CTRL_hold: self.pointer.thickness += 1
                elif e.button == 5 and self.CTRL_hold: self.pointer.thickness -= 1

            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1 or e.button == 3: 
                    self.is_active = False
                    self.pointer.position = None

    def fill(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:

        '''
        Generates points to fill gap between 2 pointer positions.
        '''

        if p1 is None: return p2

        x1, y1 = p1
        x2, y2 = p2

        dx, dy = x1 - x2, y1 - y2
        n = max(abs(dx), abs(dy))
        
        for i in range(n):
            progress = 1. * i / n
            aprogress = 1 - progress
            x = int(aprogress * x1 + progress * x2)
            y = int(aprogress * y1 + progress * y2)
            yield (x, y)

    def render(self) -> None:

        '''
        Renders board screen.
        '''

        if self.is_active:
            prev_pos = self.pointer.position
            curr_pos = pygame.mouse.get_pos()

            if 0 < curr_pos[0] < self.width-1 and 0 < curr_pos[1] < self.heigth-1:          
                for point in self.fill(prev_pos, curr_pos):
                    self.pointer.draw(point)

                self.pointer.draw(curr_pos)
            else:
                self.pointer.position = None
        
        pygame.display.update()