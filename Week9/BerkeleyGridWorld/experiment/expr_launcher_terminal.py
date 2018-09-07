# expr_runner_terminal.py
#
# experiment launcher used in terminal (command line)
# -----------------------

import os
from ..experiment_creater_and_resumer.experiment_creater_and_resumer import ExprCreaterAndResumer
from .. import gridworld
from ..input import user_input
from .. import qValueSaver
from .. import plotUtils

f_qValues = '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/results/converged_qValues.json'
root_log_dir = '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs'
# root_log_dir = '/u/guanlin/Desktop/experiment-logs'
# f_qValues = '/u/guanlin/Desktop/experiment-logs/results/converged_qValues.json'


def run_expr(alpha=0.5, epsilon=0.05, init_temp=1.0, temp_decrease_rate=1.0, noise=0.0
             , n_sub_experiment=10, agent_type="qLearningAgent"):
    """
    :param alpha: learning rate
    :param epsilon: epsilon >= 0 - use e-greedy; epsilon < 0 - use softmax
    :param init_temp: initial temperature
    :param temp_decrease_rate: temperature decreasing rate
    :param noise: the probability of moving to an unexpected state
    :param n_sub_experiment: the number of experiments for each setting
    :param agent_type: "qLearningAgent" or "TamerAgent" or "preferenceTAMERAgent"

    """
    # TAMER global parameters
    window_size = 1     # Tamer agent window size
    max_n_experience = 2000     # Tamer agent replay buffer maximum size
    is_asyn = False      # whether to receive input asynchronously

    # learning environment global parameters
    noise = noise
    n_episodes = 800
    display_speed = 2.0

    # experiment global parameters
    N = n_sub_experiment
    check_policy_converge = True
    text_only = False

    # generate postfix
    postfix = ''
    postfix += agent_type
    postfix += '_alpha' + str(alpha)
    # softmax or epsilon-greedy
    if epsilon >= 0:
        postfix += '_epsilon' + str(epsilon)
    else:
        postfix += '_temp' + str(init_temp) + '_decrease' + str(temp_decrease_rate)
    # termination condition
    if check_policy_converge:
        postfix += '_policyConverge'
    else:
        postfix += '_k' + str(n_episodes)
    # user input method
    if is_asyn:
        postfix += '_winSize' + str(window_size)
    else:
        postfix += '_synchInput'
    # environment stochastic or deterministic
    if noise > 0:
        postfix += ('_noise' + str(noise))
    postfix += '_speed' + str(display_speed)

    expr_saver = ExprCreaterAndResumer(rootdir=root_log_dir, postfix=postfix)
    expr_log_dir = expr_saver.getLogDir()

    # load optimal q-values
    optimal_qValues = qValueSaver.readQValuesFromJsonFile(f_qValues)

    # save experiment runner
    expr_saver.dump_src_code_and_model_def(fname=__file__)
    # save grid world related files
    fname = gridworld.__file__
    if fname.endswith('.pyc'):
        fname = fname.replace(".pyc", ".py")
    expr_saver.dump_src_code_and_model_def(fname=fname)
    # save input module related files
    fname = user_input.__file__
    if fname.endswith('.pyc'):
        fname = fname.replace(".pyc", ".py")
    expr_saver.dump_src_code_and_model_def(fname=fname)

    # run experiments
    policy_agreement_ratios = list()
    for i in range(0, N):
        print("*************************************")
        print("*** Start Sub-Experiment %s **********" % i)
        print("*************************************")
        # create sub-experiment directory
        sub_experiment_log_dir = expr_log_dir + '/sub-experiment-' + str(i)
        if not os.path.exists(sub_experiment_log_dir):
            os.makedirs(sub_experiment_log_dir)
        tamerGridWorld = gridworld.TamerGridWorldExperiment(learning_rate=alpha
                                                            , noise=noise
                                                            , epsilon=epsilon
                                                            , agent_max_n_experiences=max_n_experience
                                                            , agent_window_size=window_size
                                                            , n_episodes=n_episodes
                                                            , display_speed=display_speed
                                                            , is_asyn_input=is_asyn
                                                            , expr_log_dir=sub_experiment_log_dir
                                                            , optimal_policy=optimal_qValues
                                                            , check_policy_converge=check_policy_converge
                                                            , init_temp=init_temp
                                                            , temp_decrease_rate=temp_decrease_rate
                                                            , text_only=text_only
                                                            , agent_type=agent_type)
        experiment_stat = tamerGridWorld.run_episodes()
        policy_agreement_ratio = experiment_stat[0]
        policy_agreement_ratios.append(policy_agreement_ratio)

    # calculate and plot average policy agreement ratios
    avg_policy_agreement_ratios = plotUtils.getAndPlotAveragePolicyAgreementRatios(policy_agreement_ratios
                                                                                   , no_graphics=text_only)
    avg_policy_agreement_log_file = expr_log_dir + '/' + 'avg_policy_agreement_ratio.json'
    qValueSaver.saveDictToFile(avg_policy_agreement_log_file, avg_policy_agreement_ratios)


def run_experiments():
    # agent_type: "qLearningAgent" or "TamerAgent" or "preferenceTAMERAgent"
    agent_types = ["preferenceTAMERAgent"]
    n_sub_experiment = 20
    noises = [0.1, 0.3, 0.5, 0.7]
    alphas = [0.3]
    epsilons = [0.1]
    init_temps = [1.0]
    temp_decrease_rates = [1.0]

    for agent_type in agent_types:
        for noise in noises:
            for alpha in alphas:
                for epsilon in epsilons:
                    # use softmax
                    if epsilon == -1:
                        # test softmax with no temperature control
                        run_expr(alpha=alpha, epsilon=epsilon, init_temp=1.0, temp_decrease_rate=1.0, noise=noise
                                 , n_sub_experiment=n_sub_experiment, agent_type=agent_type)

                        for init_temp in init_temps:
                            for temp_decrease_rate in temp_decrease_rates:
                                # we have already tested softmax with no temperature control
                                if init_temp == 1.0 and temp_decrease_rate == 1.0:
                                    continue
                                run_expr(alpha=alpha, epsilon=epsilon, init_temp=init_temp
                                         , temp_decrease_rate=temp_decrease_rate, noise=noise
                                         , n_sub_experiment=n_sub_experiment
                                         , agent_type=agent_type)
                    # epsilon greedy
                    else:
                        run_expr(alpha=alpha, epsilon=epsilon, noise=noise, n_sub_experiment=n_sub_experiment
                                 , agent_type=agent_type)

    raw_input('Press Enter to terminate the experiment')


if __name__ == '__main__':
    run_experiments()
