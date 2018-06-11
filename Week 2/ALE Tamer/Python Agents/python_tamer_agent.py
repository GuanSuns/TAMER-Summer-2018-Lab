# python_tamer_agent.py
# Author: Lin Guan
#
# Reinforcement learning agent used in TAMER
# --------------


from python_agent import PythonReinforcementAgent
import utils
import time


class BasicTamerAgent(PythonReinforcementAgent):

    def __init__(self, index=0, isTraining=True
                 , epsilon=0.5, alpha=0.5, gamma=1, window_size=1, max_n_experiences=1000):
        """
            window_size: use the experiences within 1 second to update the weights
            max_n_experiences: maximum number of experiences stored in the history list
        """
        PythonReinforcementAgent.__init__(self, index, isTraining
                                          , epsilon, alpha, gamma)
        self.weights = utils.Dict()
        self.window_size = window_size
        self.experiences = list()
        self.max_n_experiences = max_n_experiences

    def receiveHumanSignal(self, signal):
        """ receive human signal and update the weights """
        # do nothing when the signal is 0 or it's not in training
        if signal == 0 or not self.isTraining:
            return
        current_time = time.time()

    def getAction(self, features):
        """
            The Agent will receive a GameState and
            must return an action
        """
        utils.raiseNotDefined("getAction")

    def getWeights(self):
        return self.weights

    def getStateFeatures(self, state, action):
        return {}

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        weights = self.getWeights()
        state_features = self.getStateFeatures(state, action)

        q_value = 0
        for name, value in state_features.items():
            q_value += weights[name]*value

        return q_value

    def getValue(self, state):
        return self.computeValueFromQValues(state)

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.
        """
        actions = state.getLegalActions(self.index)
        if len(actions) == 0:
            return 0

        max_q_value = -9999999
        for action in actions:
            q_value = self.getQValue(state, action)
            if q_value > max_q_value:
                max_q_value = q_value
        return max_q_value

    def extract_features(self, rgb_state):
        """ return the features based on current game RGB values"""
        pass

    def addExperience(self, experience):
        """
            Called by environment after
            observing a transition and reward

            experience should be in some format like (time, state, action, reward)
        """
        self.experiences.append(experience)
        while len(self.experiences) > self.max_n_experiences:
            self.experiences.pop(0)

    def setIsTraining(self, isTraining):
        self.isTraining = isTraining

    def isInTraining(self):
        return self.isTraining

    def startEpisode(self):
        """ Called by environment when new episode is starting """
        self.experiences = list()

    def stopEpisode(self):
        """ Called by environment when episode is done """
        print("Basic Tamer Agent - updated weights in this episode: ")
        print(self.weights)

    def final(self, state):
        """ Called by environment at the end """
        print("Basic Tamer Agent - final weights: ")
        print(self.weights)

