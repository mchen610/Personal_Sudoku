import pygame
import random
import sys
import json
from os import path
from colors import *

if __name__ == '__main__':
    desktop = path.join(path.expanduser("~"), "Desktop")
    file_path = path.join(desktop, "true_font_size.txt")
    clock = pygame.time.Clock()


    pygame.init()
    dim = (1000,600)
    screen = pygame.display.set_mode((dim[0],dim[1]))
    screen.fill((BLACK))

    real_rect = pygame.rect.Rect((0,0), dim)
    real_rect.center = screen.get_rect().center

    COLOR = GREEN

    font_list = []
    offset_list = []
    #with open(file_path, 'w') as file:
    if True:
        for font_size in range(5,800):
            
            screen.fill(BLACK)
            
            
            font = pygame.font.Font(None, font_size)
            render = font.render('B', True, COLOR)
            font_rect = render.get_rect(center = real_rect.center)
            font_rect.centery = font_rect.centery+font_size*0.04442-0.4680
            screen.blit(render, font_rect)
            pygame.draw.rect(screen, COLOR, real_rect, 1)
            text_top = -1
            text_bot = -1

            rect_centery = dim[1]//2+1
            
            #0 and height-1 are the border
            i = 0
            while text_top < 0 or text_bot < 0:
                
                for y in range(1,dim[1]//2):
                    pos = (dim[0]//2+i,y)
                    color = screen.get_at(pos)[1]

                    #get center of text and and size of text
                    #offset -> move down the difference in pixels between text center and rectangle center for each font_size
                    if color > 0:
                        text_top = y

                        break

                for y in range(dim[1]-2,dim[1]//2,-1):
                    pos = (dim[0]//2+i,y)
                    color = screen.get_at(pos)[1]

                    #get center of text and and size of text
                    #offset -> move down the difference in pixels between text center and rectangle center for each font_size
                    if color > 0:
                        text_bot = y

                        break
                
                i = i+1

            
            
            letter_height = text_bot-text_top+1
            letter_centery = text_top + letter_height//2 + 1

            offset = rect_centery - letter_centery

            #font_list.append(font_size)
            #offset_list.append(offset)
            try:
                file.write(f"{font_size}\t{letter_height}\n")        
            except:
                pass

            
            #file.write(me_talking+'\n')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

        #with open(file_path, "a+", encoding='utf-8') as file:
            #json.dump({'font_size': font_list, 'offset': offset_list}, file)

    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

