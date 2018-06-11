# python_tamer_agent.py
# Author: Lin Guan
#
# Reinforcement learning agent used in TAMER
# --------------


from python_agent import PythonReinforcementAgent


class TamerAgent(PythonReinforcementAgent):

    def __init__(self, index=0, isTraining=True
                 , epsilon=0.5, alpha=0.5, gamma=1):
        PythonReinforcementAgent.__init__(self, index, isTraining
                                          , epsilon, alpha, gamma)

    def receiveHumanSignal(self, signal):
        """ receive human signal and update the weights """
        # do nothing when the signal is 0
        if signal == 0:
            return

    def getAction(self, features):
        """
            The Agent will receive a GameState and
            must return an action
        """
        utils.raiseNotDefined("getAction")

    def extract_features(self, rgb_state):
        """ return the features based on current game RGB values"""
        pass

    def addExperience(self, experience):
        """
            Called by environment after
            observing a transition and reward

            experience should be in some format like (state, action, reward)
        """
        utils.raiseNotDefined("addExperience")

    def setIsTraining(self, isTraining):
        self.isTraining = isTraining

    def isInTraining(self):
        return self.isTraining

    def startEpisode(self):
        """
            Called by environment when new episode is starting
        """
        utils.raiseNotDefined("startEpisode")

    def stopEpisode(self):
        """
            Called by environment when episode is done
        """
        utils.raiseNotDefined("stopEpisode")

    def final(self, state):
        """
          Called by environment at the end
        """
        utils.raiseNotDefined("stopEpisode")

