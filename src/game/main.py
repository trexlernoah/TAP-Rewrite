'''
TODO
-refactor reaction.py to accept a shared surface on global display 
'''

import pygame

from reaction import reaction_test_mngr
from speedometer import shock_meter_mngr

from utils import *

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

def main(subject_id, trials: list[Trial]):
    if len(trials) <= 0: return
    display, subsurf = init()
    print('subj id %s' % subject_id)
    # TODO replace with subj id and thresholds
    main_data = Data(subject_id, 0, 0)

    react_mngr = reaction_test_mngr(subsurf, main_data)
    shock_mngr = shock_meter_mngr(display, subsurf, main_data)

    trial = 0
    main_data.generate_new_data(trial+1)
    while trial < len(trials):
        shock_mngr.draw_circles() 

        reaction_data = react_mngr.run(trial == 0)
        if not reaction_data:
            break

        # Change this
        wl = trials[trial].wl == 'Win'
        main_data.current_data_row.wl = ('W' if wl else 'L')

        if wl:
            trial_data = shock_mngr.shock_loop()
            if trial_data is None:
                break
        else:
            shock_mngr.loser_loop(int(trials[trial].shock))
            
        main_data.save_and_flush_data()
        trial += 1

    pygame.quit()

    return main_data

if __name__ == "__main__":
    main()