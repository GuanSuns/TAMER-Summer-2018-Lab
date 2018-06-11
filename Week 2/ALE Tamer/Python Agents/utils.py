# util.py
#
# Some utility functions for python agents
# -------

import sys
import numpy as np
from enum_actions import Actions


def raiseNotDefined(method_name):
    print("Method not implemented: %s" % method_name)
    sys.exit(1)


def copyBuffer(source):
    dest = np.ndarray(shape=(172, 160, 3))
    for row in range(172):
        for col in range(160):
            dest[row, col, :] = source[row, col, :]
    return dest


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def getStateFromRgbWorld(rgb_world):
    """
        In state, 0: nothing, 1: wall, 2: path, 3: pacman, 4: scared ghost, 5: ghost
    """
    dim_world = rgb_world.shape
    state = np.zeros(shape=(dim_world[0], dim_world[1]), dtype=int)

    for row in range(dim_world[0]):
        for col in range(dim_world[1]):
            # check if it's wall (1 denotes wall)
            if rgb_world[row, col, 0] == 228 \
                    and rgb_world[row, col, 1] == 111 \
                    and rgb_world[row, col, 2] == 111:
                state[row, col] = 1
            # check if it's path (2 denotes path)
            elif rgb_world[row, col, 0] == 0 \
                    and rgb_world[row, col, 1] == 28 \
                    and rgb_world[row, col, 2] == 136:
                state[row, col] = 2
            # check if it's pacman (3 denotes pacman)
            elif rgb_world[row, col, 0] == 210 \
                    and rgb_world[row, col, 1] == 164 \
                    and rgb_world[row, col, 2] == 74:
                state[row, col] = 3
            # check if it's scared ghost (4 denotes scared ghost)
            elif rgb_world[row, col, 0] == 66 \
                    and rgb_world[row, col, 1] == 114 \
                    and rgb_world[row, col, 2] == 194:
                state[row, col] = 4
            # ignore (0, 0, 0)
            elif rgb_world[row, col, 0] == 0 \
                    and rgb_world[row, col, 1] == 0 \
                    and rgb_world[row, col, 2] == 0:
                state[row, col] = 0
            # then it should be a ghost (5 denotes ghost)
            else:
                state[row, col] = 5

    return state


def getLegalActions(state):
    # check if UP is legal
    legal_actions = []
    dim_world = state.shape
    pacman_pos = None

    for row in range(dim_world[0]):
        for col in range(dim_world[1]):
            if state[row, col] == 3:
                pacman_pos = (row, col)

    # if pacman disappears, then return None action
    if pacman_pos is None:
        return [Actions.NO.value]





class Dict(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)
