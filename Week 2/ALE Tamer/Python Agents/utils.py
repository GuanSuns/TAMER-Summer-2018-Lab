# util.py
#
# Some utility functions for python agents
# -------

import sys
import numpy as np


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
    pass


class Dict(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)
