# visualize_VDBE.py
#
# tool to visualize the change of VDBE values
# -----------------------

import json
import matplotlib.pyplot as plt

VDBE_value_states = [
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 1),
    (1, 4),
    (2, 1),
    (2, 3),
    (2, 4),
    (3, 1),
    (3, 3),
    (3, 4),
    (4, 1),
    (4, 3),
    (4, 4),
]

VDBE_values_dir = '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/00_agentQ_alpha0.5_epsilon0.3_policyConverge_synchInput_speed2.0/sub-experiment-1'


def visual_VDBEs():
    values_list = list()
    names = list()
    for state in VDBE_value_states:
        log_file = VDBE_values_dir + '/vdbe-' + str(state[0]) + '-' + str(state[1]) + '.json'
        names.append(str(state[0]) + '-' + str(state[1]))
        with open(log_file) as f_ratios:
            values = json.load(f_ratios)
            values_list.append(values)
    # plot the ratios
    plotMultipleValues(values_list, names)
    # wait for user input
    raw_input("Press Enter to terminate")


def plotMultipleValues(values_list, names):
    for i in range(0, len(values_list)):
        values_item = values_list[i]
        name = names[i]
        plotValues(values_item, name)


def plotValues(values, name):
    # plot the ratio list
    plt.ion()
    plt.show()
    plt.plot(values, label=name)
    plt.xlabel('steps')
    plt.ylabel('VDBE')
    plt.legend()
    plt.draw()
    plt.pause(0.001)


if __name__ == '__main__':
    visual_VDBEs()
