import pygame

from agent.random_agent import RandomAgent
from environment.world import World


WIDTH = 800
HEIGHT = 600

NUM_EPISODES = 100
MAX_STEPS = 500

FPS = 30


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Agent - Baseline")

clock = pygame.time.Clock()

world = World(WIDTH, HEIGHT)
agent = RandomAgent()

running = True

episode = 0

while running and episode < NUM_EPISODES:

    state = world.reset()

    total_reward = 0
    steps = 0
    done = False

    while running and not done and steps < MAX_STEPS:

        # Handle window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Agent chooses a random action
        action = agent.choose_action(state)

        # Environment responds
        state, reward, done = world.step(action)

        total_reward += reward
        steps += 1

        # Draw environment
        screen.fill((30, 30, 30))

        world.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)

    episode += 1

    print(
        f"Episode {episode}: "
        f"Reward={total_reward:.2f}, "
        f"Steps={steps}, "
        f"Success={done}"
    )

pygame.quit()