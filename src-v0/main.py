'''
Notes:
- Move utilities + reaction tests to other files and import
'''

import pygame, math, random, sys, time

pygame.init()
clock = pygame.time.Clock()

RADIUS = 20
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (225, 225, 225)

running = True

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display.fill(GRAY)
window = display.get_rect()
center_x = window.centerx
center_y = window.centery

pygame.display.update()

font = pygame.font.SysFont(None, 30)

# Utility Functions

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
    pygame.draw.arc(display, WHITE, rect, startRad, endRad, 95)
    pygame.display.update()

def print_to_screen(text):
    
    text_render = font.render(text, True, BLACK)
    text_rect = text_render.get_rect(center = (center_x, center_y))
    display.blit(text_render, text_rect)
    pygame.display.flip()

# Reaction Test
def reaction_test():
    timer_start = time.time()
    print(timer_start)
    running = True
    while running:
        clock.tick(60)
        display.fill(GRAY)
        for event in pygame.event.get():
            timer_since = time.time() - timer_start

            if timer_since < 3.7:
                print_to_screen("GET READY!")
            else:
                print_to_screen("PRESS SPACEBAR")
                print(event)

        pygame.display.flip()
        

def old_reaction_test():
        timer_started = False
        release_time = 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif not timer_started:
                    text = font.render("Press and hold down the space key", True, BLACK)
                    text_rect = text.get_rect(center = (center_x, center_y))
                    display.blit(text, text_rect)
                    pygame.display.flip()

                    pygame.time.wait(2000)
                    start_time = time.time()
                    timer_started = True

                elif event.type == pygame.KEYUP and timer_started and release_time == 0:
                    release_time = time.time()

            if timer_started and release_time == 0 and time.time() - start_time >= 2:
                text = font.render("Release the space key now!", True, RED)
                display.blit(text, text_rect)
                pygame.display.flip()

            if release_time != 0:
                elapsed_time = release_time - start_time
                text = font.render(f"Elapsed Time: {elapsed_time:.3f} seconds", True, BLACK)

                text_rect = text.get_rect(center=(center_x, center_y))
                display.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(2000)
                timer_started = False
                release_time = 0
                text = font.render("Press space key to start timer", True, BLACK)
                display.blit(text, text_rect)
                running = False

            display.fill(WHITE)
            pygame.display.update()

# Shock Selection
def shock_selection():
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
                        running = False
            pygame.display.update() 
            pygame.display.flip()


def main():

    # Main loop
    while running:
        reaction_test()
        shock_selection()

        
if __name__ == "__main__":
    main()
