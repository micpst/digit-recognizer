import sys
import cv2
import pygame
import numpy as np
import tensorflow as tf
from window import Board

def preprocess(img: pygame.PixelArray) -> np.array: 

    src = np.zeros((*img.shape, 3), dtype="uint8")

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            mapped_int = img[x, y] 
            color = img.surface.unmap_rgb(mapped_int)
            src[y][x] = [color.r, color.g, color.b]
    
    img = cv2.resize(src, (28, 28), interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img.reshape(1, *img.shape, 1)
    img = img / 255
    return img

if __name__ == "__main__":

    pygame.init()

    name = sys.argv[1] if len(sys.argv) > 1 else "model.h5"
    model = tf.keras.models.load_model(name)
    
    FPS = 60
    clock = pygame.time.Clock()
    board = Board((400, 400))
    is_running = True

    while is_running:

        for e in pygame.event.get():       
            
            if e.type == pygame.QUIT:
                is_running = False

            elif e.type == pygame.KEYDOWN: 

                if e.key == pygame.K_ESCAPE:
                    is_running = False

                elif e.key == pygame.K_RETURN:
                    img = preprocess(board.canvas)
                    [ prediction ] = model.predict_classes(img)
                    print(f"Predicted number is {prediction}") 
            
            board.listen(e)

        board.draw()
        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()