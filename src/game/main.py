'''
TODO
-refactor reaction.py to accept a shared surface on global display 
'''

import pygame

from game.reaction import reaction_test_mngr
from game.speedometer import shock_meter_mngr

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((1600, 1200))
display.fill(WHITE)
subsurf = display.subsurface((400, 500), (800, 300))

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