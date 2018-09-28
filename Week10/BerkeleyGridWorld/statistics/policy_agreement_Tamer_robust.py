# policy_agreement_stat.py
#
# Statistic and visualization tools for policy agreement experiments
# -----------------------

import json
import matplotlib.pyplot as plt

dir_robust_exp = '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/TAMER-robust-experiment/'
robust_experiments = ['01_TamerAgent_alpha0.3_epsilon0.1_policyConverge_autoFeedback_no0_wrong0_speed2.0'
    , '05_TamerAgent_alpha0.3_epsilon0.1_policyConverge_autoFeedback_no0.1_wrong0_speed2.0'
    , '09_TamerAgent_alpha0.3_epsilon0.1_policyConverge_autoFeedback_no0.2_wrong0_speed2.0'
    , '13_TamerAgent_alpha0.3_epsilon0.1_policyConverge_autoFeedback_no0.3_wrong0_speed2.0'
    , '17_TamerAgent_alpha0.3_epsilon0.1_policyConverge_autoFeedback_no0_wrong0.1_speed2.0'
    , '21_TamerAgent_alpha0.3_epsilon0.1_policyConverge_autoFeedback_no0_wrong0.2_speed2.0'
    , '25_TamerAgent_alpha0.3_epsilon0.1_policyConverge_autoFeedback_no0_wrong0.3_speed2.0'
    , '29_TamerAgent_alpha0.3_epsilon0.1_policyConverge_autoFeedback_no0.1_wrong0.1_speed2.0'
    , '33_TamerAgent_alpha0.3_epsilon0.1_policyConverge_autoFeedback_no0.2_wrong0.2_speed2.0'
    , '37_TamerAgent_alpha0.3_epsilon0.1_policyConverge_autoFeedback_no0.3_wrong0.3_speed2.0']
log_file_name = '/avg_policy_agreement_ratio.json'

robust_experiments_names = ['no:0, wrong:0', 'no:0.1, wrong:0'
    , 'no:0.2, wrong:0', 'no:0.3, wrong:0'
    , 'no:0, wrong:0.1', 'no:0, wrong:0.2', 'no:0, wrong:0.3'
    , 'no:0.1, wrong:0.1', 'no:0.2, wrong:0.2', 'no:0.3, wrong:0.3']


def compare_robust():
    ratios = list()
    # read ratios_dict from files
    for robust_experiment in robust_experiments:
        with open(dir_robust_exp + robust_experiment + log_file_name) as f_ratios:
            str_ratio_dict = json.load(f_ratios)
            ratio_dict = dict()
            # convert string keys to int keys
            for str_key in str_ratio_dict:
                ratio_dict[int(str_key)] = str_ratio_dict[str_key]
            ratios.append(ratio_dict)
    # plot the ratios
    plotMultipleRatios(ratios, robust_experiments_names, 0, 500)
    # wait for user input
    raw_input("Press Enter to terminate")


def plotMultipleRatios(ratios_dicts_list, names, min_index, max_index):
    # inner helper function
    def getPolicyAgreementRatio(ratio_dict, i_step):
        if i_step in ratio_dict:
            return ratio_dict[i_step]
        else:
            return 1.0
    for i in range(0, len(ratios_dicts_list)):
        ratios_dicts_item = ratios_dicts_list[i]
        name = names[i]
        # extract values in the specified range
        ratios = list()
        for j in range(min_index, max_index+1):
            ratios.append(getPolicyAgreementRatio(ratios_dicts_item, j))
        # plot the ratios
        plotRatios(ratios, name)


def plotRatios(ratios, name):
    # plot the ratio list
    plt.ion()
    plt.show()
    plt.plot(ratios, label=name)
    plt.xlabel('steps')
    plt.ylabel('policy agreement ratios')
    plt.legend()
    plt.draw()
    plt.pause(0.001)


if __name__ == '__main__':
    compare_robust()

