from enum import Enum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (225, 225, 225) 
RED = (255, 0, 0)

BG = WHITE
FG = BLACK

class game_state(Enum):
    START = 1
    READY = 2
    HOLD = 3
    SHOCK = 4

class Trial(object):
    def __init__(self, wl, shock, feedback):
        self.wl = wl
        self.shock = shock
        self.feedback = feedback

initial_state = {'filename': "",
         'instruction': "Enter instructions here",
         'trial-count': 0,
         'trials': []}