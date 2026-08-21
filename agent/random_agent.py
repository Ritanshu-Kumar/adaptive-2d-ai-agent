import random

from environment.world import UP, LEFT, RIGHT, DOWN


class RandomAgent:
    def __init__(self):
        self.actions = [UP, LEFT, RIGHT, DOWN]

    def choose_action(self, state):
        return random.choice(self.actions)
