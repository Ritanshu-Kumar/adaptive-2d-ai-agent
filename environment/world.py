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
      old_x = self.agent.x
      old_y = self.agent.y

      self.agent.handle_input()

      self.keep_agent_inside()

      if self.check_collision():
          self.agent.x = old_x
          self.agent.y = old_y

      self.check_resource()

    def draw(self, screen):
        self.agent.draw(screen)

        for obstacle in self.obstacles:
            obstacle.draw(screen)

        self.resource.draw(screen)
        self.exit.draw(screen)

    def check_collision(self):
      for obstacle in self.obstacles:
          if self.agent.rect.colliderect(obstacle.rect):
              return True

      return False

    def keep_agent_inside(self):
      self.agent.x = max(
          0,
          min(self.agent.x, self.width - self.agent.size)
      )

      self.agent.y = max(
          0,
          min(self.agent.y, self.height - self.agent.size)
      )

    def check_resource(self):
      if not self.resource.collected:
          resource_rect = pygame.Rect(
              self.resource.x - self.resource.radius,
              self.resource.y - self.resource.radius,
              self.resource.radius * 2,
              self.resource.radius * 2
          )

          if self.agent.rect.colliderect(resource_rect):
              self.resource.collected = True

    def reached_exit(self):
      return self.agent.rect.colliderect(self.exit.rect)

    def reached_goal(self):
      return (
          self.resource.collected
          and self.reached_exit()
      )