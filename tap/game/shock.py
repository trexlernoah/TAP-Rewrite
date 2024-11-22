import pygame


from tap.game.drawer import Drawer
from tap.classes import ErrorMessage, Data, Settings, ThreadHandler, ShockTask


class ShockMeter:
    def __init__(
        self,
        thread_handler: ThreadHandler,
        settings: Settings,
        drawer: Drawer,
        data: Data,
    ):
        self.thread_handler = thread_handler
        self.settings = settings
        self.drawer = drawer
        self.data = data

    def generate_shock(self, shock: int, feedback: int):
        if shock >= 10 or shock <= 0:
            shock = 10

        # TODO move this somewhere else?
        intensity = self.settings.intensities[shock - 1]
        lower_threshold = self.settings.lower_threshold / 1000
        higher_threshold = self.settings.higher_threshold / 1000
        m = (higher_threshold - lower_threshold) / 10
        print(f"{lower_threshold} - {higher_threshold} -> {m}")
        print(f"intensity {intensity}")
        shock_mA = ((m * shock) + lower_threshold) * (intensity / 100)
        print(shock_mA)

        self.thread_handler.task_queue.put(ShockTask(shock_mA, feedback, 1))

    def lose_loop(self, shock: int, feedback: int):
        self.drawer.render_text("YOU LOST! YOU GET A SHOCK", delay=2400)
        if shock >= 10 or shock <= 0:
            shock = 10
        key = 48 + shock
        self.drawer.draw_meter(key)
        # TODO send shock here
        self.generate_shock(shock, feedback)
        self.drawer.render_text("", delay=feedback * 1000)
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
                self.data.add_error(ErrorMessage.WAIT_TO_SHOCK)

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
                        self.data.add_error(ErrorMessage.SHOCK_TOO_LONG)
                elif event.type == pygame.KEYUP and event.unicode == key_pressed:  # end
                    if current_time > timer_start:
                        time_held = current_time - time_held
                        self.drawer.reset_meter(event.key)
                        data_row.shock_duration = str(time_held)
                        self.drawer.render_text("YOU ARE DONE SHOCKING!", delay=5000)
                        return True

            pygame.display.flip()
