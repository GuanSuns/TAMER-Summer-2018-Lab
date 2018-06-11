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
    dest = np.zeros(shape=(172, 160, 3))
    print(dest.shape)
    for row in range(172):
        for col in range(160):
            for color_dim in range(3):
                dest[row, col, color_dim] = source[row, col, color_dim]
    return dest


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def getStateFromRgbWorld(rgb_world):
    """
        In state, 0: nothing, 1: wall, 2: path, 3: pacman, 4: scared ghost, 5: ghost, 6: food, 7: capsule
    """
    dim_world = rgb_world.shape
    state = np.zeros(shape=(dim_world[0], dim_world[1]), dtype=int)

    for row in range(dim_world[0]):
        for col in range(dim_world[1]):
            # check if it's wall or food or capsule (-1 denotes wall or food or capsule)
            if rgb_world[row, col, 0] == 228 \
                    and rgb_world[row, col, 1] == 111 \
                    and rgb_world[row, col, 2] == 111:
                state[row, col] = -1
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
            # ignore (0, 0, 0), set it to wall 1
            elif rgb_world[row, col, 0] == 0 \
                    and rgb_world[row, col, 1] == 0 \
                    and rgb_world[row, col, 2] == 0:
                state[row, col] = 1
            # then it should be a ghost (5 denotes ghost)
            else:
                state[row, col] = 5

    distinguishWallFoodCapsule(state)

    return state


def distinguishWallFoodCapsule(state):
    """
        In the input state, wall food and capsule should all be -1, this function help distinguish them
        In state, 0: nothing, 1: wall, 2: path, 3: pacman, 4: scared ghost, 5: ghost, 6: food, 7: capsule
    """
    dim_state = state.shape

    for row in range(dim_state[0]):
        for col in range(dim_state[1]):
            if state[row, col] == -1:
                # count component but not change its value
                n_component = countConnectedComponentSize(state, row, col, -1, -1)
                # if it's food
                if n_component < 20:
                    countConnectedComponentSize(state, row, col, -1, 6)
                # if it's capsule
                elif n_component < 30:
                    countConnectedComponentSize(state, row, col, -1, 7)
                # if it's wall
                else:
                    countConnectedComponentSize(state, row, col, -1, 1)


def countConnectedComponentSize(state, row, col, old_value, new_value):
    n_component = 0

    dim_state = state.shape
    max_depth = 210*160
    legal_moves = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]

    # queue for BFS
    que_start = 0
    que_end = 0
    queue_bfs = [[0, 0] for _ in range(0, max_depth)]  # format [x,y]
    expanded = set()

    # push initial state
    queue_bfs[que_start][0] = int(row)
    queue_bfs[que_start][1] = int(col)
    que_end += 1
    n_component += 1
    expanded.add((row, col))
    # update initial state
    state[row, col] = new_value

    while que_start <= que_end < max_depth:
        x = queue_bfs[que_start][0]
        y = queue_bfs[que_start][1]
        que_start += 1

        # spread out from the location to its neighbours
        neighbours = []
        for legal_move in legal_moves:
            new_x = x + legal_move[0]
            new_y = y + legal_move[1]
            if 0 <= new_x < dim_state[0] and 0 <= new_y < dim_state[1]:
                if state[new_x, new_y] == old_value:
                    neighbours.append((new_x, new_y))

        for new_x, new_y in neighbours:
            if que_end >= max_depth:
                break
            if (new_x, new_y) in expanded:
                continue

            expanded.add((new_x, new_y))
            state[new_x, new_y] = new_value
            n_component += 1

            queue_bfs[que_end][0] = new_x
            queue_bfs[que_end][1] = new_y
            que_end += 1

    return n_component


def getLegalActions(state, step_size=5):
    legal_actions = []
    pacman_pos = getPacmanPos(state)

    # if pacman disappears, then return None action
    if pacman_pos is None:
        return [Actions.NO.value]

    # check up
    if pacman_pos[0] - step_size >= 0 \
            and state[pacman_pos[0]-step_size, pacman_pos[1]] != 1:
        legal_actions.append(Actions.UP.value)
    # check left
    if pacman_pos[1] - step_size >= 0 \
            and state[pacman_pos[0], pacman_pos[1]-step_size] != 1:
        legal_actions.append(Actions.LEFT.value)
    # check down
    if pacman_pos[0] + step_size < 172 \
            and state[pacman_pos[0] + step_size, pacman_pos[1]] != 1:
        legal_actions.append(Actions.DOWN.value)
    # check right
    if pacman_pos[1] + step_size < 160 \
            and state[pacman_pos[0], pacman_pos[1]+step_size] != 1:
        legal_actions.append(Actions.RIGHT.value)

    return legal_actions


def getPacmanPos(state):
    """ returns the pacman position """
    pacman_pos = None
    dim_world = state.shape

    for row in range(dim_world[0]):
        for col in range(dim_world[1]):
            if state[row, col] == 3:
                pacman_pos = (row, col)
    return pacman_pos


def getNextPos(x, y, action, step_size=5):
    if action == Actions.UP.value:
        return x-step_size, y
    elif action == Actions.DOWN.value:
        return x+step_size, y
    elif action == Actions.LEFT.value:
        return x, y-step_size
    elif action == Actions.RIGHT.value:
        return x, y+step_size
    else:
        return x, y


class Dict(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)
