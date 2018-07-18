# autoFeedback.py
# ------------

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


def getAutoHumanFeedback(new_state, previous_state):
    if new_state is None or previous_state is None:
        return 0

    # evaluate terminal state
    if isinstance(new_state, str):
        if (previous_state, new_state) in terminalFeedbackValues:
            return terminalFeedbackValues[(previous_state, new_state)]
        else:
            return -1
    # evaluate non-terminal state
    if (previous_state, new_state) in feedbackValues:
        return feedbackValues[(previous_state, new_state)]
    else:
        return -1

