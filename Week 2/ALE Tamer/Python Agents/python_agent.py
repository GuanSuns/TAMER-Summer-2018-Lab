# python_agent.py
# Author: Lin Guan
#
# The abstract class defined for python agents
# --------------

import utils


class PythonAgent:
    def __init__(self, index=0):
        self.index = index

    def getAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        utils.raiseNotDefined("getAction")


class PythonReinforcementAgent(PythonAgent):
    def __init__(self, index=0):
        PythonAgent.__init__(self, index)

    
