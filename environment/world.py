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
        """
        Apply one action and return:

        state  -> new state
        reward -> feedback for the action
        done   -> whether the episode has ended
        """

        previous_x = self.agent.x
        previous_y = self.agent.y
        previous_resource_collected = self.resource.collected

        # Distance to the current objective BEFORE the action
        previous_distance = self.distance_to_current_target()

        # Apply action
        if action == UP:
            self.agent.y -= self.agent.speed

        elif action == DOWN:
            self.agent.y += self.agent.speed

        elif action == LEFT:
            self.agent.x -= self.agent.speed

        elif action == RIGHT:
            self.agent.x += self.agent.speed

        # Keep agent inside the environment
        self.keep_agent_inside()

        # Check collision
        collision = self.check_collision()

        if collision:
            self.agent.x = previous_x
            self.agent.y = previous_y

        # Check resource
        self.check_resource()

        # Distance AFTER the action
        current_distance = self.distance_to_current_target()

        # --------------------------------------------------
        # Reward calculation
        # --------------------------------------------------

        # Small penalty for taking time
        reward = -0.01

        # Reward progress toward current objective
        distance_change = previous_distance - current_distance

        reward += distance_change * 0.05

        # Collision penalty
        if collision:
            reward -= 1

        # Resource collection reward
        if (
            not previous_resource_collected
            and self.resource.collected
        ):
            reward += 10

        # Goal reward
        done = self.reached_goal()

        if done:
            reward += 100

        # New state
        state = self.get_state()

        return state, reward, done

    def get_state(self):
        """
        Return the current state of the environment.
        """

        return [
            self.agent.x,
            self.agent.y,
            self.resource.x,
            self.resource.y,
            int(self.resource.collected),
            self.exit.rect.x,
            self.exit.rect.y,
        ]

    def reset(self):
        """
        Reset the environment for a new episode.
        """

        self.agent.x = 100
        self.agent.y = 300

        self.resource.collected = False

        return self.get_state()

    def distance_to_current_target(self):
        """
        Calculate the Euclidean distance between the agent
        and its current objective.

        Before collecting the resource:
            target = resource

        After collecting the resource:
            target = exit
        """

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