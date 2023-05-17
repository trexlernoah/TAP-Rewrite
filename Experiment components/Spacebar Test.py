# Swiped from https://stackoverflow.com/a/66033644
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

game_state = "start"

running = True
while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if game_state == "start":
                game_state = "wait" 
                start_time = current_time + random.randint(1000, 4000)
            if game_state == "wait_for_reaction": 
                game_state = "wait" 
                reaction_time = (current_time - start_time) / 1000
                start_time = current_time + random.randint(1000, 4000)
                r_surf = font.render(f"REACTION TIME: {reaction_time:.03f}",0,(255,255,255))

    if game_state == "wait":
        if current_time >= start_time:
            game_state = "wait_for_reaction"        

    display.fill(pygame.Color("black"))
    
    center = display.get_rect().center
    if game_state == "start":
        display.blit(text, text.get_rect(center = center))
    if game_state == "wait_for_reaction":
        display.blit(w, w.get_rect(center = center))
    if r_surf:
        display.blit(r_surf, r_surf.get_rect(center = (center[0], 350)))
    if ar_surf:
        display.blit(ar_surf, ar_surf.get_rect(center = (center[0], 400)))

    pygame.display.flip()