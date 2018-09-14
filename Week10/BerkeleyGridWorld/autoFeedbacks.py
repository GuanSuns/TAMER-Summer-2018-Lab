# autoFeedback.py
# ------------

import util
from experimentConfigurator import ExperimentConfigurator

feedbackValues = {
    ((4, 2), (4, 2)): 1
    , ((0, 1), (1, 1)): 1
    , ((1, 1), (2, 1)): 1
    , ((2, 1), (3, 1)): 1
    , ((3, 1), (4, 1)): 1
    , ((4, 1), (4, 2)): 1
    , ((0, 2), (0, 1)): 1
    , ((0, 3), (0, 2)): 1
    , ((0, 3), (0, 4)): 1
    , ((0, 4), (1, 4)): 1
    , ((1, 4), (2, 4)): 1
    , ((2, 4), (3, 4)): 1
    , ((2, 4), (2, 3)): 1
    , ((2, 3), (3, 3)): 1
    , ((3, 4), (3, 3)): 1
    , ((3, 4), (4, 4)): 1
    , ((4, 4), (4, 3)): 1
    , ((4, 3), (4, 2)): 1
    , ((3, 3), (4, 3)): 1
}

terminalFeedbackValues = {
    ((4, 2), 'TERMINAL_STATE'): 1
}


class AutoFeedback:
    def __init__(self):
        pass

    def getAutoHumanFeedback(self, new_state, previous_state):
        if new_state is None or previous_state is None:
            return 0
        # evaluate terminal state
        if isinstance(new_state, str):
            if (previous_state, new_state) in terminalFeedbackValues:
                # simulate the case when human makes mistakes
                correct_feedback = terminalFeedbackValues[(previous_state, new_state)]
            else:
                correct_feedback = -1
        # evaluate non-terminal state
        elif (previous_state, new_state) in feedbackValues:
            # simulate the case when human makes mistakes
            correct_feedback = feedbackValues[(previous_state, new_state)]
        else:
            correct_feedback = -1

        # generate feedback
        return AutoFeedback.generateFeedback(correct_feedback)

    @staticmethod
    def generateFeedback(correct_feedback):
        # simulate the case when there is no feedback
        if util.flipCoin(ExperimentConfigurator.AutoFeedbackConfig['prob_no_feedback']):
            return 0
        # simulate the case when the human makes mistake
        if util.flipCoin(ExperimentConfigurator.AutoFeedbackConfig['prob_wrong_feedback']):
            return -correct_feedback


