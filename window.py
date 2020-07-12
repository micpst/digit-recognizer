import sys
import cv2
import pygame
import numpy as np

from tensorflow.keras.models import load_model


class Board:


    '''
    Board creates system window in which you can draw whatever you want using mouse.
    Board has also access to keras model that was trained to recognise numbers and 
    uses it to guess number you draw on screen.
    Class uses pygame and tensorflow backend.
    '''


    def __init__(self, resolution):
        self.width, self.heigth = resolution
        self.window = pygame.display.set_mode(resolution)

        self.model = load_model('model.h5')
        self.prediction = None

        self.colors = {
            'white': (255, 255, 255),
            'red':   (255, 0  , 0  ),
            'green': (0  , 255, 0  ),
            'blue':  (0  , 0  , 255),
            'black': (0  , 0  , 0  ),
        }

        self.background_color = self.colors['white']
        self.pen_color = self.colors['black']
        self.pointer_color = self.pen_color
        self.thickness = 10

        self.pointer = None
        self.prev_pointer = None

        self.is_active = False
        self.is_edited = True
        self.CTRL_hold = False

        self.window.fill(self.background_color)
        pygame.display.set_caption('Number guesser')


    @property
    def surface(self):

        '''
        Array of surface pixels value.
        '''

        pixels = np.zeros((self.heigth, self.width, 3), dtype='float32')
        surface = pygame.display.get_surface()

        for y in range(self.heigth):
            for x in range(self.width):
                color = surface.get_at((x, y))
                pixels[y][x] = np.array([color.r, color.g, color.b])

        return pixels


    def change_background_color(self, color):
        surface = pygame.display.get_surface()

        for y in range(self.heigth):
            for x in range(self.width):
                pixel_color = surface.get_at((x, y))

                if pixel_color == pygame.Color(*self.background_color):
                    surface.set_at((x, y), pygame.Color(*self.colors[color])) 

        self.background_color = self.colors[color]


    def quess(self): 

        '''
        Uses leNet model to predict a number from the board surface.
        Prints predicted number to the console.
        '''

        img = cv2.resize(self.surface, (28, 28))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        img = img.reshape(1, *img.shape, 1)
        img = img / 255
    
        [prediction] = self.model.predict_classes(img)
        self.prediction = prediction


    def navigate(self):

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

                elif e.key == pygame.K_LCTRL: 
                    self.CTRL_hold = True

                elif e.key == pygame.K_1 and self.CTRL_hold: 
                    self.change_background_color('black')

                elif e.key == pygame.K_2 and self.CTRL_hold: 
                    self.change_background_color('white')

                elif e.key == pygame.K_n and self.CTRL_hold: 
                    self.window.fill(self.background_color)

                elif e.key == pygame.K_RETURN: 
                    self.is_edited = False
                    self.quess()
  
                elif e.key == pygame.K_q: self.pen_color = self.colors['black']
                elif e.key == pygame.K_w: self.pen_color = self.colors['white']
                elif e.key == pygame.K_r: self.pen_color = self.colors['red']               
                elif e.key == pygame.K_g: self.pen_color = self.colors['green']        
                elif e.key == pygame.K_b: self.pen_color = self.colors['blue']

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: 
                    self.pointer_color = self.pen_color
                    self.is_active = True
                    self.is_edited = True

                elif e.button == 3: 
                    self.pointer_color = self.background_color
                    self.is_active = True
                    self.is_edited = True

                elif e.button == 4 and self.CTRL_hold: self.thickness = min(self.thickness + 1, 20)
                elif e.button == 5 and self.CTRL_hold: self.thickness = max(self.thickness - 1, 10)

            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1 or e.button == 3: 
                    self.is_active = False

            elif e.type == pygame.MOUSEMOTION: 
                self.prev_pointer = self.pointer
                self.pointer = pygame.mouse.get_pos()


    def replenish(self):

        '''
        Generates points to fill gap between 2 pointer positions.
        '''

        x1, y1 = self.pointer
        x2, y2 = self.prev_pointer

        dx, dy = x1 - x2, y1 - y2
        n_iters = max(abs(dx), abs(dy))
        
        for i in range(n_iters):
            progress = 1.0 * i / n_iters
            aprogress = 1 - progress
            x = int(aprogress * x1 + progress * x2)
            y = int(aprogress * y1 + progress * y2)
            yield (x, y)


    def render(self):

        '''
        Renders board screen.
        '''

        if self.is_active:

            for point in self.replenish():
                pygame.draw.circle(self.window, self.pointer_color, point, self.thickness)
            
            pygame.draw.circle(self.window, self.pointer_color, self.pointer, self.thickness)    
        
        pygame.display.update()
       