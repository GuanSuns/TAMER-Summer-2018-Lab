# expr_runner_terminal.py
#
# experiment launcher used in terminal (command line)
# -----------------------

from ..experiment_creater_and_resumer.experiment_creater_and_resumer import ExprCreaterAndResumer
from .. import gridworld
from ..input import user_input
from .. import qValueSaver


def run_expr():
    # agent parameters
    is_use_q_agent = True  # use qAgent or use Tamer agent
    alpha = 0.5     # learning rate
    epsilon = 0.0   # exploration rate
    window_size = 1     # Tamer agent window size
    max_n_experience = 2000     # Tamer agent maximum number of experiences
    is_asyn = False      # whether to receive input asynchronously

    # learning environment parameters
    n_episodes = 100
    display_speed = 2.0

    # experiment parameters
    delta = 0.02
    check_policy_converge = True
    check_value_converge = False

    # generate postfix
    postfix = ''
    postfix += 'agent' + ('Q' if is_use_q_agent else 'Tamer')
    postfix += '_alpha' + str(alpha)
    postfix += '_epsilon' + str(epsilon)
    if check_value_converge:
        postfix += '_valueConverge'
    elif check_policy_converge:
        postfix += '_policyConverge'
    else:
        postfix += '_k' + str(n_episodes)
    if is_asyn:
        postfix += '_winSize' + str(window_size)
    else:
        postfix += '_synchInput'
    postfix += '_speed' + str(display_speed)

    root_log_dir = '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs'
    expr_saver = ExprCreaterAndResumer(rootdir=root_log_dir, postfix=postfix)
    expr_log_dir = expr_saver.getLogDir()

    # load optimal q-values
    f_qValues = '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs/results/converged_qValues.json'
    optimal_qValues = qValueSaver.readQValuesFromJsonFile(f_qValues)

    # save experiment runner
    expr_saver.dump_src_code_and_model_def(fname=__file__)
    # save grid world related files
    expr_saver.dump_src_code_and_model_def(fname=gridworld.__file__)
    # save input module related files
    expr_saver.dump_src_code_and_model_def(fname=user_input.__file__)

    # run experiment
    tamerGridWorld = gridworld.TamerGridWorldExperiment(learning_rate=alpha
                                                        , epsilon=epsilon
                                                        , agent_max_n_experiences=max_n_experience
                                                        , agent_window_size=window_size
                                                        , n_episodes=n_episodes
                                                        , display_speed=display_speed
                                                        , is_asyn_input=is_asyn
                                                        , delta=delta
                                                        , expr_log_dir=expr_log_dir
                                                        , optimal_policy=optimal_qValues
                                                        , check_policy_converge=check_policy_converge
                                                        , check_value_converge=check_value_converge
                                                        , is_use_q_agent=is_use_q_agent)
    tamerGridWorld.run_episodes()


if __name__ == '__main__':
    run_expr()
