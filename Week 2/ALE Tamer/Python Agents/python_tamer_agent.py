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

        if signal == 0:
            return

