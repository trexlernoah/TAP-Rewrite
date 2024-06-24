import pygame, math, random

from constants import *
from utils import *

class shock_meter_mngr():
    '''Shock meter drawing'''
    def __init__(self, display: pygame.Surface, subsurf: pygame.Surface, data: Data):
        self.display = display
        self.subsurf = subsurf

        window = display.get_rect()
        self.center_x = window.centerx
        self.center_y = window.centery

        self.font = pygame.font.SysFont(None, 30)    

        self.data = data    

    def clockwise_arc(self, point, radius, startAngle, endAngle):
        rect = pygame.Rect(0, 0, radius*2, radius*2)
        rect.center = point

        endRad   = math.radians(-startAngle)
        startRad = math.radians(-endAngle)

        return rect, startRad, endRad

    def draw_circles(self):
        self.display.fill(WHITE)

        for i in range(1, 11):
            # Draw circles
            offset = -275 + i * 50
            x = int(self.center_x + offset)
            y = int((self.center_y - 60) + (self.center_y / 2))
            pygame.draw.circle(self.display, BLACK, (x, y), RADIUS, 3)
            
            # Draw text
            offset = -280 + i * 50
            x = self.center_x + offset
            y = (self.center_y - 30) + (self.center_y / 2)
            text = self.font.render(str(i), 1, BLACK)
            self.display.blit(text, (x, y))

        low_text = self.font.render("Low", 1, BLACK)
        self.display.blit(low_text, (self.center_x - 230, (self.center_y + 10) + (self.center_y / 2)))

        high_text = self.font.render("High", 1, BLACK)
        self.display.blit(high_text, (self.center_x + 220, (self.center_y + 10) + (self.center_y / 2)))

        # Initialize arc
        pygame.draw.circle(self.display, BLACK, (self.center_x, self.center_y - 250), 100, width=5, draw_top_left=True, draw_top_right=True)
        pygame.draw.line(self.display, BLACK, (self.center_x - 100, self.center_y - 250), (self.center_x + 100, self.center_y - 250), 5)

    def draw_meter(self, _key):
        key = _key - 48
        if key == 0:
            key = 10
            
        offset = -275 + key * 50
        
        x = int(self.center_x + offset)
        y = int((self.center_y - 60) + (self.center_y / 2))
        pygame.draw.circle(self.display, RED, (x, y), RADIUS, 39)
        rect, startRad, endRad = self.clockwise_arc((self.center_x, self.center_y - 250), 95, 180, (180+(180/10 * key)))
        pygame.draw.arc(self.display, RED, rect, startRad, endRad, 95)
        pygame.display.flip()
        
    def erase_meter(self, _key):
        key = _key - 48
        if key == 0:
            key = 10
            
        offset = 275
        rect, startRad, endRad = self.clockwise_arc((self.center_x, self.center_y - 250), 95, 180, (180+(180/10 * key)))
        pygame.draw.circle(self.display, WHITE, (self.center_x + offset, (self.center_y - 60) + (self.center_y / 2)), RADIUS, 39)
        pygame.draw.arc(self.display, WHITE, rect, startRad, endRad, 95)
        self.draw_circles()
        pygame.display.flip()

    def render(self, text, surface: pygame.Surface, color=FG, delay = 0):
        surface.fill(BG)
        text_block = self.font.render(text, 1, color)
        surface.blit(text_block, text_block.get_rect(center = surface.get_rect().center))
        pygame.display.flip()
        pygame.time.wait(delay)

    # Bad
    def loser_loop(self, shock: int):
        self.render("YOU LOST! YOU GET A SHOCK", self.subsurf, delay=2400)
        # wat happens here
        # key = random.randint(48,57)
        if shock >= 10 or shock <= 0: shock = 10
        key = 48 + shock
        self.draw_meter(key)
        pygame.display.flip()
        # send shock
        self.render("", self.subsurf, delay=1000)
        pygame.display.flip()
        self.erase_meter(key)
        pygame.display.flip()
        return True

    def shock_loop(self):
        self.render("YOU WON! YOU GET TO GIVE A SHOCK", self.subsurf)

        timer_start = pygame.time.get_ticks()
        time_held = 0
        key_pressed = None

        data_row = self.data.current_data_row
        error_flag1 = False
        error_flag2 = False

        while True:
            current_time = pygame.time.get_ticks()
            

            if current_time >= timer_start + 4000 and time_held == 0 and not error_flag1:
                error_flag1 = True
                self.render("YOU MUST PRESS A SHOCK BUTTON", self.subsurf)
                self.data.current_error.add_error(ErrorMessage.WAIT_TO_SHOCK)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key in range(48, 58) and not key_pressed: # start
                    key_pressed = str(event.unicode)
                    print("Shock: %s" % ("10" if key_pressed == "0" else key_pressed))
                    data_row.shock_intensity = ("10" if key_pressed == "0" else key_pressed)
                    if time_held == 0:
                        self.render("", self.subsurf)
                        self.draw_meter(event.key)
                        time_held = current_time
                elif event.type == pygame.TEXTINPUT and event.text == key_pressed: # hold
                    if current_time > time_held + 7000 and not error_flag2:
                        error_flag2 = True
                        self.render("YOU ARE DONE SHOCKING! PLEASE RELEASE SHOCK BUTTON", self.subsurf)
                        self.data.current_error.add_error(ErrorMessage.SHOCK_TOO_LONG)
                elif event.type == pygame.KEYUP and event.unicode == key_pressed: # end
                    if current_time > timer_start:
                        time_held = current_time - time_held
                        self.erase_meter(event.key)
                        print("Duration: %d ms" % (time_held))
                        data_row.shock_duration = str(time_held)
                        self.render("YOU ARE DONE SHOCKING!", self.subsurf, delay=5000)
                        return True
            pygame.display.flip()