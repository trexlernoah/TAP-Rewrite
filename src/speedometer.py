import pygame, math, sys, time
from pygame import gfxdraw

pygame.init()

# display = pygame.display.set_mode(1000, 800)

font = pygame.font.SysFont(None, 30)

RADIUS = 20
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (225, 225, 225) 

class shock_meter_mngr():
    '''Shock meter drawing'''
    def __init__(self, display: pygame.Surface):
        self.display = display

        window = display.get_rect()
        self.center_x = window.centerx
        self.center_y = window.centery
    

    def clockwiseArc(self, point, radius, startAngle, endAngle):
        rect = pygame.Rect(0, 0, radius*2, radius*2)
        rect.center = point

        endRad   = math.radians(-startAngle)
        startRad = math.radians(-endAngle)

        return rect, startRad, endRad

    def drawCircles(self):
        self.display.fill(WHITE)

        for i in range(1, 11):
            # Draw circles
            offset = -275 + i * 50
            x = int(self.center_x + offset)
            y = int((self.center_y - 60) + (self.center_y / 2))
            # gfxdraw.aacircle(self.display, x, y, RADIUS, BLACK)
            pygame.draw.circle(self.display, BLACK, (x, y), RADIUS, 3)
            
            # Draw text
            offset = -280 + i * 50
            x = self.center_x + offset
            y = (self.center_y - 30) + (self.center_y / 2)
            text = font.render(str(i), 1, BLACK)
            self.display.blit(text, (x, y))

        low_text = font.render("Low", 1, BLACK)
        self.display.blit(low_text, (self.center_x - 230, (self.center_y + 10) + (self.center_y / 2)))

        high_text = font.render("High", 1, BLACK)
        self.display.blit(high_text, (self.center_x + 220, (self.center_y + 10) + (self.center_y / 2)))

        # Initialize arc
        pygame.draw.circle(self.display, BLACK, (self.center_x, self.center_y - 250), 100, width=5, draw_top_left=True, draw_top_right=True)

    def arcDraw(self, x, y, r, n):
        for i in range (0, n):
            x2 = math.cos(math.radians())
            gfxdraw.filled_trigon(self.display, x, y,)

    def key_press(self, _key):
        key = _key - 48
        print("Key %d has been pressed" % key)
        if key == 0:
            key = 10
        offset = -275 + key * 50
        x = int(self.center_x + offset)
        y = int((self.center_y - 60) + (self.center_y / 2))
        pygame.draw.circle(self.display, RED, (x, y), RADIUS, 39)
        # gfxdraw.filled_circle(self.display, x, y, RADIUS, RED)
        rect, startRad, endRad = self.clockwiseArc((self.center_x, self.center_y - 250), 95, 180, (180+(180/10 * key)))
        pygame.draw.arc(self.display, RED, rect, startRad, endRad, 95)

        pygame.display.update()
        time.sleep(1)
        pygame.draw.circle(self.display, WHITE, (self.center_x + offset, (self.center_y - 60) + (self.center_y / 2)), RADIUS, 39)
        pygame.draw.arc(self.display, WHITE, rect, startRad, endRad, 95)
        self.drawCircles()
        pygame.display.update()

    def shock(self):
        while True:
            for event in pygame.event.get():
                if event.key not in range(48, 58):
                    print("Please press a key from 0-9 on the keyboard")
                else:
                    self.key_press(event.key)
                    return True

# running = True
# drawCircles()
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 pygame.quit()
#                 sys.exit()
#             elif event.key not in range(48, 58):
#                 print("Please press a key from 0-9 on the keyboard")
#             else:
#                 key_press(event.key)
#                 # running = False
#     pygame.display.update() 
#     pygame.display.flip()