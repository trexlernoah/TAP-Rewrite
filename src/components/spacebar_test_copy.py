# Swiped from https://stackoverflow.com/a/66033644
from enum import Enum
import pygame
import random
pygame.init()

display = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Reaction Time Test")

font = pygame.font.SysFont(None, 30)

text = font.render("PRESS ANY KEY TO START TEST", 0, (255,255,255))
w = font.render("PRESS ANY KEY",0,(0,255,0))
r_surf = None
ar_surf = None

# game_state = "start"

running = True
# while running:
#     current_time = pygame.time.get_ticks()
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             pygame.quit()
#         if event.type == pygame.KEYDOWN:
#             if game_state == "start":
#                 game_state = "wait" 
#                 start_time = current_time + random.randint(1000, 4000)
#             if game_state == "wait_for_reaction": 
#                 game_state = "wait" 
#                 reaction_time = (current_time - start_time) / 1000
#                 start_time = current_time + random.randint(1000, 4000)
#                 r_surf = font.render(f"REACTION TIME: {reaction_time:.03f}",0,(255,255,255))

#     if game_state == "wait":
#         if current_time >= start_time:
#             game_state = "wait_for_reaction"        

#     display.fill(pygame.Color("black"))
    
#     center = display.get_rect().center
#     if game_state == "start":
#         display.blit(text, text.get_rect(center = center))
#     if game_state == "wait_for_reaction":
#         display.blit(w, w.get_rect(center = center))
#     if r_surf:
#         display.blit(r_surf, r_surf.get_rect(center = (center[0], 350)))
#     if ar_surf:
#         display.blit(ar_surf, ar_surf.get_rect(center = (center[0], 400)))

#     pygame.display.flip()

class game_state(Enum):
    START = 1
    READY = 2
    HOLD = 3
    SHOCK = 4

def start_loop():

    display.blit(font.render("PRESS SPACEBAR TO START TEST", 0, (255,255,255)),
                        text.get_rect(center = display.get_rect().center))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("spacebar press")
                display.fill(pygame.Color("black"))
                pygame.display.flip()
                print("waiting")
                # pygame.time.wait(7650)
                print("done waiting")
                running = False
                break
        pygame.display.flip()

def ready_loop():

    display.blit(font.render("GET READY!", 0, (255,255,255)),
                         text.get_rect(center = display.get_rect().center))
    pygame.display.flip()
    pygame.time.wait(3700)
    display.fill(pygame.Color("black"))
    display.blit(font.render("PRESS SPACEBAR", 0, (255,255,255)),
                         text.get_rect(center = display.get_rect().center))
    pygame.display.flip()
    timer_start = pygame.time.get_ticks()
    print(timer_start)
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - timer_start
        if time_elapsed >= 3700:
                display.fill(pygame.Color("black"))
                display.blit(font.render("PLEASE PRESS THE SPACEBAR", 0, (255,255,255)),
                             text.get_rect(center = display.get_rect().center))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print('starting')
                running = False
                break
        pygame.display.flip()

def hold_loop():
    display.fill(pygame.Color("black"))
    display.blit(font.render("PRESS SPACEBAR", 0, (255,255,255)),
                         text.get_rect(center = display.get_rect().center))
    pygame.display.flip()

    timer_start = pygame.time.get_ticks()
    timer_release = timer_start + random.randint(2000, 4000)
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - timer_start
        if current_time >= timer_release:
            display.fill(pygame.Color("black"))
            display.blit(font.render("RELEASE", 0, (255,0,0)),
                         text.get_rect(center = display.get_rect().center))

        for event in pygame.event.get():
            if event.type == pygame.TEXTINPUT and event.text == ' ':
                print('holding')
                if current_time > timer_release + 5000:
                    display.fill(pygame.Color("black"))
                    display.blit(font.render("YOU WAITED TOO LONG", 0, (255,255,255)),
                                 text.get_rect(center = display.get_rect().center))
                    pygame.display.flip()
                    pygame.time.wait(3700)
                    # return go to get ready
                    running = False
                    break
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                print('released')
                if current_time < timer_release:
                    display.fill(pygame.Color("black"))
                    display.blit(font.render("YOU RELEASED TOO SOON", 0, (255,255,255)),
                                 text.get_rect(center = display.get_rect().center))
                    pygame.display.flip()
                    pygame.time.wait(3700)
                    # return go to get ready
                    running = False
                    break
                else:
                    display.fill(pygame.Color("black"))
                    display.blit(font.render("YOU WIN, YOU GET TO GIVE A SHOCK", 0, (255,255,255)),
                                 text.get_rect(center = display.get_rect().center))
                    pygame.display.flip()
                    pygame.time.wait(3700)
                    # return go to get ready
                    running = False
                    break
            else:
                print(event)
                print(current_time)
        pygame.display.flip()


def run():
    center = display.get_rect().center
    current_state = game_state.START

    while True:
        if current_state == game_state.START:
            start_loop()
            current_state = game_state.READY
        elif current_state == game_state.READY:
            ready_loop()
            current_state = game_state.HOLD
        elif current_state == game_state.HOLD:
            hold_loop()
            break

        
        display.fill(pygame.Color("black"))
        pygame.display.flip()

    # elif current_state == game_state.READY:

run()