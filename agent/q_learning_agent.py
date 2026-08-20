import random
from collections import defaultdict

from environment.world import UP, LEFT, RIGHT, DOWN


class QLearningAgent:
    def __init__(
        self,
        learning_rate=0.1,
        discount_factor=0.95,
        epsilon=1.0,
        epsilon_decay=0.995,
        epsilon_min=0.05,
    ):
        self.actions = [UP, LEFT, RIGHT, DOWN]

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        self.q_table = defaultdict(
            lambda: [0.0] * len(self.actions)
        )

    def get_discrete_state(self, state):
        agent_x = state[0]
        agent_y = state[1]
        resource_collected = state[4]

        grid_size = 40

        grid_x = int(agent_x // grid_size)
        grid_y = int(agent_y // grid_size)

        return (
            grid_x,
            grid_y,
            resource_collected,
        )

    def choose_action(self, state):
        discrete_state = self.get_discrete_state(state)

        # Exploration
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        # Exploitation
        q_values = self.q_table[discrete_state]

        max_q = max(q_values)

        best_actions = [
            action
            for action, q_value in zip(self.actions, q_values)
            if q_value == max_q
        ]

        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state, done):
        state = self.get_discrete_state(state)
        next_state = self.get_discrete_state(next_state)

        action_index = self.actions.index(action)

        current_q = self.q_table[state][action_index]

        if done:
            target = reward
        else:
            best_next_q = max(self.q_table[next_state])
            target = (
                reward
                + self.discount_factor * best_next_q
            )

        self.q_table[state][action_index] += (
            self.learning_rate
            * (target - current_q)
        )

    def decay_epsilon(self):
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay,
        )