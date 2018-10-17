# FirstOpenAIGym.py

import gym
from input import user_input


def main():
    user_input_module = user_input.UserInputModule(is_asyn=False)
    env = gym.make('Assault-v0')

    for i_episode in range(20):
        observation = env.reset()
        for t in range(100):
            env.render()
            print(observation)

            human_action = user_input_module.getInput()
            if human_action == 'j':
                action = 0
            elif human_action == 'f':
                action = 1
            elif human_action == 'd':
                action = 2
            elif human_action == 's':
                action = 3
            elif human_action == 'a':
                action = 4
            elif human_action == 'k':
                action = 5
            else:
                action = 0
            print(action)

            observation, reward, done, info = env.step(action)
            if done:
                print("Episode finished after {} time steps".format(t + 1))
                break
    env.close()


if __name__ == '__main__':
    main()

