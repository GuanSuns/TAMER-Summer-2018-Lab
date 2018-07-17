# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random
import util
import math
import numpy as np


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, init_temp=1024.0, temp_decrease_rate=2.0, **args):
        """
            init_temp - the initial temperature used for softmax
            temp_decrease_rate -  the value of softmax temperature decreasing rate
        """
        # you can initialize Q-values here...
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        # the key of Q-Values should be (state, action)
        self.qValues = util.Counter()
        self.temperatures = dict()
        self.init_temp = init_temp
        self.temp_decrease_rate = temp_decrease_rate
        self.is_show_real_values = True
        self.state_VDBE = dict     # just for fun, epsilon counter for VDBE

    def showRealValues(self):
        self.is_show_real_values = True

    def hideRealValues(self):
        self.is_show_real_values = False

    def getQValues(self):
        return self.qValues

    def getQValuesCopy(self):
        return self.qValues.copy()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # return 0 if hide-values is set and the state is not an exiting state
        if (not self.is_show_real_values) and (action != 'exit'):
            return 0

        return self.qValues[(state, action)]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return 0

        maxQValue = float("-inf")
        for action in actions:
            qValue = self.getQValue(state, action)
            if qValue > maxQValue:
                maxQValue = qValue
        return maxQValue

    def computeActionFromQValues(self, state):
        """
          Choose the action using softmax function
          epsilon >= 0: use e-greedy
          epsilon < 0: use softmax
        """
        "*** YOUR CODE HERE ***"
        # Get current temperature
        temperature = self.getTemperature(state)
        # update temperature
        self.updateTemperature(state)

        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return None

        qValues = list()
        for action in actions:
            qValue = float(self.getQValue(state, action))
            qValues.append(qValue)
        maxQValue = np.max(qValues)

        # if epsilon >= 0: use e-greedy
        if self.epsilon >= 0:
            actionId = np.random.choice(np.flatnonzero(maxQValue == qValues))
        # if epsilon < 0: use softmax
        else:
            softmaxValues = np.exp((qValues-maxQValue)/temperature)\
                            / float(np.sum(np.exp((qValues-maxQValue)/temperature)))
            actionId = np.random.choice(np.arange(0, len(actions)), p=softmaxValues)

        return actions[actionId]

    def updateTemperature(self, state):
        """ safely update the temperature for softmax """
        if state in self.temperatures:
            old_temperature = self.temperatures[state]
            # only update the temperature when it's not less than 0.5
            if old_temperature > 0.5:
                self.temperatures[state] = old_temperature / float(self.temp_decrease_rate)
        else:
            self.temperatures[state] = self.init_temp

    def getTemperature(self, state):
        """ return the temperature value of the state """
        if state in self.temperatures:
            return self.temperatures[state]
        else:
            self.temperatures[state] = self.init_temp
            return self.init_temp

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        # if there is no legal action
        if len(legalActions) == 0:
            return None

        # set the action to the best action
        action = self.computeActionFromQValues(state)
        # flip coin with probability of self.epsilon to determine whether to take random action
        if self.epsilon > 0 and util.flipCoin(self.epsilon):
            action = random.choice(legalActions)

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        oldQValue = self.getQValue(state, action)
        nextStateValue = self.computeValueFromQValues(nextState)

        newQValue = (1-self.alpha)*oldQValue + self.alpha*(reward + self.discount*nextStateValue)
        self.qValues[(state, action)] = newQValue

        # just for fun update VDBE
        self.updateVDBE(state, oldQValue, newQValue)

    def updateVDBE(self, state, old_qValue, new_qValue):
        # check if VDBE value for current state has been initialized
        if state not in self.state_VDBE:
            self.state_VDBE[state] = 1.0
        sigma = 0.33
        delta = 0.25
        qValue_error = np.fabs(float(new_qValue) - float(old_qValue))
        f = (1.0 - np.exp((-qValue_error)/sigma)) / (1.0 + np.exp((-qValue_error)/sigma))
        self.state_VDBE[state] = delta * f + (1 - delta) * self.state_VDBE[state]

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)

    def getAgentType(self):
        return 'qLearningAgent'


class TamerQAgent(QLearningAgent):
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
        """
        QLearningAgent.__init__(self, init_temp=init_temp
                                , temp_decrease_rate=temp_decrease_rate, **args)

        # initialize experiences list
        self.max_n_experiences = max_n_experiences
        self.experiences = list()
        self.window_size = window_size
        self.is_asyn_input = is_asyn_input

    def receiveHumanSignal(self, human_signal):
        """ receive human signal and update the weights """
        # do nothing when the signal is 0 or it's not in training
        if human_signal == 0:
            return

        # if pause-and-wait-for-user-feedback, only update according to the latest observation
        if not self.is_asyn_input:
            if len(self.experiences) > 0:
                # get the latest experience
                experience = self.experiences[len(self.experiences)-1]

                # do the update
                action = experience['action']
                state = experience['state']
                oldQValue = self.qValues[(state, action)]
                newQValue = oldQValue + self.alpha * (human_signal - oldQValue)
                self.qValues[(state, action)] = newQValue

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
            alpha = self.alpha
            for experience in self.experiences:
                action = experience['action']
                state = experience['state']
                oldQValue = self.qValues[(state, action)]
                newQValue = oldQValue + alpha * (human_signal - oldQValue)
                self.qValues[(state, action)] = newQValue

            # clear experiences
            self.experiences = list()

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

    def getAgentType(self):
        return 'TamerAgent'


class PacmanQAgent(QLearningAgent):
    """ Exactly the same as QLearningAgent, but with different default parameters """

    def __init__(self, epsilon=0.05, gamma=0.8
                 , alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        weights = self.getWeights()
        features = self.featExtractor.getFeatures(state, action)

        qValue = 0
        for name, value in features.items():
            qValue += weights[name]*value

        return qValue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        oldQValue = self.getQValue(state, action)
        newQValue = reward + self.discount * self.getValue(nextState)
        diff = newQValue - oldQValue

        weights = self.getWeights()
        features = self.featExtractor.getFeatures(state, action)
        for name, value in features.items():
            weight = weights[name]
            weights[name] = weight + self.alpha * diff * value

    def final(self, state):
        # Called at the end of each game.
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            print(self.getWeights())
