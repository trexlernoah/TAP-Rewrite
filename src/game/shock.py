import pygame

from constants import *
from utils import *
from drawer import Drawer


class ShockMeter:
    def __init__(self, drawer: Drawer, data: Data):
        self.drawer = drawer
        self.data = data

    def lose_loop(self, shock: int):
        self.drawer.render_text("YOU LOST! YOU GET A SHOCK", delay=2400)
        if shock >= 10 or shock <= 0:
            shock = 10
        key = 48 + shock
        self.drawer.draw_meter(key)
        # TODO send shock here
        self.drawer.render_text("", delay=1000)
        self.drawer.reset_meter(key)
        return True

    def win_loop(self):
        self.drawer.render_text("YOU WON! YOU GET TO GIVE A SHOCK")

        timer_start = pygame.time.get_ticks()
        time_held = 0
        key_pressed = None

        data_row = self.data.current_data_row
        error_flag1 = False
        error_flag2 = False

        while True:
            current_time = pygame.time.get_ticks()

            if (
                current_time >= timer_start + 4000
                and time_held == 0
                and not error_flag1
            ):
                error_flag1 = True
                self.drawer.render_text("YOU MUST PRESS A SHOCK BUTTON")
                self.data.current_error.add_error(ErrorMessage.WAIT_TO_SHOCK)

            for event in pygame.event.get():
                if (
                    event.type == pygame.KEYDOWN
                    and event.key in range(48, 58)
                    and not key_pressed
                ):  # start
                    key_pressed = str(event.unicode)
                    data_row.shock_intensity = (
                        "10" if key_pressed == "0" else key_pressed
                    )
                    if time_held == 0:
                        self.drawer.render_text("")
                        self.drawer.draw_meter(event.key)
                        time_held = current_time
                elif (
                    event.type == pygame.TEXTINPUT and event.text == key_pressed
                ):  # hold
                    if current_time > time_held + 7000 and not error_flag2:
                        error_flag2 = True
                        self.drawer.render_text(
                            "YOU ARE DONE SHOCKING! PLEASE RELEASE SHOCK BUTTON"
                        )
                        self.data.current_error.add_error(ErrorMessage.SHOCK_TOO_LONG)
                elif event.type == pygame.KEYUP and event.unicode == key_pressed:  # end
                    if current_time > timer_start:
                        time_held = current_time - time_held
                        self.drawer.reset_meter(event.key)
                        data_row.shock_duration = str(time_held)
                        self.drawer.render_text("YOU ARE DONE SHOCKING!", delay=5000)
                        return True

            pygame.display.flip()
