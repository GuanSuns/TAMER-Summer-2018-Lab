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
        self.weights['bias'] = 0
        self.window_size = window_size
        self.experiences = list()
        self.max_n_experiences = max_n_experiences

    def receiveHumanSignal(self, signal):
        """ receive human signal and update the weights """
        # do nothing when the signal is 0 or it's not in training
        if signal == 0 or not self.isTraining:
            return
        current_time = time.time()

    def getAction(self, state):
        """
          Compute the best action to take in a state.
        """
        legal_actions = utils.getLegalActions(state)

        max_action = None
        max_q_value = -9999999
        for action in legal_actions:
            q_value = self.getQValue(state, action)
            if q_value > max_q_value:
                max_q_value = q_value
                max_action = action
        return max_action

    def getWeights(self):
        return self.weights

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

    def extract_state(self, rgb_state):
        """
            return the state based on current game RGB values
            In state, 0: nothing, 1: wall, 2: path, 3: pacman, 4: scared ghost, 5: ghost, 6: food, 7: capsule
        """
        return {'state': utils.getStateFromRgbWorld(rgb_state)}

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

    def getStateFeatures(self, state, action):
        # get pacman pos
        (x, y) = utils.getPacmanPos(state)
        # compute the next pos
        (next_x, next_y) = utils.getNextPos(x, y, action)
        # use bfs to get features
        return self.bfs_features(state, x, y, next_x, next_y)

    def bfs_features(self, state, x, y, next_x, next_y):
        # init features
        features = utils.Dict()
        features['dist-food'] = 9999999999999
        features['dist-capsule'] = 9999999999999
        features['dist-ghost'] = 0
        features['dist-scared-ghost'] = 9999999999999




