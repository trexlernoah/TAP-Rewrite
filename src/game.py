import pygame

from reaction import ReactionTest
from shock import ShockMeter
from drawer import Drawer
from classes import Trial, Data
from typing import List


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


def play(subject_id, trials: List[Trial]):
    if len(trials) <= 0:
        return
    display, subsurf = init()
    main_data = Data()

    drawer = Drawer(display, subsurf)
    react_mngr = ReactionTest(drawer, main_data)
    shock_mngr = ShockMeter(drawer, main_data)

    for i, trial in enumerate(trials):
        drawer.reset_meter(0)

        reaction_data = react_mngr.run(i == 0)
        if not reaction_data:
            break

        wl = trial.wl == "Win"
        main_data.current_data_row.wl = "W" if wl else "L"

        if wl:
            trial_data = shock_mngr.win_loop()
            if trial_data is None:
                break
        else:
            shock_level = int(trial.shock)
            shock_mngr.lose_loop(shock_level)

        main_data.finish_trial()

    pygame.quit()

    return main_data
