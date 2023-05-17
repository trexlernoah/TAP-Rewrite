# Swiped from https://stackoverflow.com/a/66033644
import pygame
import time 
pygame.init()

screen_width = 640
screen_height = 480

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Reaction Time Test")
font = pygame.font.SysFont(None, 30)

timer_started = False
release_time = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN and not timer_started and event.key == pygame.K_SPACE:
            start_text = font.render("Press and hold down the space key", True, (0, 0, 0))
            start_text_rect = start_text.get_rect(center = (screen_width//2, screen_height//2))
            display.blit(start_text, start_text_rect)
            pygame.display.flip()

            pygame.time.wait(2000)
            start_time = time.time()
            timer_started = True

        elif event.type == pygame.KEYUP and timer_started and release_time == 0:
            release_time = time.time()

    if timer_started and release_time == 0 and time.time() - start_time >= 2:
        prompt_text = font.render("Release the space key now!", True, (255, 0, 0))
        prompt_text_rect = prompt_text.get_rect(center = (screen_width//2, screen_height//2))
        display.blit(prompt_text, prompt_text_rect)
        pygame.display.flip()

    if release_time != 0.000:
        elapsed_time = release_time - start_time
        result_text = font.render(f"Elapsed Time: {elapsed_time:.3f} seconds", True, (0, 0, 0))
        result_text_rect = result_text.get_rect(center=(screen_width//2, screen_height//2))
        display.blit(result_text, result_text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        timer_started = False
        release_time = 0
        prompt_text = font.render("Press space key to start timer", True, (0, 0, 0))
        prompt_text_rect = prompt_text.get_rect(center=(screen_width//2, screen_height//2))
        display.blit(prompt_text, prompt_text_rect)
        pygame.display.flip()

    display.fill((255,255,255))
    pygame.display.update()