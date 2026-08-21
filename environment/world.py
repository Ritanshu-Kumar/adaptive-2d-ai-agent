import math
import pygame

from environment.agent import Agent
from environment.objects import Obstacle, Resource, Exit


UP = 0
LEFT = 1
RIGHT = 2
DOWN = 3


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

    def step(self, action):
        previous_x = self.agent.x
        previous_y = self.agent.y

        previous_resource_collected = self.resource.collected
        previous_distance = self.distance_to_current_target()

        self.agent.move(action)

        self.keep_agent_inside()

        collision = self.check_collision()

        if collision:
            self.agent.x = previous_x
            self.agent.y = previous_y

        self.check_resource()

        current_distance = self.distance_to_current_target()

        reward = -0.01

        distance_change = previous_distance - current_distance
        reward += distance_change * 0.05

        if collision:
            reward -= 1

        if (
            not previous_resource_collected
            and self.resource.collected
        ):
            reward += 10

        done = self.reached_goal()

        if done:
            reward += 100

        return self.get_state(), reward, done

    def discretize_distance(self, distance):
        if distance < 20:
            return 0

        elif distance < 50:
            return 1

        elif distance < 100:
            return 2

        else:
            return 3

    def get_target_direction(self):
        agent_center_x = self.agent.x + self.agent.size / 2
        agent_center_y = self.agent.y + self.agent.size / 2

        if not self.resource.collected:
            target_x = self.resource.x
            target_y = self.resource.y
        else:
            target_x = self.exit.rect.centerx
            target_y = self.exit.rect.centery

        dx = target_x - agent_center_x
        dy = target_y - agent_center_y

        if dx > 10:
            horizontal = 1
        elif dx < -10:
            horizontal = -1
        else:
            horizontal = 0

        if dy > 10:
            vertical = 1
        elif dy < -10:
            vertical = -1
        else:
            vertical = 0

        return horizontal, vertical

    def get_state(self):
        sensors = self.agent.get_sensor_distances(
            self.obstacles,
            self.width,
            self.height
        )

        sensor_state = (
            self.discretize_distance(sensors["up"]),
            self.discretize_distance(sensors["down"]),
            self.discretize_distance(sensors["left"]),
            self.discretize_distance(sensors["right"]),
            self.discretize_distance(sensors["up_left"]),
            self.discretize_distance(sensors["up_right"]),
            self.discretize_distance(sensors["down_left"]),
            self.discretize_distance(sensors["down_right"])
        )

        target_horizontal, target_vertical = (
            self.get_target_direction()
        )

        resource_collected = int(self.resource.collected)

        return (
            *sensor_state,
            target_horizontal,
            target_vertical,
            resource_collected
        )

    def distance_to_current_target(self):
        agent_center_x = self.agent.x + self.agent.size / 2
        agent_center_y = self.agent.y + self.agent.size / 2

        if not self.resource.collected:
            target_x = self.resource.x
            target_y = self.resource.y
        else:
            target_x = self.exit.rect.centerx
            target_y = self.exit.rect.centery

        return math.sqrt(
            (target_x - agent_center_x) ** 2
            + (target_y - agent_center_y) ** 2
        )

    def draw(self, screen):
        sensors = self.agent.get_sensor_distances(
            self.obstacles,
            self.width,
            self.height
        )

        self.agent.draw(screen, sensors)

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

    def reset(self):
        self.agent.x = 100
        self.agent.y = 300

        self.resource.collected = False

        return self.get_state()