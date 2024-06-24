import pygame, random

from constants import *
from utils import *

class reaction_test_mngr():
    '''Reaction test drawing'''
    def __init__(self, display: pygame.Surface, data: Data):
        self.display = display
        self.font = pygame.font.SysFont(None, 30)

        self.data = data

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
        error_flag = False

        while True:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - timer_start
            
            if delta_time >= 3000 and not error_flag:
                error_flag = True
                self.render("PLEASE PRESS THE SPACEBAR", FG)
                self.data.current_error.add_error(ErrorMessage.WAIT_TO_START)
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
                        self.data.current_error.add_error(ErrorMessage.WAIT_TOO_LONG)
                        return False
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    if current_time < timer_release:
                        self.render("YOU RELEASED TOO SOON", FG, 3700)
                        self.data.current_error.add_error(ErrorMessage.RELEASE_TOO_SOON)
                        return False
                    else:
                        reaction_time = current_time - timer_release
                        print("ReactionTime: %d ms" % (reaction_time))
                        self.data.current_data_row.reaction_time = str(reaction_time)
                        return True
            pygame.display.flip()


    def run(self, first_trial: bool):
        # Change this
        # Only show "Press spacebar to start" on first iteration
        current_state = GameState.START if first_trial else GameState.READY

        while True:
            if current_state == GameState.START:
                current_state = GameState.READY if self.start_loop() else GameState.START
            elif current_state == GameState.READY:
                current_state = GameState.HOLD if self.ready_loop() else GameState.READY
            elif current_state == GameState.HOLD:
                current_state = GameState.SHOCK if self.hold_loop() else GameState.READY
            elif current_state == GameState.SHOCK:
                return True
            else:
                return False

            pygame.display.flip()