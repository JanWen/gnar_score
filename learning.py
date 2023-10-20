import gym
env = gym.make('CartPole-v0', render_mode="human")
env.action_space.seed(42)

observation, info = env.reset(seed=42)

for i in range(1000):
    print(i)
    observation, reward, terminated, truncated, info = env.step(env.action_space.sample())

    if terminated or truncated:
        observation, info = env.reset()

env.close()