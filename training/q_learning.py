import pygame
import sys

from agent.q_learning_agent import QLearningAgent
from environment.world import World

from training.model_io import save_q_table


WIDTH = 800
HEIGHT = 600

NUM_EPISODES = 500
MAX_STEPS = 500

FPS = 60
VISUAL_EPISODES = NUM_EPISODES


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-Learning Agent")

clock = pygame.time.Clock()

world = World(WIDTH, HEIGHT)
agent = QLearningAgent()

rewards_history = []
success_history = []

running = True

log_file = open(
    "training/q_learning_log.txt",
    "w",
    encoding="utf-8"
)

original_stdout = sys.stdout


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, message):
        for stream in self.streams:
            stream.write(message)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()


sys.stdout = Tee(original_stdout, log_file)


for episode in range(NUM_EPISODES):

    if not running:
        break

    state = world.reset()

    total_reward = 0
    steps = 0
    done = False

    while not done and steps < MAX_STEPS:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        if not running:
            break

        action = agent.choose_action(state)

        next_state, reward, done = world.step(action)

        agent.learn(
            state,
            action,
            reward,
            next_state,
            done
        )

        state = next_state

        total_reward += reward
        steps += 1

        if episode < VISUAL_EPISODES:
            screen.fill((30, 30, 30))

            world.draw(screen)

            pygame.display.flip()

        if episode < 10:
            clock.tick(FPS)
        else:
            clock.tick(240)

    if not running:
        break

    agent.decay_epsilon()

    resource_collected = world.resource.collected

    rewards_history.append(total_reward)
    success_history.append(int(done))

    print(
        f"Episode {episode + 1:4d} | "
        f"Reward: {total_reward:7.2f} | "
        f"Steps: {steps:3d} | "
        f"Resource: {resource_collected} | "
        f"Success: {done} | "
        f"Epsilon: {agent.epsilon:.3f}"
    )

save_q_table(
    agent.q_table,
    "training/q_table.pkl"
)

print("\nQ-table saved to training/q_table.pkl")    

pygame.quit()

sys.stdout = original_stdout
log_file.close()