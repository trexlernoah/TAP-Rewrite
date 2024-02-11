from enum import Enum
import pygame, random

pygame.init()

display = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Reaction Time Test")

font = pygame.font.SysFont(None, 30)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

BG = WHITE
FG = BLACK

class game_state(Enum):
    START = 1
    READY = 2
    HOLD = 3
    SHOCK = 4

def render(text, color, delay = 0):
    display.fill(BG)
    text_block = font.render(text, 1, color)
    display.blit(text_block, text_block.get_rect(center = display.get_rect().center))
    pygame.display.flip()
    pygame.time.wait(delay)

def start_loop():
    render("PRESS SPACEBAR TO START TEST", FG)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                render("", FG, 7650)
                return True

def ready_loop():
    render("GET READY!", FG, 3700)
    render("PRESS SPACEBAR", FG)

    timer_start = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - timer_start

        if delta_time >= 3700:
                render("PLEASE PRESS THE SPACEBAR", FG)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

def hold_loop():
    render("PRESS SPACEBAR", FG)

    timer_start = pygame.time.get_ticks()
    timer_release = timer_start + random.randint(2000, 4000)

    while True:
        current_time = pygame.time.get_ticks()

        if current_time >= timer_release:
            render("RELEASE", RED)

        for event in pygame.event.get():
            if event.type == pygame.TEXTINPUT and event.text == ' ':
                if current_time > timer_release + 5000:
                    render("YOU WAITED TOO LONG", FG, 3700)
                    return False
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if current_time < timer_release:
                    render("YOU RELEASED TOO SOON", FG, 3700)
                    return False
                else:
                    render("YOU WIN, YOU GET TO GIVE A SHOCK", FG, 3700)
                    return True
        pygame.display.flip()


def run():
    current_state = game_state.START

    while True:
        if current_state == game_state.START:
            current_state = game_state.READY if start_loop() else game_state.START
        elif current_state == game_state.READY:
            current_state = game_state.HOLD if ready_loop() else game_state.READY
        elif current_state == game_state.HOLD:
            current_state = game_state.SHOCK if hold_loop() else game_state.READY
        elif current_state == game_state.SHOCK:
            break
        else:
            break

        pygame.display.flip()

run()