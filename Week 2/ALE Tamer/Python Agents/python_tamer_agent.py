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

        print state_features

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
        return self.bfs_features(state, next_x, next_y)

    def bfs_features(self, state, next_x, next_y):
        """
            extract features using BFS
            In state, 0: nothing, 1: wall, 2: path, 3: pacman, 4: scared ghost, 5: ghost, 6: food, 7: capsule
        """
        # init features
        features = utils.Dict()
        features['dist-food'] = None
        features['dist-capsule'] = None
        features['dist-ghost'] = None
        features['dist-scared-ghost'] = None
        features['bias'] = 1.0

        legal_moves = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
        dim_state = state.shape

        # queue for BFS
        que_start = 0
        que_end = 0
        max_depth = 160*210
        queue_bfs = [[0, 0, 0] for _ in range(0, max_depth)]  # format [x,y,depth]
        expanded = set()

        # push initial state
        queue_bfs[que_start][0] = int(next_x)
        queue_bfs[que_start][1] = int(next_y)
        queue_bfs[que_start][2] = 0
        que_end += 1
        expanded.add((next_x, next_y))

        while que_start <= que_end < max_depth:
            x = queue_bfs[que_start][0]
            y = queue_bfs[que_start][1]
            depth = queue_bfs[que_start][2]
            que_start += 1

            # if it's not wall
            if state[x, y] != 1:
                # if it's food
                if state[x, y] == 6 and features['dist-food'] is None:
                    features['dist-food'] = depth
                # if it's capsule
                if state[x, y] == 7 and features['dist-capsule'] is None:
                    features['dist-capsule'] = depth
                # if it's ghost
                if state[x, y] == 5 and features['dist-ghost'] is None:
                    features['dist-ghost'] = depth
                # if it's scared ghost
                if state[x, y] == 4 and features['dist-scared-ghost'] is None:
                    features['dist-scared-ghost'] = depth

                # spread out from the location to its neighbours
                neighbours = []
                for legal_move in legal_moves:
                    new_x = x + legal_move[0]
                    new_y = y + legal_move[1]
                    if 0 <= new_x < dim_state[0] and 0 <= new_y < dim_state[1]:
                        neighbours.append((new_x, new_y))

                for new_x, new_y in neighbours:
                    if que_end >= max_depth:
                        break
                    if (new_x, new_y) in expanded:
                        continue
                    else:
                        expanded.add((new_x, new_y))

                    new_depth = depth + 1
                    queue_bfs[que_end][0] = new_x
                    queue_bfs[que_end][1] = new_y
                    queue_bfs[que_end][2] = new_depth
                    que_end += 1

        # compute the features
        if features['dist-food'] is not None:
            features['dist-food'] = features['dist-food']/(160*170)
        else:
            features['dist-food'] = 0

        if features['dist-capsule'] is not None:
            features['dist-capsule'] = features['dist-capsule']/(160*170)
        else:
            features['dist-capsule'] = 0

        if features['dist-ghost'] is not None:
            features['dist-ghost'] = features['dist-ghost']/(160*170)
        else:
            features['dist-ghost'] = 0

        if features['dist-scared-ghost'] is not None:
            features['dist-scared-ghost'] = features['dist-scared-ghost']/(160*170)
        else:
            features['dist-scared-ghost'] = 0

        return features




