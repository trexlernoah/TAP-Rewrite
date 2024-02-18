import pygame
import math
import sys
import time

pygame.init()
size = width, height = 1000, 800
# display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display = pygame.display.set_mode(size)
font = pygame.font.SysFont(None, 30)

RADIUS = 20
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (225, 225, 225) 

display.fill(WHITE)
window = display.get_rect()
center_x = window.centerx
center_y = window.centery

def clockwiseArc(point, radius, startAngle, endAngle):
    rect = pygame.Rect(0, 0, radius*2, radius*2)
    rect.center = point

    endRad   = math.radians(-startAngle)
    startRad = math.radians(-endAngle)

    return rect, startRad, endRad

def drawCircles():
    display.fill(GRAY)

    for i in range(1, 11):
        # Draw circles
        offset = -275 + i * 50
        x = center_x + offset
        y = (center_y - 60) + (center_y / 2)
        pygame.draw.circle(display, WHITE, (x, y), RADIUS, 39)
        
        # Draw text
        offset = -280 + i * 50
        print(offset)
        x = center_x + offset
        y = (center_y - 30) + (center_y / 2)
        text = font.render(str(i), 1, BLACK)
        display.blit(text, (x, y))

    low_text = font.render("Low", 1, BLACK)
    display.blit(low_text, (center_x - 230, (center_y + 10) + (center_y / 2)))

    high_text = font.render("High", 1, BLACK)
    display.blit(high_text, (center_x + 220, (center_y + 10) + (center_y / 2)))

    # Initialize arc
    pygame.draw.circle(display, BLACK, (center_x, center_y - 250), 100, width=5, draw_top_left=True, draw_top_right=True)

def key_press(_key):
    key = _key - 48
    print("Key %d has been pressed" % key)
    if key == 0:
        key = 10
    offset = -275 + key * 50
    pygame.draw.circle(display, RED, (center_x + offset, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * key)))
    pygame.draw.arc(display, RED, rect, startRad, endRad, 95)
    pygame.display.update()
    time.sleep(1)
    pygame.draw.circle(display, WHITE, (center_x + offset, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.arc(display, GRAY, rect, startRad, endRad, 95)
    pygame.display.update()

running = True
drawCircles()
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key not in range(48, 58):
                print("Please press a key from 0-9 on the keyboard")
            else:
                key_press(event.key)
                # running = False
    pygame.display.update() 
    pygame.display.flip()