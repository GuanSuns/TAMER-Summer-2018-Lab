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

from .. import experimentConfigurator
from ..experimentConfigurator import ExperimentConfigurator

f_qValues = '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/results/converged_qValues.json'
root_log_dir = '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs'
# root_log_dir = '/u/guanlin/Desktop/experiment-logs'
# f_qValues = '/u/guanlin/Desktop/experiment-logs/results/converged_qValues.json'


def run_expr(n_sub_experiment=10):

    # experiment parameters
    N = n_sub_experiment

    # generate postfix
    postfix = ''
    postfix += ExperimentConfigurator.experimentConfig['agent_type']
    postfix += '_alpha' + str(ExperimentConfigurator.qLearningConfig['learning_rate'])
    # softmax or epsilon-greedy
    epsilon = ExperimentConfigurator.qLearningConfig['epsilon']
    if epsilon >= 0:
        postfix += '_epsilon' + str(epsilon)
    else:
        postfix += '_temp' + str(ExperimentConfigurator.qLearningConfig['init_temp']) \
                   + '_decrease' + str(ExperimentConfigurator.qLearningConfig['temp_decrease_rate'])
    # termination condition
    if ExperimentConfigurator.experimentConfig['check_policy_converge']:
        postfix += '_policyConverge'
    else:
        postfix += '_k' + str(ExperimentConfigurator.gridWorldConfig['n_episodes'])
    # user input method
    if ExperimentConfigurator.TamerConfig['Auto_Feedback_TAMER']:
        postfix += '_autoFeedback_no' + str(ExperimentConfigurator.AutoFeedbackConfig['prob_no_feedback'])
        postfix += '_wrong' + str(ExperimentConfigurator.AutoFeedbackConfig['prob_wrong_feedback'])
    elif ExperimentConfigurator.TamerConfig['is_asyn_input']:
        postfix += '_winSize' + str(ExperimentConfigurator.TamerConfig['agent_window_size'])
    else:
        postfix += '_synchInput'
    # environment stochastic or deterministic
    noise = ExperimentConfigurator.gridWorldConfig['noise']
    if noise > 0:
        postfix += ('_noise' + str(noise))
    postfix += '_speed' + str(ExperimentConfigurator.experimentConfig['display_speed'])

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
        tamerGridWorld = gridworld.TamerGridWorldExperiment(expr_log_dir=sub_experiment_log_dir
                                                            , optimal_policy=optimal_qValues)
        experiment_stat = tamerGridWorld.run_episodes()
        policy_agreement_ratio = experiment_stat[0]
        policy_agreement_ratios.append(policy_agreement_ratio)

    # calculate and plot average policy agreement ratios
    avg_policy_agreement_ratios = plotUtils.getAndPlotAveragePolicyAgreementRatios(policy_agreement_ratios
                                                                                   , no_graphics=ExperimentConfigurator.experimentConfig['text_only'])
    avg_policy_agreement_log_file = expr_log_dir + '/' + 'avg_policy_agreement_ratio.json'
    qValueSaver.saveDictToFile(avg_policy_agreement_log_file, avg_policy_agreement_ratios)


def run_experiments():
    # agent_type: "qLearningAgent" or "TamerAgent" or "preferenceTAMERAgent"
    agent_types = ["TamerAgent", "preferenceTAMERAgent"]
    n_sub_experiment = 20
    feedback_noises = [     # format: (no_feedback, wrong_feedback)
        (0, 0)
        , (0.1, 0)
        , (0.2, 0)
        , (0.3, 0)
        , (0, 0.1)
        , (0, 0.2)
        , (0, 0.3)
        , (0.1, 0.1)
        , (0.2, 0.2)
        , (0.3, 0.3)
    ]
    noises = [0, 0.1]
    alphas = [0.3]
    epsilons = [0.05, 0.1]
    init_temps = [1.0]
    temp_decrease_rates = [1.0]

    for agent_type in agent_types:
        for feedback_noise in feedback_noises:
            wrong_feedback = feedback_noise[1]
            no_feedback = feedback_noise[0]
            for noise in noises:
                for alpha in alphas:
                    for epsilon in epsilons:
                        params = {
                            'agent_type': agent_type,
                            'env_noise': noise,
                            'alpha': alpha,
                            'epsilon': epsilon,
                            'wrong_feedback': wrong_feedback,
                            'no_feedback': no_feedback
                        }
                        # use softmax
                        if epsilon == -1:
                            # test softmax with no temperature control
                            configExperiment(**params)
                            run_expr(n_sub_experiment=n_sub_experiment)

                            for init_temp in init_temps:
                                for temp_decrease_rate in temp_decrease_rates:
                                    # we have already tested softmax with no temperature control
                                    if init_temp == 1.0 and temp_decrease_rate == 1.0:
                                        continue
                                    params['init_temp'] = init_temp
                                    params['temp_decrease_rate'] = temp_decrease_rate
                                    configExperiment(**params)
                                    run_expr(n_sub_experiment=n_sub_experiment)
                        # epsilon greedy
                        else:
                            configExperiment(**params)
                            run_expr(n_sub_experiment=n_sub_experiment)

    raw_input('Press Enter to terminate the experiment')


def configExperiment(agent_type="TamerAgent"
                     , wrong_feedback=0, no_feedback=0
                     , env_noise=0, alpha=0.5, epsilon=0
                     , init_temp=1.0, temp_decrease_rate=1.0):
    # experiment config
    experimentConfig = {'agent_type': agent_type}
    ExperimentConfigurator.setExperimentConfig(experimentConfig)

    # qLearning config
    qLearningConfig = {
        'learning_rate': alpha
        , 'init_temp': init_temp
        , 'temp_decrease_rate': temp_decrease_rate
        , 'epsilon': epsilon}  # set epsilon to -1 to use softmax
    ExperimentConfigurator.setQLearningConfig(qLearningConfig)

    # Gridworld env config
    gridWorldConfig = {
        'noise': env_noise}
    ExperimentConfigurator.setGridWorldConfig(gridWorldConfig)

    # Auto feedback config
    autoFeedbackConfig = {
        'prob_wrong_feedback': wrong_feedback,
        'prob_no_feedback': no_feedback
    }
    ExperimentConfigurator.setAutoFeedbackConfig(autoFeedbackConfig)


if __name__ == '__main__':
    run_experiments()
