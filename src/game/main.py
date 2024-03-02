'''
TODO
-refactor reaction.py to accept a shared surface on global display 
'''

import pygame

from reaction import reaction_test_mngr
from speedometer import shock_meter_mngr

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
clock = pygame.time.Clock()

info = pygame.display.Info()
screen_w = info.current_w
screen_h = info.current_h

display = pygame.display.set_mode((screen_w, screen_h))
display.fill(WHITE)

subsurf_w = 400
subsurf_h = 200
subsurf_x = (info.current_w / 2) - (subsurf_w / 2)
subsurf_y = (info.current_h / 2) - (subsurf_h / 2)
subsurf = display.subsurface((subsurf_x, subsurf_y), (subsurf_w, subsurf_h))

def main():
    react_mngr = reaction_test_mngr(subsurf)
    shock_mngr = shock_meter_mngr(display, subsurf)

    while True:
        shock_mngr.draw_circles()
        if not react_mngr.run():
            break
        if not shock_mngr.shock():
            break

if __name__ == "__main__":
    main()