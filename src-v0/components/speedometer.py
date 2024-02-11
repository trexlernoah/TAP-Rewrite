import pygame
import math
import sys
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

def clockwiseArc(surface, color, point, radius, startAngle, endAngle, fill):
    rect = pygame.Rect(0, 0, radius*2, radius*2)
    rect.center = point

    endRad   = math.radians(-startAngle)
    startRad = math.radians(-endAngle)

    pygame.draw.arc(surface, color, rect, startRad, endRad, fill)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((255,255,255))
    
    # This works for now
    pygame.draw.circle(screen,(0, 0, 0), (250, 250), 100, width=5, draw_top_left=True, draw_top_right=True)
    clockwiseArc(screen, (255, 0, 0), (250, 250), 95, 180, (180+(180/10 * 2)), 220) 
    pygame.display.flip()