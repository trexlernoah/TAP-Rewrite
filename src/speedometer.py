import pygame, math, sys, time
from pygame import gfxdraw

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
    display.fill(WHITE)

    for i in range(1, 11):
        # Draw circles
        offset = -275 + i * 50
        x = int(center_x + offset)
        y = int((center_y - 60) + (center_y / 2))
        # gfxdraw.aacircle(display, x, y, RADIUS, BLACK)
        pygame.draw.circle(display, BLACK, (x, y), RADIUS, 3)
        
        # Draw text
        offset = -280 + i * 50
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

def arcDraw(x, y, r, n):
    for i in range (0, n):
        x2 = math.cos(math.radians())
        gfxdraw.filled_trigon(display, x, y,)

def key_press(_key):
    key = _key - 48
    print("Key %d has been pressed" % key)
    if key == 0:
        key = 10
    offset = -275 + key * 50
    x = int(center_x + offset)
    y = int((center_y - 60) + (center_y / 2))
    pygame.draw.circle(display, RED, (x, y), RADIUS, 39)
    # gfxdraw.filled_circle(display, x, y, RADIUS, RED)
    rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * key)))
    pygame.draw.arc(display, RED, rect, startRad, endRad, 95)
    # for i in range(0, 96):
        # gfxdraw.arc(display, center_x, center_y - 250, i, 180, 270, RED)
    # x = center_x
    # y = center_y - 250
    # n = math.sin(math.radians(18)) * 90
    # gfxdraw.filled_trigon(display, x, y, x-90, y, x-90, y-int(n), RED)
    pygame.display.update()
    time.sleep(1)
    pygame.draw.circle(display, WHITE, (center_x + offset, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.arc(display, WHITE, rect, startRad, endRad, 95)
    drawCircles()
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