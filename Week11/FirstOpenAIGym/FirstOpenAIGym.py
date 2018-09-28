# FirstOpenAIGym.py

import gym
from input import user_input


def main():
    user_input_module = user_input.UserInputModule(is_asyn=False)
    env = gym.make('CartPole-v0')

    for i_episode in range(20):
        observation = env.reset()
        for t in range(100):
            env.render()
            print(observation)
            human_action = user_input_module.getInput()
            if human_action == 'a':
                action = 0
            else:
                action = 1
            print(action)
            observation, reward, done, info = env.step(action)
            if done:
                print("Episode finished after {} time steps".format(t + 1))
                break


if __name__ == '__main__':
    main()

