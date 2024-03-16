'''
TODO
-refactor reaction.py to accept a shared surface on global display 
'''

import pygame, random
import pandas as pd
import numpy as np

from reaction import reaction_test_mngr
from speedometer import shock_meter_mngr

def init():
    pygame.init()

    info = pygame.display.Info()
    screen_w = info.current_w
    screen_h = info.current_h

    display = pygame.display.set_mode((screen_w, screen_h))
    display.fill((255, 255, 255))

    subsurf_w = screen_w - 200
    subsurf_h = 200
    subsurf_x = (info.current_w / 2) - (subsurf_w / 2)
    subsurf_y = (info.current_h / 2) - (subsurf_h / 2)
    subsurf = display.subsurface((subsurf_x, subsurf_y), (subsurf_w, subsurf_h))

    return (display, subsurf)

def main(trials: int):
    display, subsurf = init()

    data = []
    react_mngr = reaction_test_mngr(subsurf, data)
    shock_mngr = shock_meter_mngr(display, subsurf, data)

    trial = 1
    while trial <= trials:
        data.append(trial)
        shock_mngr.draw_circles()
        if not react_mngr.run():
            break
        
        # Change this
        wl = random.choice([True, True])
        data.append(('W' if wl else 'L'))
        shock_fn = shock_mngr.shock_loop if wl else shock_mngr.loser_loop

        if not shock_fn():
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
    pygame.quit()

    return df

if __name__ == "__main__":
    main()