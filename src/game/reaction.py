import pygame, random

from constants import *
from utils import *
from drawer import Drawer

class ReactionTest():
    def __init__(self, drawer: Drawer, data: Data):
        self.drawer = drawer
        self.data = data

    def start_loop(self):
        self.drawer.render_text("PRESS SPACEBAR TO START")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.drawer.render_text("", 7650)
                    return True

    def ready_loop(self):
        self.drawer.render_text("GET READY!", 3700)
        self.drawer.render_text("PRESS SPACEBAR")

        timer_start = pygame.time.get_ticks()
        error_flag = False

        while True:
            current_time = pygame.time.get_ticks()
            delta_time = current_time - timer_start
            
            if delta_time >= 3000 and not error_flag:
                error_flag = True
                self.drawer.render_text("PLEASE PRESS THE SPACEBAR")
                self.data.current_error.add_error(ErrorMessage.WAIT_TO_START)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return True

    def hold_loop(self):
        timer_start = pygame.time.get_ticks()
        timer_release = timer_start + random.randint(2000, 4000)

        while True:
            current_time = pygame.time.get_ticks()

            if current_time >= timer_release:
                self.drawer.render_text("RELEASE", RED)

            for event in pygame.event.get():
                if event.type == pygame.TEXTINPUT and event.text == ' ':
                    if current_time > timer_release + 1000:
                        self.drawer.render_text("YOU WAITED TOO LONG", 3700)
                        self.data.current_error.add_error(ErrorMessage.WAIT_TOO_LONG)
                        return False
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    if current_time < timer_release:
                        self.drawer.render_text("YOU RELEASED TOO SOON", 3700)
                        self.data.current_error.add_error(ErrorMessage.RELEASE_TOO_SOON)
                        return False
                    else:
                        self.drawer.render_text("", FG, 1000)
                        reaction_time = current_time - timer_release
                        self.data.current_data_row.reaction_time = str(reaction_time)
                        return True
            pygame.display.flip()


    def run(self, first_trial: bool):
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