# policy_agreement_stat.py
#
# Statistic and visualization tools for policy agreement experiments
# -----------------------

import json
import matplotlib.pyplot as plt

temperature_control_experiments = ['/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/18_agentQ_alpha0.5_temp30_decrease1.005_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/17_agentQ_alpha0.5_temp10_decrease1.005_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/16_agentQ_alpha0.5_temp50_decrease1.05_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/15_agentQ_alpha0.5_temp1024.0_decrease1.2_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/14_agentQ_alpha0.5_temp1024.0_decrease2.0_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/13_agentQ_alpha0.5_temp1.0_decrease1.0_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json']
temperature_control_experiment_names = ['T:30 D:1.005', 'T:10 D:1.005', 'T:50 D:1.05', 'T:1024 D:1.2', 'T:1024 D:2', 'pure softmax']

e_greedy_experiments = ['/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/deterministic-environment/38_agentQ_alpha0.5_epsilon1_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/deterministic-environment/36_agentQ_alpha0.5_epsilon0.5_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/deterministic-environment/35_agentQ_alpha0.5_epsilon0.3_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/deterministic-environment/34_agentQ_alpha0.5_epsilon0.1_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/deterministic-environment/00_VDBE_with_episode_anneal/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/deterministic-environment/00_VDBE_no_episode_anneal/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/deterministic-environment/00_VDBE_0.1_no_episode_anneal/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/deterministic-environment/01_decay01_Episode_Annealing/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/deterministic-environment/02_decay02_Episode_Annealing/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/deterministic-environment/03_decay03_Episode_Annealing/avg_policy_agreement_ratio.json']
e_greedy_experiment_names = ['Random', 'e:0.5', 'e:0.3', 'e:0.1', 'VDBE with episode anneal', 'VDBE no episode anneal', 'VDBE 0.1 no episode anneal', 'episode-anneal, r=0.1', 'episode-anneal, r=0.2', 'episode-anneal, r=0.3']

compare_experiments = ['/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/26_agentTamer_alpha0.5_epsilon0.05_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/25_agentTamer_alpha0.5_epsilon0.01_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/19_agentTamer_alpha0.5_temp1.0_decrease1.0_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/11_agentQ_alpha0.5_epsilon1.0_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/09_agentQ_alpha0.5_epsilon0.5_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/08_agentQ_alpha0.5_epsilon0.3_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/16_agentQ_alpha0.5_temp50_decrease1.05_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/13_agentQ_alpha0.5_temp1.0_decrease1.0_policyConverge_synchInput_speed2.0/avg_policy_agreement_ratio.json']
compare_experiment_names = ['Tamer, e:0.05', 'Tamer, e:0.01', 'Tamer, softmax', 'Random', 'e:0.5', 'e:0.3', 'T:50 D:1.05', 'pure softmax']

plot_skip_set = ['episode-anneal, r=0.1', 'episode-anneal, r=0.2', 'Random', 'e:0.1', 'episode-anneal, r=0.3']


def compare_both_methods():
    ratios = list()
    # read ratios_dict from files
    for compare_experiment in compare_experiments:
        with open(compare_experiment) as f_ratios:
            str_ratio_dict = json.load(f_ratios)
            ratio_dict = dict()
            # convert string keys to int keys
            for str_key in str_ratio_dict:
                ratio_dict[int(str_key)] = str_ratio_dict[str_key]
            ratios.append(ratio_dict)
    # plot the ratios
    plotMultipleRatios(ratios, compare_experiment_names, 0, 360)
    # wait for user input
    raw_input("Press Enter to terminate")


def compare_temperature_control():
    ratios = list()
    # read ratios_dict from files
    for temperature_control_experiment in temperature_control_experiments:
        with open(temperature_control_experiment) as f_ratios:
            str_ratio_dict = json.load(f_ratios)
            ratio_dict = dict()
            # convert string keys to int keys
            for str_key in str_ratio_dict:
                ratio_dict[int(str_key)] = str_ratio_dict[str_key]
            ratios.append(ratio_dict)
    # plot the ratios
    plotMultipleRatios(ratios, temperature_control_experiment_names, 0, 200)
    # wait for user input
    raw_input("Press Enter to terminate")


def compare_epsilon():
    ratios = list()
    # read ratios_dict from files
    for e_greedy_experiment in e_greedy_experiments:
        with open(e_greedy_experiment) as f_ratios:
            str_ratio_dict = json.load(f_ratios)
            ratio_dict = dict()
            # convert string keys to int keys
            for str_key in str_ratio_dict:
                ratio_dict[int(str_key)] = str_ratio_dict[str_key]
            ratios.append(ratio_dict)
    # plot the ratios
    plotMultipleRatios(ratios, e_greedy_experiment_names, 0, 500)
    # wait for user input
    raw_input("Press Enter to terminate")


def plotMultipleRatios(ratios_dicts_list, names, min_index, max_index):
    # inner helper function
    def getPolicyAgreementRatio(ratio_dict, i_step):
        if i_step in ratio_dict:
            return ratio_dict[i_step]
        else:
            return 0.0
    for i in range(0, len(ratios_dicts_list)):
        ratios_dicts_item = ratios_dicts_list[i]
        name = names[i]
        if name in plot_skip_set:
            continue
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
    compare_epsilon()

