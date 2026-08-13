import pygame


class Agent:
    def __init__(self, x, y, size=30):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 5

    @property
    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        if keys[pygame.K_UP]:
            self.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (50, 150, 255),
            self.rect
        )