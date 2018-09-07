# PreferenceTamerAgent.py
# ------------------

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
from util import Counter

import random
import util
import math
import numpy as np

from qlearningAgents import TamerQAgent


class PreferenceTAMERAgent(TamerQAgent):
    def __init__(self, max_n_experiences=1000, window_size=1, is_asyn_input=True
                 , init_temp=1024.0, temp_decrease_rate=2.0, **args):
        """
            window_size: use the experiences within 2 seconds to update the weights
            max_n_experiences: maximum number of experiences stored in the history list

            Instance variables inherited from QLearningAgent
                - self.epsilon (exploration prob)
                - self.alpha (learning rate)
                - self.discount (discount rate)
            init_temp - the initial temperature used for softmax
            temp_decrease_rate -  the value of softmax temperature decreasing rate
            is_asyn_input - whether to wait for human feedback after taking an action
        """
        TamerQAgent.__init__(self, init_temp=init_temp
                                , temp_decrease_rate=temp_decrease_rate, **args)

        # initialize experiences list
        self.max_n_experiences = max_n_experiences
        self.experiences = list()
        self.window_size = window_size
        self.is_asyn_input = is_asyn_input

        # state-action credit (key: (state, action) value: credit)
        self.state_action_credit = Counter()

    def receiveHumanSignal(self, human_signal):
        """ receive human signal and update the weights """
        # do nothing when the signal is 0 or it's not in training
        if human_signal == 0:
            return

        # just for fun, update episode-wise epsilon annealing
        if self.use_episode_epsilon_anneal:
            self.updateEpisodeEpsilonAnnealing()

        # if pause-and-wait-for-user-feedback, only update according to the latest observation
        if not self.is_asyn_input:
            if len(self.experiences) > 0:
                # get the latest experience
                experience = self.experiences[len(self.experiences)-1]

                # do the update
                action = experience['action']
                state = experience['state']
                self.updateStateActionCredit(state, action, human_signal)

                # clear experiences
                self.experiences = list()
        else:
            # clear stale data
            current_time = time.time()
            while len(self.experiences) > 0:
                experience = self.experiences[0]
                if experience['time'] < current_time - self.window_size:
                    self.experiences.pop(0)
                else:
                    break

            # update q-values
            for experience in self.experiences:
                action = experience['action']
                state = experience['state']
                self.updateStateActionCredit(state, action, human_signal)

            # clear experiences
            self.experiences = list()

    def updateStateActionCredit(self, state, action, human_signal):
        old_credit = self.state_action_credit[(state, action)]
        self.state_action_credit[(state, action)] = old_credit + human_signal

    def update(self, state, action, nextState, reward):
        """
          Add the transition experience to experiences list
        """
        "*** YOUR CODE HERE ***"
        current_time = time.time()
        experience = {'time': current_time, 'action': action, 'state': state, 'nextState': nextState, 'reward': reward}
        self.experiences.append(experience)

        # pop out stale experience
        while len(self.experiences) > self.max_n_experiences:
            self.experiences.pop(0)

    def getAction(self, state):
        """
          Use softmax to choose action based on the state-action credits
        """
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return None

        action_credits = list()
        for action in actions:
            action_credit = float(self.getActionCredit(state, action))
            action_credits.append(action_credit)
        maxCredit = np.max(action_credits)

        temperature = 1.0
        softmaxValues = np.exp((action_credits - maxCredit) / temperature) \
                        / float(np.sum(np.exp((action_credits - maxCredit) / temperature)))
        actionId = np.random.choice(np.arange(0, len(actions)), p=softmaxValues)

        return actions[actionId]

    def getCurrentBestActions(self, state, is_single_action=False):
        """
        Choose the optimal action without any randomness
        """
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return None

        state_action_credits = list()
        for action in actions:
            action_credit = float(self.getActionCredit(state, action))
            state_action_credits.append(action_credit)
        maxActionCredit = np.max(state_action_credits)

        action_indices = np.flatnonzero(state_action_credits == maxActionCredit)
        if is_single_action:
            action_indices = random.choice(action_indices)
        return actions[action_indices]

    def getActionCredit(self, state, action):
        return self.state_action_credit[(state, action)]

    def getQValues(self):
        """ For displaying credit, use credit value to replace q-Value"""
        return self.state_action_credit

    def getQValuesCopy(self):
        """ For displaying credit, use credit value to replace q-Value"""
        return self.state_action_credit.copy()

    def getQValue(self, state, action):
        """ For displaying credit, use credit value to replace q-Value"""
        "*** YOUR CODE HERE ***"
        # return 0 if hide-values is set and the state is not an exiting state
        if (not self.is_show_real_values) and (action != 'exit'):
            return 0

        return self.getActionCredit(state, action)

    def getPolicy(self, state):
        return self.getCurrentBestActions(state, is_single_action=True)

    @staticmethod
    def getAgentType():
        return 'preferenceTAMERAgent'
