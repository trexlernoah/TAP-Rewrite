import math
import pygame
import random
import sys
import time
 
# initialising pygame
pygame.init()

# Colors
RADIUS = 20
black = (0, 0, 0)
red = (225, 0, 0)
white = (255, 255, 255)

# creating display
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display.fill((225, 225, 225))
window = display.get_rect()
center_x = window.centerx
center_y = window.centery
 
# Impot arc drawing function
def clockwiseArc(point, radius, startAngle, endAngle):
    rect = pygame.Rect(0, 0, radius*2, radius*2)
    rect.center = point

    endRad   = math.radians(-startAngle)
    startRad = math.radians(-endAngle)

    return rect, startRad, endRad


pygame.display.update()

font = pygame.font.SysFont(None, 30)

# Initialize circles
pygame.draw.circle(display, white, (center_x - 225, (center_y - 60) + (center_y / 2)), RADIUS, 39)
pygame.draw.circle(display, white, (center_x - 175, (center_y - 60) + (center_y / 2)), RADIUS, 39)
pygame.draw.circle(display, white, (center_x - 125, (center_y - 60) + (center_y / 2)), RADIUS, 39)
pygame.draw.circle(display, white, (center_x - 75, (center_y - 60) + (center_y / 2)), RADIUS, 39)
pygame.draw.circle(display, white, (center_x - 25, (center_y - 60) + (center_y / 2)), RADIUS, 39)
pygame.draw.circle(display, white, (center_x + 25, (center_y - 60) + (center_y / 2)), RADIUS, 39)
pygame.draw.circle(display, white, (center_x + 75, (center_y - 60) + (center_y / 2)), RADIUS, 39)
pygame.draw.circle(display, white, (center_x + 125, (center_y - 60) + (center_y / 2)), RADIUS, 39)
pygame.draw.circle(display, white, (center_x + 175, (center_y - 60) + (center_y / 2)), RADIUS, 39)
pygame.draw.circle(display, white, (center_x + 225, (center_y - 60) + (center_y / 2)), RADIUS, 39)

# Initialize circle text
low_text = font.render("Low", 0, (0,0,0))
display.blit(low_text, (center_x - 230, (center_y + 10) + (center_y / 2)))

high_text = font.render("High", 0, (0,0,0))
display.blit(high_text, (center_x + 230, (center_y + 10) + (center_y / 2)))

circle0 = font.render("1", 0, (0,0,0))
display.blit(circle0, (center_x - 230, (center_y - 30) + (center_y / 2)))

circle1 = font.render("2", 0, (0,0,0))
display.blit(circle1, (center_x - 170, (center_y - 30) + (center_y / 2)))

circle2 = font.render("3", 0, (0,0,0))
display.blit(circle2, (center_x - 120, (center_y - 30) + (center_y / 2)))

circle3 = font.render("4", 0, (0,0,0))
display.blit(circle3, (center_x - 70, (center_y - 30) + (center_y / 2)))

circle4 = font.render("5", 0, (0,0,0))
display.blit(circle4, (center_x - 20, (center_y - 30) + (center_y / 2)))

circle5 = font.render("6", 0, (0,0,0))
display.blit(circle5, (center_x + 20, (center_y - 30) + (center_y / 2)))

circle6 = font.render("7", 0, (0,0,0))
display.blit(circle6, (center_x + 70, (center_y - 30) + (center_y / 2)))

circle7 = font.render("8", 0, (0,0,0))
display.blit(circle7, (center_x + 120, (center_y - 30) + (center_y / 2)))

circle8 = font.render("9", 0, (0,0,0))
display.blit(circle8, (center_x + 170, (center_y - 30) + (center_y / 2)))

circle9 = font.render("10", 0, (0,0,0))
display.blit(circle9, (center_x + 220, (center_y - 30) + (center_y / 2)))

# Initialize arc
pygame.draw.circle(display,(0, 0, 0), (center_x, center_y - 250), 100, width=5, draw_top_left=True, draw_top_right=True)


class ShockState():
    def __init__(self):
        self.state = 'reaction_state'

    def reaction_test(self):
        timer_started = False
        release_time = 0
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN and not timer_started:
                text = font.render("Press and hold down the space key", True, black)
                text_rect = text.get_rect(center = (center_x, center_y))
                display.blit(text, text_rect)
                pygame.display.flip()

                pygame.time.wait(2000)
                start_time = time.time()
                timer_started = True

            elif event.type == pygame.KEYUP and timer_started and release_time == 0:
                release_time = time.time()

        if timer_started and release_time == 0 and time.time() - start_time >= 2:
            text = font.render("Release the space key now!", True, red)
            display.blit(text, text_rect)
            pygame.display.flip()

        if release_time != 0:
            elapsed_time = release_time - start_time
            text = font.render(f"Elapsed Time: {elapsed_time:.3f} seconds", True, black)

            text_rect = text.get_rect(center=(center_x, center_y))
            display.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            timer_started = False
            release_time = 0
            text = font.render("Press space key to start timer", True, black)
            display.blit(text, text_rect)

        display.fill(white)
        pygame.display.update()

    def shock_select(self):
        # checking if keydown event happened or not
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_1:
                        print("Key 1 has been pressed")
                        pygame.draw.circle(display, red, (center_x - 225, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 1)))
                        pygame.draw.arc(display, (255, 0, 0), rect, startRad, endRad, 95)
                        pygame.display.update()
                        time.sleep(1)
                        pygame.draw.circle(display, white, (center_x - 225, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        pygame.draw.arc(display, (255, 225, 225), rect, startRad, endRad, 95)
                        pygame.display.update()

                    case pygame.K_2:
                        print("Key 2 has been pressed")
                        pygame.draw.circle(display, red, (center_x - 175, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 2)))
                        pygame.draw.arc(display, (255, 0, 0), rect, startRad, endRad, 95)
                        pygame.display.update()
                        time.sleep(1)
                        pygame.draw.circle(display, white, (center_x - 175, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        pygame.draw.arc(display, (255, 225, 225), rect, startRad, endRad, 95)
                        pygame.display.update()

                    case pygame.K_3:
                        print("Key 3 has been pressed")
                        pygame.draw.circle(display, red, (center_x - 125, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 3)))
                        pygame.draw.arc(display, (255, 0, 0), rect, startRad, endRad, 95)
                        pygame.display.update()
                        time.sleep(1)
                        pygame.draw.circle(display, white, (center_x - 125, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        pygame.draw.arc(display, (255, 225, 225), rect, startRad, endRad, 95)
                        pygame.display.update()

                    case pygame.K_4:
                        print("Key 4 has been pressed")
                        pygame.draw.circle(display, red, (center_x - 75, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 4)))
                        pygame.draw.arc(display, (255, 0, 0), rect, startRad, endRad, 95)
                        pygame.display.update()
                        time.sleep(1)
                        pygame.draw.circle(display, white, (center_x - 75, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        pygame.draw.arc(display, (255, 225, 225), rect, startRad, endRad, 95)
                        pygame.display.update()

                    case pygame.K_5:
                        print("Key 5 has been pressed")
                        pygame.draw.circle(display, red, (center_x - 25, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 5)))
                        pygame.draw.arc(display, (255, 0, 0), rect, startRad, endRad, 95)
                        pygame.display.update()
                        time.sleep(1)
                        pygame.draw.circle(display, white, (center_x - 25, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        pygame.draw.arc(display, (255, 225, 225), rect, startRad, endRad, 95)
                        pygame.display.update()

                    case pygame.K_6:
                        print("Key 6 has been pressed")
                        pygame.draw.circle(display, red, (center_x + 25, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 6)))
                        pygame.draw.arc(display, (255, 0, 0), rect, startRad, endRad, 95)
                        pygame.display.update()
                        time.sleep(1)
                        pygame.draw.circle(display, white, (center_x + 25, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        pygame.draw.arc(display, (255, 225, 225), rect, startRad, endRad, 95)
                        pygame.display.update()

                    case pygame.K_7:
                        print("Key 7 has been pressed")
                        pygame.draw.circle(display, red, (center_x + 75, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 7)))
                        pygame.draw.arc(display, (255, 0, 0), rect, startRad, endRad, 95)
                        pygame.display.update()
                        time.sleep(1)
                        pygame.draw.circle(display, white, (center_x + 75, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        pygame.draw.arc(display, (255, 225, 225), rect, startRad, endRad, 95)
                        pygame.display.update()

                    case pygame.K_8:
                        print("Key 8 has been pressed")
                        pygame.draw.circle(display, red, (center_x + 125, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 8)))
                        pygame.draw.arc(display, (255, 0, 0), rect, startRad, endRad, 95)
                        pygame.display.update()
                        time.sleep(1)
                        pygame.draw.circle(display, white, (center_x + 125, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        pygame.draw.arc(display, (255, 225, 225), rect, startRad, endRad, 95)
                        pygame.display.update()

                    case pygame.K_9:
                        print("Key 9 has been pressed")
                        pygame.draw.circle(display, red, (center_x + 175, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 9)))
                        pygame.draw.arc(display, (255, 0, 0), rect, startRad, endRad, 95)
                        pygame.display.update()
                        time.sleep(1)
                        pygame.draw.circle(display, white, (center_x + 175, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        pygame.draw.arc(display, (255, 225, 225), rect, startRad, endRad, 95)
                        pygame.display.update()

                    case pygame.K_0:
                        print("Key 0 has been pressed")
                        pygame.draw.circle(display, red, (center_x + 225, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 10)))
                        pygame.draw.arc(display, (255, 0, 0), rect, startRad, endRad, 95)
                        pygame.display.update()
                        time.sleep(1)
                        pygame.draw.circle(display, white, (center_x + 225, (center_y - 60) + (center_y / 2)), RADIUS, 39)
                        pygame.draw.arc(display, (255, 225, 225), rect, startRad, endRad, 95)
                        pygame.display.update()

                    case pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    case _:
                        print("Please press a key from 0-9 on the keyboard")

        pygame.display.update() 
        pygame.display.flip() 

    def state_manager(self):
        if self.state == 'reaction_state':
           self.reaction_test()
            
        elif self.state == 'shock_select':
            self.shock_select()
    
state = ShockState()

while True:
   state.shock_select() 
  
pygame.quit()