'''
TODO
-refactor reaction.py to accept a shared surface on global display 
'''

import pygame
import pandas as pd
import numpy as np

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

subsurf_w = screen_w - 200
subsurf_h = 200
subsurf_x = (info.current_w / 2) - (subsurf_w / 2)
subsurf_y = (info.current_h / 2) - (subsurf_h / 2)
subsurf = display.subsurface((subsurf_x, subsurf_y), (subsurf_w, subsurf_h))

def main(trials: int):
    data = []
    react_mngr = reaction_test_mngr(subsurf, data)
    shock_mngr = shock_meter_mngr(display, subsurf, data)

    trial = 1
    while trial <= trials:
        data.append(trial)
        data.append('W') # TODO hard coded W/L change this
        shock_mngr.draw_circles()
        if not react_mngr.run():
            break
        if not shock_mngr.shock_loop():
            break
        trial += 1

    # Bad 
    df = np.empty((0,5))
    for i in range(0, len(data), 5):
        dr = []
        for j in range(i, i+5):
            dr.append(data[j])
        df = np.append(df, np.array([dr]), axis=0)

    df = pd.DataFrame(df)
    return df

if __name__ == "__main__":
    main(1)