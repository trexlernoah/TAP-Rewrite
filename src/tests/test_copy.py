# Swiped from https://stackoverflow.com/a/66033644
import pygame
import random
pygame.init()

black = (0,0,0)
white = (255,255,255)

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Reaction Time Test")

font = pygame.font.SysFont(None, 30)
text = font.render("PRESS ANY KEY TO START TEST", 0, black)
w = font.render("PRESS ANY KEY",0,black)
r_surf = None

start_time = 0
status = "wait"

running = True
while running:
    current_time = pygame.time.get_ticks()    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if status == "start":
                    status = "wait"
                    # I'm not sure what the timing is for the key release,
                    # this is just a guess of a time between 1 and 4 seconds
                    start_time = current_time + random.randint(1000, 4000)

                if status == "wait_for_reaction":
                    status = "wait"
                    reaction_time = (current_time - start_time) / 1000
                    start_time = current_time + random.randint(1000, 4000)
                    r_surf = font.render(f"REACTION TIME: {reaction_time:.03f}",0,black)

    if status == "wait":
        if current_time >= start_time:
            status = "wait_for_reaction"

    display.fill(white)

    center = display.get_rect().center
    if status == "start":
        display.blit(text, text.get_rect(center = center))
    if status == "wait_for_reaction":
        display.blit(w, w.get_rect(center = center))
    if r_surf:
        display.blit(r_surf, r_surf.get_rect(center = (center[0], 350)))

    pygame.display.flip()