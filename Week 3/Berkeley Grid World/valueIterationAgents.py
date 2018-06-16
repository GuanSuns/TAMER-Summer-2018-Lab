# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()    # A Counter is a dict with default 0

        "*** YOUR CODE HERE ***"
        for i in range(0, iterations):
            # get all the states
            stateValues = util.Counter()
            states = mdp.getStates()

            for state in states:
                actions = mdp.getPossibleActions(state)
                # if there is no possible action, continue
                if len(actions) == 0:
                    continue

                # iterate through all the possible actions
                qValues = util.Counter()
                for action in actions:
                    qValues[action] = self.getQValue(state, action)
                # get the state value from qValues
                stateValues[state] = qValues[qValues.argMax()]

            # only update those states we reach
            for state in states:
                self.values[state] = stateValues[state]

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def getQValue(self, state, action):
        """
          The q-value of the state action pair
          (after the indicated number of value iteration
          passes).  Note that value iteration does not
          necessarily create this quantity and you may have
          to derive it on the fly.
        """
        "*** YOUR CODE HERE ***"
        qValue = 0
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)

        for nextState, probs in transitions:
            reward = self.mdp.getReward(state, action, nextState)
            qValue += probs * (reward + self.discount * self.values[nextState])

        return qValue

    def getPolicy(self, state):
        """
          The policy is the best action in the given state
          according to the values computed by value iteration.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        actions = mdp.getPossibleActions(state)

        if len(actions) == 0:
            return None

        # iterate through all the possible actions
        best_action = None
        best_q_value = -9999999999999

        for action in actions:
            qValue = self.getQValue(state, action)
            if qValue > best_q_value:
                best_action = action
                best_q_value = qValue

        return best_action

    def getAction(self, state):
        """ Returns the policy at the state (no exploration). """
        return self.getPolicy(state)

