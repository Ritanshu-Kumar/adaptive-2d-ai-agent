import pygame

from agent.q_learning_agent import QLearningAgent
from environment.world import World
from training.model_io import load_q_table


WIDTH = 800
HEIGHT = 600

NUM_EPISODES = 50
MAX_STEPS = 500
FPS = 60


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-Learning Evaluation")

clock = pygame.time.Clock()

world = World(WIDTH, HEIGHT)
agent = QLearningAgent()

load_q_table(
    agent,
    "training/q_table.pkl"
)

agent.set_evaluation_mode()

successes = 0
resource_collections = 0

total_rewards = []
total_steps = []

running = True


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

        state = next_state

        total_reward += reward
        steps += 1

        screen.fill((30, 30, 30))

        world.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    if not running:
        break

    resource_collected = world.resource.collected

    if resource_collected:
        resource_collections += 1

    if done:
        successes += 1

    total_rewards.append(total_reward)
    total_steps.append(steps)

    print(
        f"Episode {episode + 1:3d} | "
        f"Reward: {total_reward:7.2f} | "
        f"Steps: {steps:3d} | "
        f"Resource: {resource_collected} | "
        f"Success: {done}"
    )


completed_episodes = len(total_rewards)

if completed_episodes > 0:
    average_reward = sum(total_rewards) / completed_episodes
    average_steps = sum(total_steps) / completed_episodes

    success_rate = (
        successes / completed_episodes
    ) * 100

    resource_rate = (
        resource_collections / completed_episodes
    ) * 100

    print("\nEvaluation Results")
    print("------------------")
    print(f"Episodes:              {completed_episodes}")
    print(f"Successful episodes:   {successes}")
    print(f"Success rate:          {success_rate:.2f}%")
    print(f"Resource collections:  {resource_collections}")
    print(f"Resource rate:         {resource_rate:.2f}%")
    print(f"Average reward:        {average_reward:.2f}")
    print(f"Average steps:         {average_steps:.2f}")


pygame.quit()