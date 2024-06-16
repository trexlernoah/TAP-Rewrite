from enum import Enum
import pygame, random

# display = pygame.display.set_mode((640, 480))
# pygame.display.set_caption("Reaction Time Test")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

BG = WHITE
FG = BLACK

class game_state(Enum):
    START = 1
    READY = 2
    HOLD = 3
    SHOCK = 4

class reaction_test_mngr():
    '''Reaction test drawing'''
    def __init__(self, display: pygame.Surface, dr: list):
        self.display = display
        self.dr = dr

        self.font = pygame.font.SysFont(None, 30)

    def render(self, text, color, delay = 0):
        self.display.fill(BG)
        text_block = self.font.render(text, 1, color)
        self.display.blit(text_block, text_block.get_rect(center = self.display.get_rect().center))
        pygame.display.flip()
        pygame.time.wait(delay)

    def start_loop(self):
        self.render("PRESS SPACEBAR TO START TEST", FG)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.render("", FG, 7650)
                    return True

    def ready_loop(self):
        self.render("GET READY!", FG, 3700)
        self.render("PRESS SPACEBAR", FG)

        timer_start = pygame.time.get_ticks()

        while True:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - timer_start

            if delta_time >= 3000:
                    self.render("PLEASE PRESS THE SPACEBAR", FG)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return True

    def hold_loop(self):
        self.render("PRESS SPACEBAR", FG)

        timer_start = pygame.time.get_ticks()
        timer_release = timer_start + random.randint(2000, 4000)

        while True:
            current_time = pygame.time.get_ticks()

            if current_time >= timer_release:
                self.render("RELEASE", RED)

            for event in pygame.event.get():
                if event.type == pygame.TEXTINPUT and event.text == ' ':
                    if current_time > timer_release + 1000:
                        self.render("YOU WAITED TOO LONG", FG, 3700)
                        return False
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    if current_time < timer_release:
                        self.render("YOU RELEASED TOO SOON", FG, 3700)
                        return False
                    else:
                        reaction_time = current_time - timer_release
                        print("ReactionTime: %d ms" % (reaction_time))
                        self.dr[4] = str(reaction_time)
                        return True
            pygame.display.flip()


    def run(self):
        # Change this
        # Only show "Press spacebar to start" on first iteration
        current_state = game_state.START if self.dr[0] == 1 else game_state.READY

        while True:
            if current_state == game_state.START:
                current_state = game_state.READY if self.start_loop() else game_state.START
            elif current_state == game_state.READY:
                current_state = game_state.HOLD if self.ready_loop() else game_state.READY
            elif current_state == game_state.HOLD:
                current_state = game_state.SHOCK if self.hold_loop() else game_state.READY
            elif current_state == game_state.SHOCK:
                return True
            else:
                return False

            pygame.display.flip()