import pygame

from environment.world import World


pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adaptive 2D AI Agent")

clock = pygame.time.Clock()

world = World(WIDTH, HEIGHT)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    world.update()

    screen.fill((30, 30, 30))

    world.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()