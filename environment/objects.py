import pygame


class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)

class Resource:
    def __init__(self, x, y, radius=12):
        self.x = x
        self.y = y
        self.radius = radius
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(
                screen,
                (50, 220, 100),
                (self.x, self.y),
                self.radius
            )

class Exit:
    def __init__(self, x, y, width=40, height=50):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (230, 200, 50), self.rect)