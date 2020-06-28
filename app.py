import sys
import cv2
import pygame
from tensorflow.keras.models import load_model 

class Board:
    def __init__(self, resolution):
        self.window_width, self.window_heigth = resolution
        self.window = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        self.FPS = 120
        
        self.bg_mode = 'default'
        self.pen_mode = 'default'
        self.thickness = 5

        self.pointer = None
        self.prev_pointer = None    

        self.drawing = False
        self.erasing = False
        self.ctrl_holding = False

        self.window.fill(self.bg_color)
        pygame.display.set_caption('Number guesser')

    @property
    def bg_color(self):
        if self.bg_mode == 'white': return (255, 255, 255)
        if self.bg_mode == 'black': return (0  , 0  , 0  )
        return (255, 255, 255)

    @property
    def pen_color(self):
        if self.pen_mode == 'white': return (255, 255, 255)
        if self.pen_mode == 'red':   return (255, 0  , 0  )
        if self.pen_mode == 'green': return (0  , 255, 0  )
        if self.pen_mode == 'blue':  return (0  , 0  , 255)
        if self.pen_mode == 'black': return (0  , 0  , 0  )
        return (0, 0, 0)

    @property
    def color(self):
        if self.drawing: return self.pen_color
        if self.erasing: return self.bg_color

    def make_prediction(self):
        model = load_model('model.h5')


    def navigate(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

                elif e.key == pygame.K_LCTRL: self.ctrl_holding = True
                elif e.key == pygame.K_n and self.ctrl_holding: self.window.fill(self.bg_color)

                elif e.key == pygame.K_RETURN: self.make_prediction()

                elif e.key == pygame.K_1: self.bg_mode = 'black'
                elif e.key == pygame.K_2: self.bg_mode = 'white'

                elif e.key == pygame.K_q: self.pen_mode = 'black'
                elif e.key == pygame.K_w: self.pen_mode = 'white'
                elif e.key == pygame.K_r: self.pen_mode = 'red'
                elif e.key == pygame.K_g: self.pen_mode = 'green'        
                elif e.key == pygame.K_b: self.pen_mode = 'blue'

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: self.drawing = True
                elif e.button == 3: self.erasing = True

                elif e.button == 4 and self.ctrl_holding: self.thickness = min(self.thickness + 1, 25)
                elif e.button == 5 and self.ctrl_holding: self.thickness = max(self.thickness - 1, 1)

            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1: self.drawing = False
                elif e.button == 3: self.erasing = False    

            elif e.type == pygame.MOUSEMOTION:
                self.pointer = pygame.mouse.get_pos()

    def replenish(self):
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
        if self.drawing or self.erasing:
            for point in self.replenish():
                pygame.draw.circle(self.window, self.color, point, self.thickness)

            pygame.draw.circle(self.window, self.color, self.pointer, self.thickness)

    def run(self):
        while True:
            self.navigate()    
            self.render()

            self.prev_pointer = self.pointer

            pygame.display.update()      
            self.clock.tick(self.FPS)

board = Board((640, 480))
board.run()