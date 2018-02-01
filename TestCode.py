import pygame
pygame.init()

screen_size = screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(screen_size)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

running = True

while running:
    for event in pygame.event.get():
        event.type == pygame.QUIT:
            running = False

    screen.fill(black)
    #screen.blit(surface)
    pygame.display.update()

pygame.quit()
exit()
