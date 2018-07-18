# policy_agreement_stat.py
#
# Statistic and visualization tools for policy agreement experiments
# -----------------------

import json
import matplotlib.pyplot as plt

noise_01_experiments = ['/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/08_agentQ_alpha0.3_epsilon0.1_policyConverge_synchInput_noise0.1_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/09_agentQ_alpha0.3_epsilon0.3_policyConverge_synchInput_noise0.1_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/10_agentQ_alpha0.3_epsilon0.5_policyConverge_synchInput_noise0.1_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/17_agentTamer_alpha0.3_epsilon0.3_policyConverge_synchInput_noise0.1_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/noise0.1_anneal/avg_policy_agreement_ratio.json']
noise_01_experiments_names = ['e: 0.1', 'e: 0.3', 'e: 0.5', 'Tamer, e:0.3', 'anneal']

noise_05_experiments = ['/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/11_agentQ_alpha0.3_epsilon0.1_policyConverge_synchInput_noise0.5_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/12_agentQ_alpha0.3_epsilon0.3_policyConverge_synchInput_noise0.5_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/13_agentQ_alpha0.3_epsilon0.5_policyConverge_synchInput_noise0.5_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/18_agentTamer_alpha0.3_epsilon0.3_policyConverge_synchInput_noise0.5_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/noise0.5_anneal/avg_policy_agreement_ratio.json']
noise_05_experiments_names = ['e: 0.1', 'e: 0.3', 'e: 0.5', 'Tamer, e:0.3', 'anneal']


noise_09_experiments = ['/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/14_agentQ_alpha0.3_epsilon0.1_policyConverge_synchInput_noise0.9_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/15_agentQ_alpha0.3_epsilon0.3_policyConverge_synchInput_noise0.9_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/16_agentQ_alpha0.3_epsilon0.5_policyConverge_synchInput_noise0.9_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/19_agentTamer_alpha0.3_epsilon0.3_policyConverge_synchInput_noise0.9_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/noise0.9_anneal/avg_policy_agreement_ratio.json']
noise_09_experiments_names = ['e: 0.1', 'e: 0.3', 'e: 0.5', 'Tamer, e:0.3', 'anneal']


noise_02_alpha_experiments = ['/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/00_agentQ_alpha0.1_epsilon0.3_policyConverge_synchInput_noise0.3_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/01_agentQ_alpha0.3_epsilon0.3_policyConverge_synchInput_noise0.3_speed2.0/avg_policy_agreement_ratio.json'
, '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/02_agentQ_alpha0.5_epsilon0.3_policyConverge_synchInput_noise0.3_speed2.0/avg_policy_agreement_ratio.json'
    , '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/stochastic-environment/03_agentQ_alpha0.8_epsilon0.3_policyConverge_synchInput_noise0.3_speed2.0/avg_policy_agreement_ratio.json']
noise_02_alpha_experiments_names = ['alpha:0.1', 'alpha:0.3', 'alpha:0.5', 'alpha:0.8']


def compare_noise_01():
    ratios = list()
    # read ratios_dict from files
    for noise_01_experiment in noise_01_experiments:
        with open(noise_01_experiment) as f_ratios:
            str_ratio_dict = json.load(f_ratios)
            ratio_dict = dict()
            # convert string keys to int keys
            for str_key in str_ratio_dict:
                ratio_dict[int(str_key)] = str_ratio_dict[str_key]
            ratios.append(ratio_dict)
    # plot the ratios
    plotMultipleRatios(ratios, noise_01_experiments_names, 0, 2000)
    # wait for user input
    raw_input("Press Enter to terminate")


def compare_noise_05():
    ratios = list()
    # read ratios_dict from files
    for noise_05_experiment in noise_05_experiments:
        with open(noise_05_experiment) as f_ratios:
            str_ratio_dict = json.load(f_ratios)
            ratio_dict = dict()
            # convert string keys to int keys
            for str_key in str_ratio_dict:
                ratio_dict[int(str_key)] = str_ratio_dict[str_key]
            ratios.append(ratio_dict)
    # plot the ratios
    plotMultipleRatios(ratios, noise_05_experiments_names, 0, 4000)
    # wait for user input
    raw_input("Press Enter to terminate")


def compare_noise_09():
    ratios = list()
    # read ratios_dict from files
    for noise_09_experiment in noise_09_experiments:
        with open(noise_09_experiment) as f_ratios:
            str_ratio_dict = json.load(f_ratios)
            ratio_dict = dict()
            # convert string keys to int keys
            for str_key in str_ratio_dict:
                ratio_dict[int(str_key)] = str_ratio_dict[str_key]
            ratios.append(ratio_dict)
    # plot the ratios
    plotMultipleRatios(ratios, noise_09_experiments_names, 0, 500)
    # wait for user input
    raw_input("Press Enter to terminate")


def compare_alphas_noise_02():
    ratios = list()
    # read ratios_dict from files
    for noise_02_alpha_experiment in noise_02_alpha_experiments:
        with open(noise_02_alpha_experiment) as f_ratios:
            str_ratio_dict = json.load(f_ratios)
            ratio_dict = dict()
            # convert string keys to int keys
            for str_key in str_ratio_dict:
                ratio_dict[int(str_key)] = str_ratio_dict[str_key]
            ratios.append(ratio_dict)
    # plot the ratios
    plotMultipleRatios(ratios, noise_02_alpha_experiments_names, 0, 500)
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
    compare_noise_09()

