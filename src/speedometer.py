import pygame
import math
import sys
pygame.init()
size = width, height = 500, 500
display = pygame.display.set_mode(size)
font = pygame.font.SysFont(None, 30)
RADIUS = 20
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (225, 225, 225) 
display.fill(GRAY)
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
    display.fill((225, 225, 225))
    # Initialize circles
    pygame.draw.circle(display, WHITE, (center_x - 225, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.circle(display, WHITE, (center_x - 175, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.circle(display, WHITE, (center_x - 125, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.circle(display, WHITE, (center_x - 75, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.circle(display, WHITE, (center_x - 25, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.circle(display, WHITE, (center_x + 25, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.circle(display, WHITE, (center_x + 75, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.circle(display, WHITE, (center_x + 125, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.circle(display, WHITE, (center_x + 175, (center_y - 60) + (center_y / 2)), RADIUS, 39)
    pygame.draw.circle(display, WHITE, (center_x + 225, (center_y - 60) + (center_y / 2)), RADIUS, 39)

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

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    display.fill((255,255,255))
    
    # This works for now
    pygame.draw.circle(display,(0, 0, 0), (250, 250), 100, width=5, draw_top_left=True, draw_top_right=True)
    rect, startRad, endRad = clockwiseArc((center_x, center_y - 250), 95, 180, (180+(180/10 * 1)))
    pygame.draw.arc(display, RED, rect, startRad, endRad, 95)
    drawCircles()
    pygame.display.flip()