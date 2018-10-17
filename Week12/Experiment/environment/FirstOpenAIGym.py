# FirstOpenAIGym.py

import gym
import os
import six
from input import user_input
from experiment_saver import counter_saver


class OpenAIGymExperiment:
    def __init__(self, expr_log_dir=None):
        self.expr_log_dir = expr_log_dir

    def run_episodes(self):
        user_input_module = user_input.UserInputModule(is_asyn=True)
        env = gym.make('Assault-v0')

        human_actions = {}
        for i_episode in range(5):
            episode_log_dir = self.expr_log_dir + '/' + 'episode-' + str(i_episode)
            if not os.path.exists(episode_log_dir):
                os.makedirs(episode_log_dir)

            env.reset()
            for t in range(10000):
                env.render()

                env.env.ale.saveScreenPNG(six.b(episode_log_dir + '/' + str(t) + '.png'))

                human_action = user_input_module.getInput()
                if human_action is None:
                    action = env.action_space.sample()
                else:
                    print(human_action)
                    human_actions[str(i_episode) + '_' + str(t)] = human_action
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

                observation, reward, done, info = env.step(action)

                if done:
                    print("Episode finished after {} time steps".format(t + 1))
                    break

        counter_saver.saveDictToFile(self.expr_log_dir + '/' + 'human_actions.txt', human_actions)
        env.close()


def main():
    user_input_module = user_input.UserInputModule(is_asyn=True)
    env = gym.make('Assault-v0')

    for i_episode in range(20):
        env.reset()
        for t in range(100):
            env.render()

            human_action = user_input_module.getInput()
            if human_action is None:
                action = env.action_space.sample()
            else:
                print(human_action)
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

            observation, reward, done, info = env.step(action)
            if done:
                print("Episode finished after {} time steps".format(t + 1))
                break
    env.close()


if __name__ == '__main__':
    main()

