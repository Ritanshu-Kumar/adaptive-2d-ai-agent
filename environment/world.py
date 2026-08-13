import pygame

from environment.agent import Agent
from environment.objects import Obstacle, Resource, Exit


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.agent = Agent(100, 300)

        self.obstacles = [
            Obstacle(250, 150, 40, 250),
            Obstacle(450, 100, 40, 250),
            Obstacle(600, 350, 120, 40),
        ]

        self.resource = Resource(650, 150)

        self.exit = Exit(700, 500)

    def update(self):
        self.agent.handle_input()

    def draw(self, screen):
        self.agent.draw(screen)

        for obstacle in self.obstacles:
            obstacle.draw(screen)

        self.resource.draw(screen)
        self.exit.draw(screen)