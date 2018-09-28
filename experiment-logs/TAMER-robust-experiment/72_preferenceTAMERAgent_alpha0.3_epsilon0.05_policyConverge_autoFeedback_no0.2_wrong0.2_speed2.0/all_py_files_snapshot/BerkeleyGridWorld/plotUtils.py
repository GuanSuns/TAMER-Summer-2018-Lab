# plotUtils.py
# ------------

import numpy as np
import matplotlib.pyplot as plt


def plotAgreementRatios(ratio_dict, is_new_figure=False):
    indices = ratio_dict.keys()
    min_index = np.min(indices)
    max_index = np.max(indices)
    ratio_list = list()
    for i in range(min_index, max_index+1):
        if i in ratio_dict:
            ratio_list.append(ratio_dict[i])
        else:
            ratio_list.append(0)
    # return if the list is empty
    if len(ratio_list) == 0:
        return
    # plot the ratio list
    plt.ion()
    # it can be used to control whether to show all the lines in one figure
    if is_new_figure:
        plt.figure()
    plt.show()
    plt.plot(ratio_list)
    plt.xlabel('steps')
    plt.ylabel('policy agreement ratios')
    plt.draw()
    plt.pause(0.001)


def getAndPlotAveragePolicyAgreementRatios(ratios_list, no_graphics=False):
    # inner helper function
    def getPolicyAgreementRatios(ratio_dict, i_step):
        keys = ratio_dict.keys()
        max_key = np.max(keys)
        if i_step in ratio_dict:
            return ratio_dict[i_step]
        else:
            # otherwise return the last value
            return ratio_dict[max_key]

    # find the smallest and largest index
    min_index = np.inf
    max_index = -np.inf
    for ratios in ratios_list:
        min_index = min(min_index, np.min(ratios.keys()))
        max_index = max(max_index, np.max(ratios.keys()))

    n_experiments = len(ratios_list)
    avg_agreement_ratios = dict()
    for i in range(min_index, max_index+1):
        sum_agreement_ratios = float(np.sum([getPolicyAgreementRatios(ratios, i) for ratios in ratios_list]))
        avg_agreement_ratios[i] = sum_agreement_ratios / float(n_experiments)

    # plot the ratios
    if not no_graphics:
        plotAgreementRatios(avg_agreement_ratios, True)
    # return the calculated avg ratios
    return avg_agreement_ratios





